"""Command-line entry point: `dialect-tax <command> --config configs/pilot.yaml`."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import typer

from dialect_tax.analysis import build_report, load_rows
from dialect_tax.cards import build_card, load_card, render_writer_sheet, save_card
from dialect_tax.config import ORIGINAL_VARIANT, load_config
from dialect_tax.tasks import load_instances, load_task_ids, save_tasks, select_pilot
from dialect_tax.variants import validate_variant

app = typer.Typer(add_completion=False, help="Dialect Tax benchmark tooling.")
CONFIG = typer.Option("configs/pilot.yaml", "--config", "-c", help="Experiment YAML.")


def _setup_logging(verbose: bool = False) -> None:
    os.environ.setdefault("MSWEA_SILENT_STARTUP", "1")
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def _csv(value: str | None, default: list[str]) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()] if value else default


@app.command("select-tasks")
def select_tasks(config: str = CONFIG, n: int = 50, seed: int = 20261103, min_prose: int = 300, max_total: int = 3500):
    """Pick the pilot subset from SWE-bench Verified (stratified by repo)."""
    cfg = load_config(config)
    instances = load_instances(cfg.dataset, cfg.split)
    chosen = select_pilot(instances, n=n, seed=seed, min_prose=min_prose, max_total=max_total)
    meta = {"dataset": cfg.dataset, "split": cfg.split, "n": n, "seed": seed, "min_prose": min_prose, "max_total": max_total}
    save_tasks(cfg.tasks_path, chosen, meta)
    repos: dict[str, int] = {}
    for t in chosen:
        repos[t["repo"]] = repos.get(t["repo"], 0) + 1
    typer.echo(f"Wrote {len(chosen)} tasks to {cfg.tasks_path}")
    typer.echo(json.dumps(repos, indent=2))


@app.command("make-cards")
def make_cards(config: str = CONFIG):
    """Create card skeletons (prose split from verbatim attachments). Keeps existing units."""
    cfg = load_config(config)
    instances = load_instances(cfg.dataset, cfg.split)
    for iid in load_task_ids(cfg.tasks_path):
        save_card(cfg.cards_path, build_card(instances[iid]))
    typer.echo(f"Cards in {cfg.cards_path}")


@app.command("sheets")
def sheets(config: str = CONFIG, out: str = "data/writer_sheets"):
    """Render the writer sheets (units + attachments, no English prose)."""
    cfg = load_config(config)
    out_dir = cfg.resolve(Path(out))
    out_dir.mkdir(parents=True, exist_ok=True)
    missing_units = 0
    for iid in load_task_ids(cfg.tasks_path):
        card = load_card(cfg.cards_path, iid)
        missing_units += not card.units
        (out_dir / f"{iid}.md").write_text(render_writer_sheet(card))
    typer.echo(f"Sheets in {out_dir} ({missing_units} cards still without units)")


@app.command("validate")
def validate(config: str = CONFIG, variants: str = typer.Option(None, help="Comma-separated; default: all non-orig variants")):
    """Check every variant file: exists, right script, placeholders valid."""
    cfg = load_config(config)
    wanted = _csv(variants, [v for v in cfg.variants if v != ORIGINAL_VARIANT])
    task_ids = load_task_ids(cfg.tasks_path)
    failures = 0
    for variant in wanted:
        ok = 0
        for iid in task_ids:
            result = validate_variant(variant, load_card(cfg.cards_path, iid), cfg.variants_path)
            if result.ok:
                ok += 1
            else:
                failures += 1
            for e in result.errors:
                typer.echo(f"ERROR {variant}/{iid}: {e}")
            for w in result.warnings:
                typer.echo(f"warn  {variant}/{iid}: {w}")
        typer.echo(f"{variant}: {ok}/{len(task_ids)} valid")
    raise typer.Exit(code=1 if failures else 0)


@app.command("run")
def run(
    config: str = CONFIG,
    models: str = typer.Option(None, help="Comma-separated model names from the config, or 'gold'/'empty' for a keyless dry run"),
    variants: str = typer.Option(None, help="Comma-separated variants (default: config)"),
    limit: int = typer.Option(0, help="Only the first N tasks (0 = all)"),
    tasks: str = typer.Option(None, help="Comma-separated instance ids (overrides --limit)"),
    repeats: int = typer.Option(0, help="Repeats per cell (0 = config)"),
    workers: int = typer.Option(0, help="Parallel cells per task (0 = config)"),
    output: str = typer.Option(None, help="Override output dir"),
    redo: bool = typer.Option(False, help="Ignore existing results"),
    verbose: bool = False,
):
    """Run agents and grade them. Resumable: finished cells are skipped."""
    _setup_logging(verbose)
    from dialect_tax.runner import DRY_RUN_MODELS, run_experiment

    cfg = load_config(config)
    if output:
        cfg.output_dir = Path(output)
    model_names = _csv(models, [m.name for m in cfg.models])
    real_models = [m for m in model_names if m not in DRY_RUN_MODELS]
    for m in real_models:
        cfg.model(m)
    if real_models and not os.getenv("OPENROUTER_API_KEY") and any(cfg.model(m).model_class.startswith("openrouter") for m in real_models):
        raise typer.BadParameter("OPENROUTER_API_KEY is not set")

    task_ids = _csv(tasks, load_task_ids(cfg.tasks_path))
    if limit and not tasks:
        task_ids = task_ids[:limit]
    instances = load_instances(cfg.dataset, cfg.split)

    def report_progress(cell, outcome):
        typer.echo(f"{cell.instance_id} {cell.model} {cell.variant} r{cell.repeat}: {outcome.get('status')}")

    run_experiment(
        cfg,
        instances,
        task_ids,
        models=model_names,
        variants=_csv(variants, cfg.variants),
        repeats=repeats or cfg.runs_per_cell,
        workers=workers or cfg.workers,
        redo=redo,
        on_cell_done=report_progress,
    )
    report_path = cfg.output_path / "report.md"
    report_path.write_text(build_report(load_rows(cfg.output_path), cfg.reference_variant, cfg.variants))
    typer.echo(f"Report: {report_path}")


@app.command("report")
def report(config: str = CONFIG, output: str = typer.Option(None), reference: str = typer.Option(None)):
    """Rebuild the markdown report from finished cells."""
    cfg = load_config(config)
    if output:
        cfg.output_dir = Path(output)
    text = build_report(load_rows(cfg.output_path), reference or cfg.reference_variant, cfg.variants)
    path = cfg.output_path / "report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    typer.echo(text)


@app.command("estimate-cost")
def estimate_cost(config: str = CONFIG, output: str = typer.Option(None), tasks: int = 50, repeats: int = 0):
    """Extrapolate full-pilot cost per model from cells finished so far."""
    cfg = load_config(config)
    if output:
        cfg.output_dir = Path(output)
    rows = load_rows(cfg.output_path)
    repeats = repeats or cfg.runs_per_cell
    cells_per_model = tasks * len(cfg.variants) * repeats
    total = 0.0
    for model in sorted({r.model for r in rows}):
        costs = [r.cost for r in rows if r.model == model]
        avg = sum(costs) / len(costs)
        total += avg * cells_per_model
        typer.echo(f"{model}: ${avg:.3f}/run from {len(costs)} runs -> ${avg * cells_per_model:,.0f} for {cells_per_model} runs")
    typer.echo(f"Total: ${total:,.0f}")


@app.command("build-writer-page")
def build_writer_page(config: str = CONFIG, template: str = "web/WriterApp.template.html", out: str = "web/WriterApp.html"):
    """Embed the cards (without English prose) into the writers' web page."""
    from dialect_tax.writer_page import build_page

    cfg = load_config(config)
    path = build_page(cfg.resolve(Path(template)), cfg.cards_path, load_task_ids(cfg.tasks_path), cfg.resolve(Path(out)))
    typer.echo(f"Wrote {path} ({path.stat().st_size:,} bytes)")


@app.command("import-submissions")
def import_submissions_cmd(dump: str, config: str = CONFIG, include_drafts: bool = False):
    """Write writers' submitted texts into data/variants/. DUMP is a JSON file or an exported store directory."""
    from dialect_tax.writer_page import dump_from_directory, import_submissions

    cfg = load_config(config)
    source = Path(dump)
    data = dump_from_directory(source) if source.is_dir() else json.loads(source.read_text())
    counts = import_submissions(data, cfg.variants_path, include_drafts=include_drafts)
    typer.echo(json.dumps(counts))


if __name__ == "__main__":
    app()
