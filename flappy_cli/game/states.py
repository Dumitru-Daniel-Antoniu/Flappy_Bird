from __future__ import annotations

import copy

from dataclasses import dataclass

from typing import Optional, Protocol

from ..config import GameMode, make_spawner
from ..model import advance_world, collides, collides_pipe


class GameState(Protocol):
    def handle_input(self, game: "Game", key: Optional[str]) -> None: ...
    def update(self, game: "Game") -> None: ...
    def render(self, game: "Game") -> None: ...


@dataclass(slots=True)
class StartState:
    def handle_input(self, game: "Game", key: Optional[str]) -> None:
        if key == "q":
            game.is_running = False
            return

        if key == "1":
            game.mode = GameMode.EASY
            return
        if key == "2":
            game.mode = GameMode.MEDIUM
            return
        if key == "3":
            game.mode = GameMode.HARD
            return

        if key == " ":
            game.spawner = make_spawner(game.mode)
            game.reset_world()
            game.set_state(PlayingState())
            game.world.bird.flap(game.config.flap_velocity)

    def update(self, game: "Game") -> None:
        return

    def render(self, game: "Game") -> None:
        message = (
            "1 = Easy   2 = Medium   3 = Hard\n"
            f"Current mode: {game.mode.value.upper()}\n"
            "SPACE to play | Q to quit"
        )
        game.renderer.render(game.world, message=message)


@dataclass(slots=True)
class PlayingState:
    def handle_input(self, game: "Game", key: Optional[str]) -> None:
        if key == "q":
            game.is_running = False
        elif key == " ":
            game.world.bird.flap(game.config.flap_velocity)

    def update(self, game: "Game") -> None:
        if game.spawner.should_spawn(tick=game.tick, world=game.world):
            pipe = game.spawner.make_pipe(world=game.world, rng=game.rng)
            game.world.pipes.append(pipe)

        safe_world = copy.deepcopy(game.world)

        advance_world(game.world, gravity=game.config.gravity)

        if collides(game.world):
            if collides_pipe(game.world):
                game.world = safe_world
            game.set_state(GameOverState(final_score=game.world.score))
            return

        game.tick += 1

    def render(self, game: "Game") -> None:
        message = (
            "PLAYING\n"
            f"Mode: {game.mode.value.upper()}\n"
            "SPACE to flap | Q to quit"
        )
        game.renderer.render(game.world, message=message)


@dataclass(slots=True)
class GameOverState:
    final_score: int

    def handle_input(self, game: "Game", key: Optional[str]) -> None:
        if key == "q":
            game.is_running = False
        elif key == "r":
            game.reset_world()
            game.set_state(StartState())

    def update(self, game: "Game") -> None:
        return

    def render(self, game: "Game") -> None:
        message = (
            "GAME OVER\n"
            f"Final score: {self.final_score}\n"
            "R to restart | Q to quit"
        )
        game.renderer.render(game.world, message=message)
