"""Run agents on every (task x model x variant x repeat) cell, then grade each patch.

Execution is task-major: pull one task image, run all of its cells in parallel,
grade them, then remove the image. This keeps disk usage at roughly one image
per in-flight task (SWE-bench images are 1-4 GB each).
"""

from __future__ import annotations

import base64
import concurrent.futures
import contextlib
import json
import logging
import signal
import subprocess
import threading
import time
import traceback
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

from dialect_tax.cards import load_card
from dialect_tax.config import ExperimentConfig, ModelSpec
from dialect_tax.evaluate import evaluate_patch, safe_run_id
from dialect_tax.variants import problem_statement

log = logging.getLogger("dialect_tax.runner")

DRY_RUN_MODELS = {"gold", "empty"}


@dataclass(frozen=True)
class Cell:
    instance_id: str
    model: str
    variant: str
    repeat: int

    def directory(self, output: Path) -> Path:
        return output / "cells" / self.model / self.variant / f"r{self.repeat}" / self.instance_id

    @property
    def run_id(self) -> str:
        return safe_run_id(self.model, self.variant, f"r{self.repeat}")


def _base_swebench_config() -> dict:
    from minisweagent.config import builtin_config_dir

    return yaml.safe_load((builtin_config_dir / "benchmarks" / "swebench.yaml").read_text())


def _dry_run_model(kind: str, instance: dict):
    from minisweagent.models.test_models import DeterministicModel, make_output

    if kind == "gold":
        encoded = base64.b64encode(instance["patch"].encode()).decode()
        work = f"cd /testbed && echo {encoded} | base64 -d > /tmp/gold.patch && git apply /tmp/gold.patch && git diff > patch.txt"
    else:
        work = "cd /testbed && git diff > patch.txt"
    outputs = [
        make_output("apply", [{"command": work}], cost=0.0),
        make_output("submit", [{"command": "cd /testbed && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt"}], cost=0.0),
    ]
    return DeterministicModel(outputs=outputs, model_name=f"dry-run-{kind}", cost_per_call=0.0)


def _make_model(spec: ModelSpec, base: dict, instance: dict):
    if spec.name in DRY_RUN_MODELS:
        return _dry_run_model(spec.name, instance)
    from minisweagent.models import get_model

    model_config = {**base.get("model", {})}
    model_config.pop("model_name", None)
    model_kwargs = {**model_config.get("model_kwargs", {}), **spec.model_kwargs}
    if spec.model_class.startswith("openrouter"):
        model_kwargs.pop("drop_params", None)
    model_config["model_kwargs"] = model_kwargs
    model_config["model_class"] = spec.model_class
    return get_model(spec.model_name, config=model_config)


def run_agent(cell: Cell, cfg: ExperimentConfig, instance: dict, task_text: str) -> dict:
    """Run one agent episode. Returns the result record (also written to disk)."""
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.environments import get_environment

    base = _base_swebench_config()
    spec = cfg.model(cell.model) if cell.model not in DRY_RUN_MODELS else ModelSpec(cell.model, cell.model)
    out_dir = cell.directory(cfg.output_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    env_config = {**base["environment"], "image": cfg.image_for(cell.instance_id), "timeout": cfg.command_timeout_seconds}
    agent_config = {
        **base["agent"],
        "step_limit": cfg.agent_step_limit,
        "cost_limit": cfg.agent_cost_limit,
        "wall_time_limit_seconds": cfg.agent_wall_time_seconds,
    }

    started = time.time()
    env = agent = None
    record = {"exit_status": None, "patch": "", "cost": 0.0, "api_calls": 0}
    try:
        model = _make_model(spec, base, instance)
        env = get_environment(env_config)
        agent = DefaultAgent(model, env, **agent_config)
        info = agent.run(task_text)
        record["exit_status"] = info.get("exit_status")
        record["patch"] = info.get("submission") or ""
    except Exception as exc:
        record["exit_status"] = type(exc).__name__
        record["error"] = str(exc)
        record["traceback"] = traceback.format_exc()
        log.error("Agent failed on %s: %s", cell, exc)
    finally:
        if agent is not None:
            record["cost"] = agent.cost
            record["api_calls"] = agent.n_calls
            agent.save(out_dir / "trajectory.json")
        if env is not None:
            env.cleanup()
    record["duration_seconds"] = round(time.time() - started, 1)
    (out_dir / "agent.json").write_text(json.dumps({"cell": asdict(cell), **record}, indent=2))
    return record


def grade(cell: Cell, cfg: ExperimentConfig, instance: dict, patch: str) -> dict:
    out_dir = cell.directory(cfg.output_path)
    result = evaluate_patch(
        instance,
        patch,
        image=cfg.image_for(cell.instance_id),
        run_id=cell.run_id,
        model_name=cell.model,
        log_dir=cfg.output_path / "eval_logs",
        timeout=cfg.eval_timeout_seconds,
    )
    (out_dir / "eval.json").write_text(json.dumps({"cell": asdict(cell), **result}, indent=2))
    return result


def process_cell(cell: Cell, cfg: ExperimentConfig, instance: dict, task_text: str, *, redo: bool = False) -> dict:
    out_dir = cell.directory(cfg.output_path)
    agent_file, eval_file = out_dir / "agent.json", out_dir / "eval.json"
    if redo:
        agent_file.unlink(missing_ok=True)
        eval_file.unlink(missing_ok=True)

    if agent_file.exists():
        record = json.loads(agent_file.read_text())
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "task.md").write_text(task_text)
        record = run_agent(cell, cfg, instance, task_text)

    if eval_file.exists():
        evaluation = json.loads(eval_file.read_text())
        if evaluation.get("status") != "eval_error":
            return evaluation
    if record.get("error") and not record.get("patch"):
        evaluation = {"status": "agent_error", "resolved": None}
        (out_dir / "eval.json").write_text(json.dumps({"cell": asdict(cell), **evaluation}, indent=2))
        return evaluation
    return grade(cell, cfg, instance, record.get("patch", ""))


