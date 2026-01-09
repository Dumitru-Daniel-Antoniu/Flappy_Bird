from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

from .strategy import FixedIntervalSpawner, ScalingIntervalSpawner, SpawnerStrategy


class GameMode(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass(slots=True, frozen=True)
class GameConfig:
    width: int = 45
    height: int = 20
    bird_x: int = 6

    gravity: float = 0.25
    flap_velocity: float = -1.6

    fps: int = 20

    seed: int | None = None


def make_spawner(mode: GameMode) -> SpawnerStrategy:
    if mode == GameMode.EASY:
        return FixedIntervalSpawner(interval_ticks=24, gap_h=8)

    if mode == GameMode.MEDIUM:
        return ScalingIntervalSpawner(
            start_interval=23,
            min_interval=15,
            every_points=4,
            gap_h=7
        )

    return ScalingIntervalSpawner(
        start_interval=22,
        min_interval=12,
        every_points=3,
        gap_h=6
    )
