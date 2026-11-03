"""Load, validate and assemble per-variant problem statements.

A variant file holds only the writer's prose, with [[A1]]-style placeholders
where attachments go. Assembly substitutes the verbatim attachments from the
task card. The special variant ``orig`` is the untouched SWE-bench text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from dialect_tax.cards import PLACEHOLDER_RE, Card
from dialect_tax.config import ORIGINAL_VARIANT

ARABIC_RE = re.compile(r"[؀-ۿ]")
LATIN_RE = re.compile(r"[A-Za-z]")

EXPECTED_SCRIPT = {
    "en": "latin",
    "msa": "arabic",
    "egy": "arabic",
    "gulf": "arabic",
    "lev": "arabic",
    "mag": "arabic",
    "egy-franco": "latin",
    "gulf-franco": "latin",
    "mag-franco": "latin",
}


@dataclass
class ValidationResult:
    instance_id: str
    variant: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def variant_path(variants_dir: Path, variant: str, instance_id: str) -> Path:
    return variants_dir / variant / f"{instance_id}.md"


def _strip_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", PLACEHOLDER_RE.sub("", text))


def arabic_ratio(text: str) -> float:
    body = _strip_code(text)
    arabic = len(ARABIC_RE.findall(body))
    latin = len(LATIN_RE.findall(body))
    return arabic / (arabic + latin) if arabic + latin else 0.0


def assemble(prose: str, card: Card) -> str:
    """Replace placeholders with verbatim attachments; append unreferenced ones at the end."""
    attachments = card.attachment_map()
    used: set[int] = set()

    def substitute(match: re.Match) -> str:
        n = int(match.group(1))
        if n not in attachments:
            raise ValueError(f"{card.instance_id}: unknown placeholder [[A{n}]]")
        used.add(n)
        return attachments[n].text

    body = PLACEHOLDER_RE.sub(substitute, prose.strip())
    leftovers = [a.text for a in card.attachments if a.id not in used]
    if leftovers:
        body = body + "\n\n" + "\n\n".join(leftovers)
    return body.strip() + "\n"


def problem_statement(variant: str, instance: dict, card: Card | None, variants_dir: Path) -> str:
    if variant == ORIGINAL_VARIANT:
        return instance["problem_statement"]
    if card is None:
        raise ValueError(f"{instance['instance_id']}: variant '{variant}' needs a card")
    path = variant_path(variants_dir, variant, instance["instance_id"])
    if not path.exists():
        raise FileNotFoundError(path)
    return assemble(path.read_text(), card)


def validate_variant(variant: str, card: Card, variants_dir: Path) -> ValidationResult:
    result = ValidationResult(card.instance_id, variant)
    path = variant_path(variants_dir, variant, card.instance_id)
    if not path.exists():
        result.errors.append("missing file")
        return result
    prose = path.read_text()
    words = _strip_code(prose).split()
    if len(words) < 8:
        result.errors.append(f"prose too short ({len(words)} words)")

    ids = card.attachment_map()
    referenced = [int(n) for n in PLACEHOLDER_RE.findall(prose)]
    unknown = sorted(set(referenced) - set(ids))
    if unknown:
        result.errors.append(f"unknown placeholders: {unknown}")
    missing = sorted(set(ids) - set(referenced))
    if missing:
        result.warnings.append(f"placeholders not referenced (will be appended at end): {missing}")
    duplicated = sorted({n for n in referenced if referenced.count(n) > 1})
    if duplicated:
        result.warnings.append(f"placeholders used more than once: {duplicated}")

    expected = EXPECTED_SCRIPT.get(variant)
    ratio = arabic_ratio(prose)
    if expected == "arabic" and ratio < 0.5:
        result.errors.append(f"expected Arabic script, Arabic ratio is {ratio:.0%}")
    if expected == "latin" and ratio > 0.05:
        result.errors.append(f"expected Latin script, Arabic ratio is {ratio:.0%}")

    for attachment in card.attachments:
        snippet = attachment.text.strip().splitlines()[1:2] if attachment.kind == "code" else []
        if snippet and snippet[0].strip() and len(snippet[0].strip()) > 20 and snippet[0].strip() in prose:
            result.warnings.append(f"attachment A{attachment.id} seems pasted inline instead of via placeholder")
    return result
