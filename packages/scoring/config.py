from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class ScoringConfig:
    total_weights: dict[str, float]
    component_weights: dict[str, dict[str, float]]
    normalization: dict[str, float]
    recommendation_thresholds: dict[str, float]


@lru_cache
def load_default_config() -> ScoringConfig:
    config_path = Path(__file__).parent / "config" / "default_weights.json"
    raw_config = json.loads(config_path.read_text(encoding="utf-8"))

    return ScoringConfig(
        total_weights=raw_config["total_weights"],
        component_weights=raw_config["component_weights"],
        normalization=raw_config["normalization"],
        recommendation_thresholds=raw_config["recommendation_thresholds"],
    )
