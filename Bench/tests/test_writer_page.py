import json

from dialect_tax.cards import Attachment, Card, save_card
from dialect_tax.writer_page import build_page, import_submissions


def make_card(tmp_path, iid="a__b-1"):
    card = Card(
        instance_id=iid,
        repo="a/b",
        title="SECRET ENGLISH TITLE",
        units=["unit one [[A1]]"],
        attachments=[Attachment(1, "code", "```python\nprint('</script>')\n```")],
        original_prose="SECRET ENGLISH PROSE [[A1]]",
    )
    save_card(tmp_path / "cards", card)
    return card


def test_page_excludes_english_prose_and_escapes_script_end(tmp_path):
    make_card(tmp_path)
    template = tmp_path / "t.html"
    template.write_text('<script type="application/json" id="cards">/*__CARDS__*/</script>')
    out = build_page(template, tmp_path / "cards", ["a__b-1"], tmp_path / "out.html")
    html = out.read_text()
    assert "SECRET ENGLISH" not in html
    assert html.count("</script>") == 1
    payload = html.split('id="cards">', 1)[1].rsplit("</script>", 1)[0]
    assert json.loads(payload)[0]["units"] == ["unit one [[A1]]"]


def test_dump_from_exported_directory(tmp_path):
    from dialect_tax.writer_page import dump_from_directory

    (tmp_path / "claims").mkdir()
    (tmp_path / "claims" / "a__b-1.json").write_text(json.dumps({"id": "a__b-1", "data": {"uid": "u_1", "status": "submitted"}, "version": 3}))
    tasks = tmp_path / "subs" / "u_1" / "tasks"
    tasks.mkdir(parents=True)
    (tasks / "a__b-1.json").write_text(json.dumps({"en": "hi there", "status": "submitted"}))
    dump = dump_from_directory(tmp_path)
    assert dump["claims"]["a__b-1"]["uid"] == "u_1"
    assert dump["subs"]["u_1"]["a__b-1"]["en"] == "hi there"


def test_import_writes_only_submitted_canonical_texts(tmp_path):
    dump = {
        "claims": {
            "a__b-1": {"uid": "u_1", "status": "submitted"},
            "a__b-2": {"uid": "u_2", "status": "claimed"},
        },
        "subs": {
            "u_1": {"a__b-1": {"en": "When I run it", "egy": "لما بشغله", "franco": "lama bashaghalo", "status": "submitted", "updatedAt": 1}},
            "u_2": {"a__b-2": {"en": "draft", "egy": "", "franco": "", "status": "draft", "updatedAt": 2}},
            "u_3": {"a__b-1": {"en": "not the claimer", "status": "submitted"}},
        },
    }
    counts = import_submissions(dump, tmp_path)
    assert counts == {"written": 1, "skipped_not_submitted": 1, "skipped_not_accepted": 0, "missing_text": 0}
    assert (tmp_path / "egy-franco" / "a__b-1.md").read_text() == "lama bashaghalo\n"
    assert (tmp_path / "en" / "a__b-1.md").read_text() == "When I run it\n"
    assert not (tmp_path / "en" / "a__b-2.md").exists()
    assert json.loads((tmp_path / "provenance.json").read_text())["a__b-1"]["writer"] == "u_1"


def test_accepted_only_uses_review_and_records_it(tmp_path):
    dump = {
        "claims": {
            "a__b-1": {"uid": "u_1", "status": "submitted", "review": {"status": "accepted", "by": "u_9"}},
            "a__b-2": {"uid": "u_1", "status": "submitted", "review": {"status": "changes", "by": "u_9"}},
            "a__b-3": {"uid": "u_1", "status": "submitted"},
        },
        "subs": {"u_1": {k: {"en": "text " + k, "status": "submitted"} for k in ("a__b-1", "a__b-2", "a__b-3")}},
        "reviews": {"u_9": {"a__b-1": {"verdict": "accepted", "notes": "good"}}},
    }
    counts = import_submissions(dump, tmp_path, accepted_only=True)
    assert counts["written"] == 1 and counts["skipped_not_accepted"] == 2
    prov = json.loads((tmp_path / "provenance.json").read_text())
    assert prov["a__b-1"]["review"]["detail"]["notes"] == "good"
