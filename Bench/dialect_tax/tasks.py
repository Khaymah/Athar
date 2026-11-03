"""Load SWE-bench instances and select the pilot subset."""

from __future__ import annotations

import json
import random
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

from dialect_tax.cards import prose_length, split_problem_statement

PILOT_DIFFICULTIES = ("<15 min fix", "15 min - 1 hour")
NETWORK_DEPENDENT_REPOS = {"psf/requests"}


@lru_cache(maxsize=4)
def _load(dataset: str, split: str) -> tuple[dict, ...]:
    from datasets import load_dataset

    return tuple(dict(row) for row in load_dataset(dataset, split=split))


def load_instances(dataset: str, split: str) -> dict[str, dict]:
    return {row["instance_id"]: row for row in _load(dataset, split)}


def eligible(instance: dict, *, min_prose: int, max_total: int) -> bool:
    text = instance["problem_statement"]
    if instance.get("difficulty") not in PILOT_DIFFICULTIES:
        return False
    if instance["repo"] in NETWORK_DEPENDENT_REPOS:
        return False
    if len(text) > max_total:
        return False
    if prose_length(text) < min_prose:
        return False
    if "http://" in text or "https://" in text:
        prose, _ = split_problem_statement(text)
        if prose.count("http") > 2:
            return False
    return True


def select_pilot(
    instances: dict[str, dict],
    *,
    n: int = 50,
    seed: int = 20261103,
    min_prose: int = 300,
    max_total: int = 3500,
    max_share_per_repo: float = 0.3,
) -> list[dict]:
    """Stratified sample by repo, capped so no repo dominates (django is ~46% of Verified)."""
    pool: dict[str, list[dict]] = defaultdict(list)
    for inst in sorted(instances.values(), key=lambda r: r["instance_id"]):
        if eligible(inst, min_prose=min_prose, max_total=max_total):
            pool[inst["repo"]].append(inst)
    total = sum(len(v) for v in pool.values())
    if total < n:
        raise ValueError(f"Only {total} eligible instances for n={n}")

    rng = random.Random(seed)
    cap = max(1, int(n * max_share_per_repo))
    quota = {repo: min(cap, max(1, round(n * len(items) / total)), len(items)) for repo, items in pool.items()}
    while sum(quota.values()) > n:
        biggest = max(quota, key=lambda r: quota[r])
        quota[biggest] -= 1
    while sum(quota.values()) < n:
        room = [r for r in pool if quota[r] < min(cap, len(pool[r]))]
        if not room:
            break
        quota[max(room, key=lambda r: len(pool[r]) - quota[r])] += 1

    chosen: list[dict] = []
    for repo in sorted(pool):
        items = pool[repo][:]
        rng.shuffle(items)
        chosen.extend(items[: quota[repo]])
    return sorted(chosen, key=lambda r: r["instance_id"])


def task_summary(instance: dict) -> dict:
    _, attachments = split_problem_statement(instance["problem_statement"])
    return {
        "instance_id": instance["instance_id"],
        "repo": instance["repo"],
        "difficulty": instance["difficulty"],
        "prose_chars": prose_length(instance["problem_statement"]),
        "attachments": len(attachments),
    }


def save_tasks(path: Path, tasks: list[dict], meta: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"meta": meta, "tasks": [task_summary(t) for t in tasks]}
    path.write_text(json.dumps(payload, indent=2) + "\n")


def load_task_ids(path: Path) -> list[str]:
    return [t["instance_id"] for t in json.loads(path.read_text())["tasks"]]
