"""Split SWE-bench problem statements into prose and verbatim attachments.

The dialect variants only rewrite the prose. Code blocks, tracebacks and logs
(the "attachments") are kept byte-identical across variants, so any measured
difference comes from the natural-language part of the request.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\[\[A(\d+)\]\]")
FENCE_RE = re.compile(r"^(?P<fence>```|~~~)[^\n]*\n.*?^(?P=fence)[ \t]*$", re.DOTALL | re.MULTILINE)
TRACEBACK_START = "Traceback (most recent call last):"


@dataclass
class Attachment:
    id: int
    kind: str
    text: str

    @property
    def placeholder(self) -> str:
        return f"[[A{self.id}]]"


@dataclass
class Card:
    instance_id: str
    repo: str
    title: str
    units: list[str] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)
    original_prose: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, text: str) -> "Card":
        raw = json.loads(text)
        raw["attachments"] = [Attachment(**a) for a in raw.get("attachments", [])]
        return cls(**raw)

    def attachment_map(self) -> dict[int, Attachment]:
        return {a.id: a for a in self.attachments}


DETAILS_RE = re.compile(r"<details>.*?</details>", re.DOTALL | re.IGNORECASE)
IMAGE_RE = re.compile(r"<img\b[^>]*>|!\[[^\]]*\]\([^)\s]+\)", re.IGNORECASE)

# A line matching any of these (after stripping indentation) is treated as code, not prose.
# Needed because Trac-imported Django issues lose their code fences and indentation.
CODE_LINE_RE = re.compile(
    "|".join(
        [
            r">>>",
            r"\.\.\.(\s|$)",
            r"(In|Out)\s*\[\d+\]:",
            r"\$ \S",
            r"from\s+[\w.]+\s+import\s",
            r"import\s+[\w.]+(\s+as\s+\w+)?(\s*,\s*[\w.]+)*\s*$",
            r"(async\s+)?(class|def)\s+\w+.*:\s*$",
            r"@[\w.]+(\(.*\))?\s*$",
            r"(return|raise|assert|yield)\b",
            r"(pass|continue|break)\s*$",
            r"print\(",
            r"(if|elif|else|for|while|with|try|except|finally)\b.*:\s*$",
            r"[A-Za-z_][\w.]*(\[[^\]]*\])*\s*(=|\+=|-=|\*=)\s*[^=\s]",
            r"[A-Za-z_][\w.]*\(",
            r"[)\]}]+[,;)\]}]*\s*$",
            r"Traceback \(most recent call last\):",
            r"File \".*\", line \d+",
            r"[\w.]*(Error|Exception|Warning)(:|\s*$)",
            r"[\w.]+\.[A-Z]\d{3}:",
            r"(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER)\s",
        ]
    )
)
TRAC_METADATA_RE = re.compile(r"^\s*\(last modified by .*\)\s*$")
PROSE_SENTENCE_RE = re.compile(r"^[A-Z][a-z']*,?(\s+[\w'’“”\"(),.-]+){3,}|^[A-Z][a-z']*(\s+[\w'’“”\"(),.-]+)+[:.]\s*$")
MIN_BLOCK_CHARS = 10


def _is_code_line(line: str) -> bool:
    if not line.strip() or TRAC_METADATA_RE.match(line):
        return False
    if line.startswith(("    ", "\t")):
        return True
    return bool(CODE_LINE_RE.match(line.strip()))


def _line_code_blocks(text: str) -> list[tuple[int, int, str]]:
    """Group consecutive code-like lines (blank lines allowed inside) into (start, end, kind) spans.

    The first line is the issue title and is never treated as code.
    """
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    def next_nonblank(k: int) -> int:
        while k < len(lines) and not lines[k].strip():
            k += 1
        return k

    spans: list[tuple[int, int, str]] = []
    i = 1
    while i < len(lines):
        if not _is_code_line(lines[i]):
            i += 1
            continue
        j = i + 1
        in_session = lines[i].strip().startswith((">>>", "In ["))
        while j < len(lines):
            in_session = in_session or lines[j - 1].strip().startswith((">>>", "In ["))
            session_output = in_session and lines[j].strip() and not PROSE_SENTENCE_RE.match(lines[j])
            if _is_code_line(lines[j]) or session_output:
                j += 1
                continue
            k = next_nonblank(j)
            if not lines[j].strip() and k < len(lines) and _is_code_line(lines[k]):
                j = k
                continue
            break
        block = "".join(lines[i:j])
        if len(block.strip()) >= MIN_BLOCK_CHARS:
            kind = "traceback" if TRACEBACK_START in block else "code"
            spans.append((offsets[i], offsets[j], kind))
        i = j
    return spans


def _mask(text: str, spans: list[tuple[int, int, str]]) -> str:
    chars = list(text)
    for start, end, _ in spans:
        for k in range(start, end):
            if chars[k] != "\n":
                chars[k] = " "
    return "".join(chars)


def _overlaps(start: int, end: int, spans: list[tuple[int, int, str]]) -> bool:
    return any(s < end and start < e for s, e, _ in spans)


def split_problem_statement(text: str) -> tuple[str, list[Attachment]]:
    """Return (prose_with_placeholders, attachments). Identical blocks share one attachment id."""
    text = text.replace("\r\n", "\n")
    spans: list[tuple[int, int, str]] = [(m.start(), m.end(), "details") for m in DETAILS_RE.finditer(text)]
    for m in FENCE_RE.finditer(text):
        if not _overlaps(m.start(), m.end(), spans):
            spans.append((m.start(), m.end(), "code"))
    for m in IMAGE_RE.finditer(text):
        if not _overlaps(m.start(), m.end(), spans):
            spans.append((m.start(), m.end(), "image"))
    for start, end, kind in _line_code_blocks(_mask(text, spans)):
        if text[start:end].strip() and not _overlaps(start, end, spans):
            spans.append((start, end, kind))
    spans.sort()

    attachments: list[Attachment] = []
    by_text: dict[str, int] = {}
    out: list[str] = []
    cursor = 0
    for start, end, kind in spans:
        out.append(text[cursor:start])
        block = text[start:end].rstrip("\n")
        if block not in by_text:
            by_text[block] = len(attachments) + 1
            attachments.append(Attachment(id=by_text[block], kind=kind, text=block))
        out.append(f"[[A{by_text[block]}]]")
        if text[start:end].endswith("\n"):
            out.append("\n")
        cursor = end
    out.append(text[cursor:])
    prose = "".join(out).strip()
    return prose, attachments


def prose_length(text: str) -> int:
    prose, _ = split_problem_statement(text)
    return len(PLACEHOLDER_RE.sub("", prose).strip())


def build_card(instance: dict) -> Card:
    prose, attachments = split_problem_statement(instance["problem_statement"])
    first_line = instance["problem_statement"].strip().splitlines()[0] if instance["problem_statement"].strip() else ""
    return Card(
        instance_id=instance["instance_id"],
        repo=instance["repo"],
        title=first_line[:160],
        attachments=attachments,
        original_prose=prose,
    )


def load_card(cards_dir: Path, instance_id: str) -> Card:
    return Card.from_json((cards_dir / f"{instance_id}.json").read_text())


def save_card(cards_dir: Path, card: Card, *, keep_units: bool = True) -> Path:
    cards_dir.mkdir(parents=True, exist_ok=True)
    path = cards_dir / f"{card.instance_id}.json"
    if keep_units and path.exists():
        existing = Card.from_json(path.read_text())
        if existing.units and not card.units:
            card.units = existing.units
    path.write_text(card.to_json() + "\n")
    return path


def render_writer_sheet(card: Card) -> str:
    """Markdown sheet a native-speaker writer reads. Deliberately excludes the English prose."""
    lines = [
        f"# {card.instance_id}",
        "",
        f"**Repo:** `{card.repo}`",
        "",
        "## What the request must convey (all units, nothing extra)",
        "",
    ]
    if card.units:
        lines += [f"{i}. {u}" for i, u in enumerate(card.units, start=1)]
    else:
        lines.append("_(units not written yet)_")
    lines += ["", "## Attachments (paste the placeholder where you would paste the block)", ""]
    if not card.attachments:
        lines.append("_None: the request is prose only._")
    for a in card.attachments:
        already_fenced = a.text.lstrip().startswith(("```", "~~~"))
        lines += [f"### `{a.placeholder}` ({a.kind})", "", a.text if already_fenced else f"````\n{a.text}\n````", ""]
    return "\n".join(lines).rstrip() + "\n"
