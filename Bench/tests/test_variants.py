import pytest

from dialect_tax.cards import Attachment, Card
from dialect_tax.variants import arabic_ratio, assemble, problem_statement, validate_variant, variant_path


@pytest.fixture
def card():
    return Card(
        instance_id="repo__proj-1",
        repo="repo/proj",
        title="t",
        attachments=[
            Attachment(1, "code", "```python\nfoo(1)\n```"),
            Attachment(2, "traceback", "Traceback (most recent call last):\nValueError: x"),
        ],
    )


def write(tmp_path, variant, text, iid="repo__proj-1"):
    path = variant_path(tmp_path, variant, iid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_assemble_substitutes_and_appends_unreferenced(card):
    out = assemble("الكود ده [[A1]] بيضرب", card)
    assert "foo(1)" in out
    assert out.rstrip().endswith("ValueError: x")


def test_assemble_rejects_unknown_placeholder(card):
    with pytest.raises(ValueError):
        assemble("see [[A9]]", card)


def test_orig_variant_returns_dataset_text(card, tmp_path):
    inst = {"instance_id": card.instance_id, "problem_statement": "ORIGINAL"}
    assert problem_statement("orig", inst, None, tmp_path) == "ORIGINAL"


def test_validate_flags_wrong_script(card, tmp_path):
    write(tmp_path, "egy", "This is written in English only, which is wrong for egy [[A1]] [[A2]]")
    result = validate_variant("egy", card, tmp_path)
    assert not result.ok
    assert any("Arabic" in e for e in result.errors)


def test_validate_accepts_code_switched_egyptian(card, tmp_path):
    write(tmp_path, "egy", "لما بشغّل الـ function دي [[A1]] بيطلعلي الـ error ده [[A2]] والمفروض يرجّع القيمة عادي من غير exception")
    result = validate_variant("egy", card, tmp_path)
    assert result.ok, result.errors


def test_validate_franco_must_be_latin(card, tmp_path):
    write(tmp_path, "egy-franco", "lama bashaghal el function di [[A1]] bytla3li el error da [[A2]] w el mafrood yerga3 3adi")
    assert validate_variant("egy-franco", card, tmp_path).ok


def test_validate_warns_on_missing_placeholder(card, tmp_path):
    write(tmp_path, "en", "When I run this function [[A1]] it crashes instead of returning the value normally.")
    result = validate_variant("en", card, tmp_path)
    assert result.ok
    assert any("not referenced" in w for w in result.warnings)


def test_arabic_ratio_ignores_inline_code():
    assert arabic_ratio("الـ `some_long_identifier_name()` بيضرب") == 1.0


def test_heavily_code_switched_egyptian_passes(card, tmp_path):
    write(tmp_path, "egy", "صفحة الـ debug لسه بتعرض الـ RuntimeError حتى مع raise ValueError from None، الـ view ده [[A1]] والسبب [[A2]]")
    assert validate_variant("egy", card, tmp_path).ok


def test_blind_variant_returns_text_verbatim_without_attachments(card, tmp_path):
    text = "There is a bug in this repository. Find it and fix it.\n"
    path = variant_path(tmp_path, "blind-synth", card.instance_id)
    path.parent.mkdir(parents=True)
    path.write_text(text)
    inst = {"instance_id": card.instance_id, "problem_statement": "ORIGINAL"}
    assert problem_statement("blind-synth", inst, card, tmp_path) == text
    assert card.attachments  # the fixture has attachments, and none were appended
