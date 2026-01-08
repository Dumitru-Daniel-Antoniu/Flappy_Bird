from __future__ import annotations

from dataclasses import dataclass

from typing import Optional, Protocol

from ..config import GameMode, make_spawner
from ..model import advance_world, collides


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
            game.world.bird.flap(game.flap_velocity)

    def update(self, game: "Game") -> None:
        return

    def render(self, game: "Game") -> None:
        message = f"1=Easy 2=Medium 3=Hard | SPACE to play | Q to quit"
        game.renderer.render(game.world, message=message)


@dataclass(slots=True)
class PlayingState:
    def handle_input(self, game: "Game", key: Optional[str]) -> None:
        if key == "q":
            game.is_running = False
        elif key == " ":
            game.world.bird.flap(game.flap_velocity)

    def update(self, game: "Game") -> None:
        if game.spawner.should_spawn(tick=game.tick, world=game.world):
            pipe = game.spawner.make_pipe(world=game.world, rng=game.rng)
            game.world.pipes.append(pipe)

        advance_world(game.world, gravity=game.gravity)

        if collides(game.world):
            game.set_state(GameOverState(final_score=game.world.score))

        game.tick += 1

    def render(self, game: "Game") -> None:
        message = f"Mode: {game.mode.value.upper()} | SPACE to flap | Q to quit"
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
        message = f"GAME OVER | Score: {self.final_score} | R to restart | Q to quit"
        game.renderer.render(game.world, message=message)