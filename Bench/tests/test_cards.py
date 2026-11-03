from dialect_tax.cards import Card, build_card, render_writer_sheet, split_problem_statement

ISSUE = """Title line here
Some prose explaining the bug.

```python
x = compute()
print(x)
```

More prose after the code.

Traceback (most recent call last):
  File "a.py", line 1, in <module>
    compute()
ValueError: boom

Final words.
"""


def test_split_extracts_fenced_and_traceback_blocks():
    prose, attachments = split_problem_statement(ISSUE)
    kinds = [a.kind for a in attachments]
    assert kinds == ["code", "traceback"]
    assert attachments[0].text.startswith("```python")
    assert attachments[0].text.endswith("```")
    assert attachments[1].text.splitlines()[-1] == "ValueError: boom"
    assert "[[A1]]" in prose and "[[A2]]" in prose
    assert "compute()" not in prose
    assert "Final words." in prose


def test_indented_block_becomes_attachment_unless_trivially_short():
    text = "Prose.\n\n    line one\n    line two\n\nTail prose.\n\n    single\n\nEnd."
    prose, attachments = split_problem_statement(text)
    assert len(attachments) == 1
    assert attachments[0].kind == "code"
    assert "single" in prose


def test_no_attachments_keeps_prose_intact():
    prose, attachments = split_problem_statement("Just prose, nothing else.")
    assert attachments == []
    assert prose == "Just prose, nothing else."


def test_trac_style_unindented_django_code_is_extracted():
    text = (
        "makemigrations produces incorrect path\nDescription\n\t\n"
        "To reproduce, create the following as your model:\n"
        "class Outer(object):\n\tclass Inner(models.CharField):\n\t\tpass\n"
        "class A(models.Model):\n\tfield = Outer.Inner(max_length=20)\n"
        "After running manage.py makemigrations, the file contains:\n"
        "migrations.CreateModel(\n\tname='A',\n),\n"
        "Note the test1.models.Inner, which should have been test1.models.Outer.Inner.\n"
    )
    prose, attachments = split_problem_statement(text)
    assert len(attachments) == 2
    assert attachments[0].text.startswith("class Outer(object):")
    assert attachments[0].text.endswith("max_length=20)")
    assert attachments[1].text.startswith("migrations.CreateModel(")
    assert "To reproduce, create the following" in prose
    assert "Note the test1.models.Inner" in prose


def test_doctest_session_and_unfenced_code_with_blank_lines():
    text = (
        "Title(x) is wrong\n    >>> from sympy import *\n    >>> e.subs(x, 2)\n    NameError: name 'cotm' is not defined\n\n"
        "Fails for 2, 3, 5.\n\nThe code:\n\nfrom sympy.combinatorics import DihedralGroup\n\nG = DihedralGroup(18)\n\nS2 = G.sylow_subgroup(p=2)\n \nThanks."
    )
    prose, attachments = split_problem_statement(text)
    assert len(attachments) == 2
    assert "NameError" in attachments[0].text
    assert attachments[1].text.splitlines()[-1] == "S2 = G.sylow_subgroup(p=2)"
    assert prose.startswith("Title(x) is wrong")
    assert "Fails for 2, 3, 5." in prose


def test_trac_metadata_line_stays_prose():
    text = "Title\nDescription\n\t \n\t\t(last modified by Someone)\n\t \nSome prose here."
    _, attachments = split_problem_statement(text)
    assert attachments == []


def test_images_details_and_duplicates():
    text = (
        "Title\nSee ![shot](https://x/y.png) here.\n<details><summary>Env</summary>\nversions\n</details>\n"
        "```python\nfoo()\n```\nAgain:\n```python\nfoo()\n```\n"
    )
    prose, attachments = split_problem_statement(text)
    assert [a.kind for a in attachments] == ["image", "details", "code"]
    assert prose.count("[[A3]]") == 2


def test_card_round_trip_and_sheet_excludes_english_prose():
    card = build_card({"instance_id": "x__y-1", "repo": "x/y", "problem_statement": ISSUE})
    card.units = ["Unit one", "Unit two"]
    clone = Card.from_json(card.to_json())
    assert clone == card
    sheet = render_writer_sheet(clone)
    assert "Unit two" in sheet
    assert "Some prose explaining the bug" not in sheet
    assert "[[A2]]" in sheet


def test_doctest_output_lines_stay_in_the_same_block():
    text = 'Title\n### Versions\n\n>>> import sys; print("Python", sys.version)\nPython 3.10.11 | conda-forge\n>>> import numpy; print(numpy.__version__)\n1.24.3\n\nEnd prose.'
    prose, attachments = split_problem_statement(text)
    assert len(attachments) == 1
    assert attachments[0].text.endswith("1.24.3")
    assert "End prose." in prose
