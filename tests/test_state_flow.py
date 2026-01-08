import random

from flappy_cli.config import GameConfig, GameMode, make_spawner
from flappy_cli.game.core import Game
from flappy_cli.game.states import StartState, PlayingState, GameOverState
from flappy_cli.io.input import NullKeyReader
from flappy_cli.io.render import NullRenderer
from flappy_cli.model import Bird, World


def make_test_game() -> Game:
    config = GameConfig(width=20, height=10, bird_x=5, fps=999)
    bird = Bird(x=5, y=5.0)
    world = World(width=20, height=10, bird=bird)
    mode = GameMode.EASY
    spawner = make_spawner(mode)

    game = Game(
        world=world,
        spawner=spawner,
        mode=mode,
        config=config,
        renderer=NullRenderer(),
        keys=NullKeyReader(),
        rng=random.Random(123),
        fps=999
    )

    return game


def test_start_to_playing_on_space():
    game = make_test_game()
    game.set_state(StartState())

    game.step_once(" ")
    assert isinstance(game.state, PlayingState)


def test_playing_to_gameover_on_collision_out_of_bounds():
    game = make_test_game()
    game.set_state(PlayingState())

    game.world.bird.y = -10.0
    game.step_once(None)

    assert isinstance(game.state, GameOverState)
