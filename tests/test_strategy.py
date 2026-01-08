import random

from flappy_cli.model import Bird, World
from flappy_cli.strategy import FixedIntervalSpawner, ScalingIntervalSpawner


def make_world(*, score=0, width=20, height=10) -> World:
    bird = Bird(x=5, y=5.0)
    world =  World(width=width, height=height, bird=bird, pipes=[], score=score)
    return world


def test_fixed_interval_should_spawn():
    world = make_world()
    spawner = FixedIntervalSpawner(interval_ticks=5)

    assert spawner.should_spawn(tick=5, world=world) is True
    assert spawner.should_spawn(tick=6, world=world) is False
    assert spawner.should_spawn(tick=10, world=world) is True


def test_fixed_interval_make_pipe_in_bounds():
    world = make_world(height=10)
    spawner = FixedIntervalSpawner(interval_ticks=5, gap_h=4)
    rng = random.Random(123)

    pipe = spawner.make_pipe(world=world, rng=rng)
    assert pipe.x == world.width - 1
    assert 0 <= pipe.gap_y <= world.height - pipe.gap_h


def test_scaling_interval_decreases_with_score():
    spawner = ScalingIntervalSpawner(
        start_interval=10,
        min_interval=6,
        every_points=2,
    )

    assert spawner.current_interval(score=0) == 10
    assert spawner.current_interval(score=1) == 10
    assert spawner.current_interval(score=2) == 9
    assert spawner.current_interval(score=4) == 8
    assert spawner.current_interval(score=100) == 6
