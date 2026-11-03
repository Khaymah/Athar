"""Experiment configuration loaded from YAML."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

ORIGINAL_VARIANT = "orig"


@dataclass
class ModelSpec:
    name: str
    model_name: str
    model_class: str = "openrouter"
    model_kwargs: dict = field(default_factory=dict)


@dataclass
class ExperimentConfig:
    name: str
    root: Path
    dataset: str = "SWE-bench/SWE-bench_Verified"
    split: str = "test"
    image_template: str = "ghcr.io/epoch-research/swe-bench.eval.x86_64.{instance_id}:latest"
    tasks_file: Path = Path("data/pilot_tasks.json")
    cards_dir: Path = Path("data/cards")
    variants_dir: Path = Path("data/variants")
    output_dir: Path = Path("runs/pilot")
    reference_variant: str = "en"
    variants: list[str] = field(default_factory=lambda: [ORIGINAL_VARIANT, "en", "egy", "egy-franco"])
    runs_per_cell: int = 3
    models: list[ModelSpec] = field(default_factory=list)
    agent_step_limit: int = 100
    agent_cost_limit: float = 2.0
    agent_wall_time_seconds: int = 1800
    command_timeout_seconds: int = 120
    eval_timeout_seconds: int = 1800
    workers: int = 4
    cleanup_images: bool = True

    def resolve(self, path: Path) -> Path:
        return path if path.is_absolute() else self.root / path

    @property
    def tasks_path(self) -> Path:
        return self.resolve(self.tasks_file)

    @property
    def cards_path(self) -> Path:
        return self.resolve(self.cards_dir)

    @property
    def variants_path(self) -> Path:
        return self.resolve(self.variants_dir)

    @property
    def output_path(self) -> Path:
        return self.resolve(self.output_dir)

    def image_for(self, instance_id: str) -> str:
        return self.image_template.format(instance_id=instance_id)

    def model(self, name: str) -> ModelSpec:
        for spec in self.models:
            if spec.name == name:
                return spec
        raise KeyError(f"Unknown model '{name}'. Known: {[m.name for m in self.models]}")


def load_config(path: str | Path) -> ExperimentConfig:
    path = Path(path).resolve()
    raw = yaml.safe_load(path.read_text())
    root = path.parent.parent if path.parent.name == "configs" else path.parent
    models = [ModelSpec(**m) for m in raw.pop("models", [])]
    agent = raw.pop("agent", {}) or {}
    evaluation = raw.pop("eval", {}) or {}
    for key in ("tasks_file", "cards_dir", "variants_dir", "output_dir"):
        if key in raw:
            raw[key] = Path(raw[key])
    cfg = ExperimentConfig(root=root, models=models, **raw)
    cfg.agent_step_limit = agent.get("step_limit", cfg.agent_step_limit)
    cfg.agent_cost_limit = agent.get("cost_limit", cfg.agent_cost_limit)
    cfg.agent_wall_time_seconds = agent.get("wall_time_seconds", cfg.agent_wall_time_seconds)
    cfg.command_timeout_seconds = agent.get("command_timeout_seconds", cfg.command_timeout_seconds)
    cfg.eval_timeout_seconds = evaluation.get("timeout_seconds", cfg.eval_timeout_seconds)
    if cfg.reference_variant not in cfg.variants:
        raise ValueError(f"reference_variant '{cfg.reference_variant}' must be listed in variants")
    return cfg
