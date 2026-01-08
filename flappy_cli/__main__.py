from __future__ import annotations

import random

from .config import GameConfig, GameMode, make_spawner
from .game.core import Game
from .io.input import WindowsKeyReader
from .io.render import AsciiRenderer
from .model import Bird, World


def main() -> None:
    config = GameConfig()
    rng = random.Random(config.seed)

    world = World(
        width=config.width,
        height=config.height,
        bird=Bird(x=config.bird_x, y=config.height // 2),
    )

    mode = GameMode.EASY
    spawner = make_spawner(mode)

    game = Game(
        world=world,
        spawner=spawner,
        mode=mode,
        config=config,
        renderer=AsciiRenderer(clear_once=True),
        keys=WindowsKeyReader(),
        rng=rng,
    )

    game.run()


if __name__ == "__main__":
    main()
