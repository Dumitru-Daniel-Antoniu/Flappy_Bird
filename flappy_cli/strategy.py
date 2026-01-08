from __future__ import annotations

import random

from dataclasses import dataclass

from typing import Protocol

from .model import Pipe, World


class SpawnerStrategy(Protocol):
    def reset(self) -> None: ...
    def should_spawn(self, *, tick: int, world: World) -> bool: ...
    def make_pipe(self, *, world: World, rng: random.Random) -> Pipe: ...


@dataclass(slots=True)
class FixedIntervalSpawner:
    interval_ticks: int
    gap_h: int = 4
    next_spawn_tick: int = 1

    def reset(self) -> None:
        self.next_spawn_tick = 1

    def should_spawn(self, *, tick: int, world: World) -> bool:
        if tick >= self.next_spawn_tick:
            self.next_spawn_tick = tick + self.interval_ticks

            return True

        return False

    def make_pipe(self, *, world: World, rng: random.Random) -> Pipe:
        max_top =  max(0, world.height - self.gap_h)
        gap_y = rng.randint(0, max_top)

        pipe = Pipe(x=world.width - 1, gap_y=gap_y, gap_h=self.gap_h)

        return pipe


@dataclass(slots=True)
class ScalingIntervalSpawner:
    start_interval: int = 28
    min_interval: int = 16
    every_points: int = 5
    gap_h: int = 4
    next_spawn_tick: int = 1

    def reset(self) -> None:
        self.next_spawn_tick = 1

    def current_interval(self, score: int) -> int:
        dec = score // self.every_points

        return max(self.min_interval, self.start_interval - dec)

    def should_spawn(self, *, tick: int, world: World) -> bool:
        if tick >= self.next_spawn_tick:
            interval = self.current_interval(world.score)
            self.next_spawn_tick = tick + interval

            return True

        return False

    def make_pipe(self, *, world: World, rng: random.Random) -> Pipe:
        max_top =  max(0, world.height - self.gap_h)
        gap_y = rng.randint(0, max_top)

        pipe = Pipe(x=world.width - 1, gap_y=gap_y, gap_h=self.gap_h) 

        return pipe
