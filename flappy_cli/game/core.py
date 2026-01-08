from __future__ import annotations

import random
import time

from dataclasses import dataclass, field

from typing import Optional

from ..config import GameConfig, GameMode
from ..model import World
from ..strategy import SpawnerStrategy
from ..io.input import KeyReader
from ..io.render import Renderer
from .states import GameState, StartState


@dataclass(slots=True)
class Game:
    world: World
    spawner: SpawnerStrategy
    mode: GameMode
    config: GameConfig

    renderer: Renderer
    keys: KeyReader
    rng: random.Random

    gravity: float = 0.25
    flap_velocity: float = -1.6
    fps: int = 20

    state: GameState = field(default_factory=StartState)
    is_running: bool = True
    tick: int = 0

    def set_state(self, state: GameState) -> None:
        self.state = state

    def reset_world(self) -> None:
        self.world.bird.y = self.world.height // 2
        self.world.bird.vy = 0.0
        self.world.pipes.clear()
        self.world.score = 0
        self.tick = 0
        self.spawner.reset()
        self.keys.flush()

    def step_once(self, key: Optional[str]) -> None:
        self.state.handle_input(self, key)
        self.state.update(self)
        self.state.render(self)

    def run(self) -> None:
        frame_time = 1.0 / self.config.fps
        next_t = time.monotonic()

        while self.is_running:
            key = self.keys.read_key()
            self.state.handle_input(self, key)
            self.state.update(self)
            self.state.render(self)

            next_t += frame_time
            delay = next_t - time.monotonic()
            if delay > 0:
                time.sleep(delay)