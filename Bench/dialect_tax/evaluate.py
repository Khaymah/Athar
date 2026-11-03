"""Grade a model patch with the official SWE-bench harness (hidden tests in Docker)."""

from __future__ import annotations

import re
import threading
from pathlib import Path

_PATCH_LOCK = threading.Lock()
_CONFIGURED_DIR: Path | None = None

STATUS_RESOLVED = "resolved"
STATUS_UNRESOLVED = "unresolved"
STATUS_EMPTY_PATCH = "empty_patch"
STATUS_PATCH_APPLY_FAILED = "patch_apply_failed"
STATUS_EVAL_ERROR = "eval_error"

COUNTED_STATUSES = {STATUS_RESOLVED, STATUS_UNRESOLVED, STATUS_EMPTY_PATCH, STATUS_PATCH_APPLY_FAILED}


def _configure_log_dir(log_dir: Path) -> None:
    """swebench writes logs under a module-level constant; point it at our run directory once."""
    global _CONFIGURED_DIR
    with _PATCH_LOCK:
        if _CONFIGURED_DIR == log_dir:
            return
        import swebench.harness.run_evaluation as run_evaluation

        run_evaluation.RUN_EVALUATION_LOG_DIR = log_dir
        _CONFIGURED_DIR = log_dir


def safe_run_id(*parts: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "-", ".".join(parts)).lower()


def evaluate_patch(
    instance: dict,
    patch: str,
    *,
    image: str,
    run_id: str,
    model_name: str,
    log_dir: Path,
    timeout: int,
) -> dict:
    """Return {"status": ..., "resolved": bool | None}. ``resolved`` is None for infra errors."""
    if not (patch or "").strip():
        return {"status": STATUS_EMPTY_PATCH, "resolved": False}

    import docker
    from swebench.harness.constants import APPLY_PATCH_FAIL, LOG_INSTANCE
    from swebench.harness.run_evaluation import run_instance
    from swebench.harness.utils import make_test_spec

    _configure_log_dir(log_dir)
    spec = make_test_spec({**instance, "image": image})
    prediction = {"instance_id": instance["instance_id"], "model_name_or_path": model_name, "model_patch": patch}
    client = docker.from_env(timeout=600)
    try:
        outcome = run_instance(spec, prediction, client, run_id, timeout=timeout)
    finally:
        client.close()

    if outcome:
        _, report = outcome
        resolved = bool(report[instance["instance_id"]]["resolved"])
        return {"status": STATUS_RESOLVED if resolved else STATUS_UNRESOLVED, "resolved": resolved}

    instance_log = log_dir / run_id / model_name.replace("/", "__") / instance["instance_id"] / LOG_INSTANCE
    log_text = instance_log.read_text(errors="replace") if instance_log.exists() else ""
    if APPLY_PATCH_FAIL in log_text:
        return {"status": STATUS_PATCH_APPLY_FAILED, "resolved": False}
    return {"status": STATUS_EVAL_ERROR, "resolved": None, "log": str(instance_log)}
