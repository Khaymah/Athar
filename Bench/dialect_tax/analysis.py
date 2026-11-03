"""Paired analysis of resolve rates: dialect tax with bootstrap CIs and permutation p-values.

Unit of analysis is the task. For each task we average the repeats of a cell,
then compare variants on the same task (paired design), so task difficulty
cancels out.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from dialect_tax.evaluate import COUNTED_STATUSES

Z_POWER_80_ALPHA_05 = 2.8


@dataclass
class Row:
    instance_id: str
    model: str
    variant: str
    repeat: int
    status: str
    resolved: bool | None
    cost: float
    api_calls: int
    exit_status: str | None


@dataclass
class TaxEstimate:
    model: str
    variant: str
    reference: str
    n_tasks: int
    reference_rate: float
    variant_rate: float
    tax_pp: float
    ci_low_pp: float
    ci_high_pp: float
    p_value: float
    diff_sd_pp: float

    @property
    def relative_tax(self) -> float:
        return self.tax_pp / self.reference_rate if self.reference_rate else float("nan")

    def mde_pp(self) -> float:
        """Minimum detectable effect (80% power, alpha 0.05) at the current task count."""
        return Z_POWER_80_ALPHA_05 * self.diff_sd_pp / math.sqrt(self.n_tasks) if self.n_tasks else float("nan")

    def tasks_needed(self, effect_pp: float) -> int:
        if effect_pp <= 0 or self.diff_sd_pp == 0:
            return 0
        return math.ceil((Z_POWER_80_ALPHA_05 * self.diff_sd_pp / effect_pp) ** 2)


def load_rows(output_dir: Path) -> list[Row]:
    rows: list[Row] = []
    for eval_file in sorted((output_dir / "cells").glob("*/*/r*/*/eval.json")):
        evaluation = json.loads(eval_file.read_text())
        agent_file = eval_file.with_name("agent.json")
        agent = json.loads(agent_file.read_text()) if agent_file.exists() else {}
        cell = evaluation["cell"]
        rows.append(
            Row(
                instance_id=cell["instance_id"],
                model=cell["model"],
                variant=cell["variant"],
                repeat=cell["repeat"],
                status=evaluation.get("status", ""),
                resolved=evaluation.get("resolved"),
                cost=float(agent.get("cost", 0.0) or 0.0),
                api_calls=int(agent.get("api_calls", 0) or 0),
                exit_status=agent.get("exit_status"),
            )
        )
    return rows


def per_task_rates(rows: list[Row], model: str, variant: str) -> dict[str, float]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        if r.model == model and r.variant == variant and r.status in COUNTED_STATUSES:
            buckets[r.instance_id].append(1.0 if r.resolved else 0.0)
    return {iid: float(np.mean(v)) for iid, v in buckets.items() if v}


def paired_bootstrap_ci(diffs: np.ndarray, *, iterations: int = 10_000, seed: int = 0) -> tuple[float, float]:
    if len(diffs) == 0:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    samples = rng.choice(diffs, size=(iterations, len(diffs)), replace=True).mean(axis=1)
    return float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))


def sign_flip_p_value(diffs: np.ndarray, *, iterations: int = 20_000, seed: int = 1) -> float:
    """Two-sided paired permutation test of mean difference == 0."""
    nonzero = diffs[diffs != 0]
    if len(nonzero) == 0:
        return 1.0
    observed = abs(nonzero.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice([-1.0, 1.0], size=(iterations, len(nonzero)))
    null = np.abs((signs * nonzero).mean(axis=1))
    return float((np.sum(null >= observed - 1e-12) + 1) / (iterations + 1))


def estimate_tax(rows: list[Row], model: str, variant: str, reference: str) -> TaxEstimate:
    ref = per_task_rates(rows, model, reference)
    var = per_task_rates(rows, model, variant)
    shared = sorted(set(ref) & set(var))
    diffs = np.array([ref[t] - var[t] for t in shared], dtype=float)
    low, high = paired_bootstrap_ci(diffs)
    return TaxEstimate(
        model=model,
        variant=variant,
        reference=reference,
        n_tasks=len(shared),
        reference_rate=float(np.mean([ref[t] for t in shared])) if shared else float("nan"),
        variant_rate=float(np.mean([var[t] for t in shared])) if shared else float("nan"),
        tax_pp=float(diffs.mean() * 100) if len(diffs) else float("nan"),
        ci_low_pp=low * 100,
        ci_high_pp=high * 100,
        p_value=sign_flip_p_value(diffs) if len(diffs) else float("nan"),
        diff_sd_pp=float(diffs.std(ddof=1) * 100) if len(diffs) > 1 else 0.0,
    )


def _fmt(x: float, digits: int = 1) -> str:
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{digits}f}"


def build_report(rows: list[Row], reference: str, variants_order: list[str] | None = None) -> str:
    if not rows:
        return "# Dialect Tax report\n\nNo results yet.\n"
    models = sorted({r.model for r in rows})
    variants = variants_order or sorted({r.variant for r in rows})
    lines = ["# Dialect Tax report", "", f"Reference variant: `{reference}`. Tax = reference resolve rate minus variant resolve rate, in percentage points (pp), paired by task.", ""]

    for model in models:
        model_rows = [r for r in rows if r.model == model]
        lines += [f"## {model}", "", "| Variant | Tasks | Resolve % | Tax (pp) | 95% CI | p | MDE (pp) | Cost/run $ | Steps/run |", "|---|---|---|---|---|---|---|---|---|"]
        for variant in variants:
            vrows = [r for r in model_rows if r.variant == variant]
            if not vrows:
                continue
            rate = per_task_rates(rows, model, variant)
            cost = np.mean([r.cost for r in vrows]) if vrows else float("nan")
            steps = np.mean([r.api_calls for r in vrows]) if vrows else float("nan")
            if variant == reference or not per_task_rates(rows, model, reference):
                lines.append(f"| **{variant}** | {len(rate)} | {_fmt(np.mean(list(rate.values())) * 100 if rate else float('nan'))} | — | — | — | — | {_fmt(cost, 3)} | {_fmt(steps)} |")
                continue
            est = estimate_tax(rows, model, variant, reference)
            lines.append(
                f"| {variant} | {est.n_tasks} | {_fmt(est.variant_rate * 100)} | {_fmt(est.tax_pp)} | "
                f"[{_fmt(est.ci_low_pp)}, {_fmt(est.ci_high_pp)}] | {_fmt(est.p_value, 3)} | {_fmt(est.mde_pp())} | {_fmt(cost, 3)} | {_fmt(steps)} |"
            )
        excluded = [r for r in model_rows if r.status not in COUNTED_STATUSES]
        if excluded:
            by_status: dict[str, int] = defaultdict(int)
            for r in excluded:
                by_status[r.status] += 1
            lines += ["", f"Excluded (infrastructure) cells: {dict(by_status)}. Re-run them before drawing conclusions."]
        lines.append("")

    total_cost = sum(r.cost for r in rows)
    lines += ["## Cost", "", f"Total agent cost so far: ${total_cost:.2f} over {len(rows)} cells (${total_cost / len(rows):.3f}/cell).", ""]
    lines += [
        "## How to read this",
        "",
        "- **Tax > 0** means the agent solves fewer tasks in that variant than in the reference.",
        "- The **95% CI** comes from a paired bootstrap over tasks. If it includes 0, the pilot cannot distinguish the tax from noise.",
        "- **MDE** is the smallest tax this many tasks can reliably detect (80% power). Use it to size the next round.",
        "",
    ]
    return "\n".join(lines)