def _docker(*args: str, timeout: int = 1800) -> subprocess.CompletedProcess:
    return subprocess.run(["docker", *args], capture_output=True, text=True, timeout=timeout)


def ensure_image(image: str, retries: int = 3) -> None:
    if _docker("image", "inspect", image, timeout=60).returncode == 0:
        return
    for attempt in range(1, retries + 1):
        result = _docker("pull", image)
        if result.returncode == 0:
            return
        log.warning("Pull failed (%d/%d) for %s: %s", attempt, retries, image, result.stderr.strip()[-300:])
        time.sleep(10 * attempt)
    raise RuntimeError(f"Could not pull {image}")


def remove_image(image: str) -> None:
    _docker("image", "rm", "-f", image, timeout=300)


def image_prefix(cfg: ExperimentConfig) -> str:
    return cfg.image_template.split("{instance_id}")[0]


def prune_stale_images(cfg: ExperimentConfig, keep: set[str]) -> list[str]:
    """Remove task images left behind by crashed or killed runs.

    Uses ``docker image rm`` without ``-f`` so an image still used by a container
    (for example by another runner process on the same machine) is left alone.
    """
    listing = _docker("images", "--format", "{{.Repository}}:{{.Tag}}", timeout=120)
    if listing.returncode != 0:
        return []
    prefix = image_prefix(cfg)
    stale = [name for name in listing.stdout.split() if name.startswith(prefix) and name not in keep]
    removed = [name for name in stale if _docker("image", "rm", name, timeout=300).returncode == 0]
    if removed:
        log.info("Removed %d stale task image(s)", len(removed))
    return removed


@contextlib.contextmanager
def _sigterm_as_interrupt():
    """Turn SIGTERM into KeyboardInterrupt so `finally` blocks (image cleanup) run on `kill`."""
    if threading.current_thread() is not threading.main_thread():
        yield
        return

    def handler(signum, frame):
        raise KeyboardInterrupt(f"signal {signum}")

    previous = signal.signal(signal.SIGTERM, handler)
    try:
        yield
    finally:
        signal.signal(signal.SIGTERM, previous)


def plan_cells(cfg: ExperimentConfig, instance_ids: list[str], models: list[str], variants: list[str], repeats: int) -> dict[str, list[Cell]]:
    return {
        iid: [Cell(iid, m, v, r) for m in models for v in variants for r in range(1, repeats + 1)]
        for iid in instance_ids
    }


def cell_is_done(cell: Cell, cfg: ExperimentConfig) -> bool:
    eval_file = cell.directory(cfg.output_path) / "eval.json"
    if not eval_file.exists():
        return False
    return json.loads(eval_file.read_text()).get("status") not in {"eval_error", "agent_error"}


def run_experiment(
    cfg: ExperimentConfig,
    instances: dict[str, dict],
    instance_ids: list[str],
    *,
    models: list[str],
    variants: list[str],
    repeats: int,
    workers: int,
    redo: bool = False,
    on_cell_done=None,
) -> list[tuple[Cell, dict]]:
    plan = plan_cells(cfg, instance_ids, models, variants, repeats)
    results: list[tuple[Cell, dict]] = []
    with _sigterm_as_interrupt():
        _run_plan(cfg, instances, plan, results, workers=workers, redo=redo, on_cell_done=on_cell_done)
    return results


def _run_plan(cfg, instances, plan, results, *, workers, redo, on_cell_done) -> None:
    pruned = not cfg.cleanup_images
    for index, (iid, cells) in enumerate(plan.items(), start=1):
        todo = [c for c in cells if redo or not cell_is_done(c, cfg)]
        log.info("[%d/%d] %s: %d/%d cells to run", index, len(plan), iid, len(todo), len(cells))
        if not todo:
            continue
        instance = instances[iid]
        card = None
        if any(c.variant != "orig" for c in todo):
            card = load_card(cfg.cards_path, iid)
        texts = {v: problem_statement(v, instance, card, cfg.variants_path) for v in {c.variant for c in todo}}

        image = cfg.image_for(iid)
        if not pruned:
            prune_stale_images(cfg, keep={image})
            pruned = True
        try:
            ensure_image(image)
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {pool.submit(process_cell, c, cfg, instance, texts[c.variant], redo=redo): c for c in todo}
                for future in concurrent.futures.as_completed(futures):
                    cell = futures[future]
                    try:
                        outcome = future.result()
                    except Exception as exc:
                        log.error("Cell crashed %s: %s", cell, exc, exc_info=True)
                        outcome = {"status": "crash", "resolved": None, "error": str(exc)}
                    results.append((cell, outcome))
                    if on_cell_done:
                        on_cell_done(cell, outcome)
        finally:
            if cfg.cleanup_images:
                remove_image(image)
