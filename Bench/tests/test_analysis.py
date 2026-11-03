import json

import numpy as np

from dialect_tax.analysis import Row, build_report, estimate_tax, load_rows, paired_bootstrap_ci, sign_flip_p_value


def make_rows(ref_solved: list[int], var_solved: list[int], model="m", ref="en", var="egy") -> list[Row]:
    rows = []
    for i, (a, b) in enumerate(zip(ref_solved, var_solved)):
        for variant, solved in ((ref, a), (var, b)):
            rows.append(Row(f"t{i}", model, variant, 1, "resolved" if solved else "unresolved", bool(solved), 0.1, 10, "Submitted"))
    return rows


def test_tax_is_paired_difference_in_pp():
    rows = make_rows([1, 1, 1, 0] * 10, [1, 0, 1, 0] * 10)
    est = estimate_tax(rows, "m", "egy", "en")
    assert est.n_tasks == 40
    assert abs(est.tax_pp - 25.0) < 1e-9
    assert est.ci_low_pp > 0
    assert est.p_value < 0.01


def test_no_difference_gives_zero_tax_and_p_one():
    rows = make_rows([1, 0] * 10, [1, 0] * 10)
    est = estimate_tax(rows, "m", "egy", "en")
    assert est.tax_pp == 0
    assert est.p_value == 1.0


def test_infra_errors_are_excluded():
    rows = make_rows([1, 1], [0, 0])
    rows.append(Row("t0", "m", "egy", 2, "eval_error", None, 0.0, 0, None))
    est = estimate_tax(rows, "m", "egy", "en")
    assert est.variant_rate == 0.0


def test_bootstrap_and_permutation_are_deterministic():
    diffs = np.array([0.0, 1.0, 0.0, 1.0, -1.0, 0.0, 1.0])
    assert paired_bootstrap_ci(diffs) == paired_bootstrap_ci(diffs)
    assert sign_flip_p_value(diffs) == sign_flip_p_value(diffs)


def test_mde_and_tasks_needed():
    rows = make_rows([1, 0, 1, 1, 0] * 10, [0, 0, 1, 1, 1] * 10)
    est = estimate_tax(rows, "m", "egy", "en")
    assert est.mde_pp() > 0
    assert est.tasks_needed(5.0) > est.tasks_needed(20.0)


def test_load_rows_and_report(tmp_path):
    for variant, resolved in (("en", True), ("egy", False)):
        d = tmp_path / "cells" / "m" / variant / "r1" / "t0"
        d.mkdir(parents=True)
        cell = {"instance_id": "t0", "model": "m", "variant": variant, "repeat": 1}
        (d / "eval.json").write_text(json.dumps({"cell": cell, "status": "resolved" if resolved else "unresolved", "resolved": resolved}))
        (d / "agent.json").write_text(json.dumps({"cell": cell, "cost": 0.5, "api_calls": 12, "exit_status": "Submitted"}))
    rows = load_rows(tmp_path)
    assert len(rows) == 2
    report = build_report(rows, "en", ["en", "egy"])
    assert "| egy | 1 | 0.0 | 100.0 |" in report
    assert "$1.00" in report
