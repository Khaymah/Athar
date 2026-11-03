import os
import signal
import subprocess
from pathlib import Path

import pytest

from dialect_tax import runner
from dialect_tax.config import ExperimentConfig

PREFIX = "ghcr.io/epoch-research/swe-bench.eval.x86_64."


@pytest.fixture
def docker_calls(monkeypatch):
    calls = []
    images = [f"{PREFIX}a__a-1:latest", f"{PREFIX}b__b-2:latest", "python:3.11", f"{PREFIX}busy__c-3:latest"]

    def fake_docker(*args, timeout=0):
        calls.append(args)
        if args[0] == "images":
            return subprocess.CompletedProcess(args, 0, stdout="\n".join(images) + "\n", stderr="")
        if args[:2] == ("image", "rm") and "busy" in args[-1]:
            return subprocess.CompletedProcess(args, 1, stdout="", stderr="image is being used")
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(runner, "_docker", fake_docker)
    return calls


def test_prune_removes_only_stale_task_images(docker_calls):
    cfg = ExperimentConfig(name="t", root=Path("."))
    removed = runner.prune_stale_images(cfg, keep={f"{PREFIX}a__a-1:latest"})
    assert removed == [f"{PREFIX}b__b-2:latest"]
    rm_calls = [c for c in docker_calls if c[:2] == ("image", "rm")]
    assert all("-f" not in c for c in rm_calls)  # never force: images in use are left alone
    assert ("image", "rm", "python:3.11") not in rm_calls


def test_run_experiment_cleans_up_image_on_sigterm(docker_calls, monkeypatch, tmp_path):
    cfg = ExperimentConfig(name="t", root=tmp_path, output_dir=Path("out"))
    monkeypatch.setattr(runner, "ensure_image", lambda image: None)

    def killed(*args, **kwargs):
        os.kill(os.getpid(), signal.SIGTERM)
        raise AssertionError("SIGTERM should have interrupted")

    monkeypatch.setattr(runner, "process_cell", killed)
    monkeypatch.setattr(runner, "problem_statement", lambda *a, **k: "text")
    with pytest.raises(KeyboardInterrupt):
        runner.run_experiment(cfg, {"a__a-1": {"instance_id": "a__a-1"}}, ["a__a-1"],
                              models=["m"], variants=["orig"], repeats=1, workers=1)
    assert ("image", "rm", "-f", cfg.image_for("a__a-1")) in docker_calls
    assert signal.getsignal(signal.SIGTERM) is not None
