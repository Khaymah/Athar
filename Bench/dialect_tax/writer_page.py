"""Build the writers' web page and import what writers submitted through it.

The page embeds the cards WITHOUT the original English prose or title, so
writers cannot translate. Submissions live in the artifact's shared store:

    claims/<instance_id>                 {uid, status: "claimed" | "submitted", at}
    subs/<uid>/tasks/<instance_id>       {en, egy, franco, status, updatedAt}
"""

from __future__ import annotations

import json
from pathlib import Path

from dialect_tax.cards import load_card
from dialect_tax.variants import variant_path

PAGE_FIELD_TO_VARIANT = {"en": "en", "egy": "egy", "franco": "egy-franco"}
CARDS_MARKER = "/*__CARDS__*/"


def build_page(template: Path, cards_dir: Path, task_ids: list[str], out: Path) -> Path:
    cards = []
    for iid in task_ids:
        card = load_card(cards_dir, iid)
        if not card.units:
            raise ValueError(f"{iid}: card has no units yet")
        cards.append(
            {
                "instance_id": card.instance_id,
                "repo": card.repo,
                "units": card.units,
                "units_ar": card.units_ar if len(card.units_ar) == len(card.units) else [],
                "attachments": [{"id": a.id, "kind": a.kind, "text": a.text} for a in card.attachments],
            }
        )
    payload = json.dumps(cards, ensure_ascii=False).replace("</", "<\\/")
    html = template.read_text()
    if CARDS_MARKER not in html:
        raise ValueError(f"{template} has no {CARDS_MARKER} marker")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html.replace(CARDS_MARKER, payload))
    return out


def _doc_body(raw: dict) -> dict:
    return raw["data"] if isinstance(raw.get("data"), dict) else raw


def dump_from_directory(root: Path) -> dict:
    """Build a dump from files saved by the store's out_dir export.

    Expects <root>/claims/<iid>.json and <root>/subs/<uid>/tasks/<iid>.json.
    """
    claims = {p.stem: _doc_body(json.loads(p.read_text())) for p in sorted((root / "claims").glob("*.json"))}
    subs: dict[str, dict] = {}
    for p in sorted((root / "subs").glob("*/tasks/*.json")):
        subs.setdefault(p.parent.parent.name, {})[p.stem] = _doc_body(json.loads(p.read_text()))
    return {"claims": claims, "subs": subs}


def import_submissions(dump: dict, variants_dir: Path, *, include_drafts: bool = False) -> dict[str, int]:
    """Write submitted texts to data/variants/<variant>/<id>.md and record who wrote what.

    ``dump`` = {"claims": {iid: {...}}, "subs": {uid: {iid: {...}}}} as pulled from the store.
    The claim decides which writer's text is canonical for a task.
    """
    claims: dict = dump.get("claims", {})
    subs: dict = dump.get("subs", {})
    provenance_path = variants_dir / "provenance.json"
    provenance = json.loads(provenance_path.read_text()) if provenance_path.exists() else {}
    counts = {"written": 0, "skipped_not_submitted": 0, "missing_text": 0}

    for iid, claim in sorted(claims.items()):
        uid = claim.get("uid")
        doc = subs.get(uid, {}).get(iid) if uid else None
        if not doc:
            counts["missing_text"] += 1
            continue
        if doc.get("status") != "submitted" and not include_drafts:
            counts["skipped_not_submitted"] += 1
            continue
        for field, variant in PAGE_FIELD_TO_VARIANT.items():
            text = (doc.get(field) or "").strip()
            if not text:
                continue
            path = variant_path(variants_dir, variant, iid)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text + "\n")
        provenance[iid] = {"writer": uid, "status": doc.get("status"), "updated_at": doc.get("updatedAt")}
        counts["written"] += 1

    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    return counts
