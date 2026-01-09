from __future__ import annotations

from dataclasses import dataclass, field

from typing import List


@dataclass(slots=True)
class Bird:
    x: int
    y: int 
    vy: float = 0.0

    def flap(self, flap_velocity: float) -> None:
        self.vy = flap_velocity

    def apply_gravity(self, gravity: float) -> None:
        self.vy += gravity

    def step(self) -> None:
        self.y += self.vy

    @property
    def cell_y(self) -> int:
        return int(self.y)


@dataclass(slots=True)
class Pipe:
    x: int
    gap_y: int
    gap_h: int
    passed: bool = False


@dataclass(slots=True)
class World:
    width: int
    height: int
    bird: Bird
    pipes: List[Pipe] = field(default_factory=list)
    score: int = 0


def in_bounds_y(world: World, y: int) -> bool:
    return 0 <= y < world.height


def pipe_blocks_cell(pipe: Pipe, y: int) -> bool:
    in_gap = pipe.gap_y <= y < (pipe.gap_y + pipe.gap_h)

    return not in_gap


def collides_bounds(world: World) -> bool:
    by = world.bird.cell_y

    return not in_bounds_y(world, by)


def collides_pipe(world: World) -> bool:
    by = world.bird.cell_y
    bx = world.bird.x

    for p in world.pipes:
        if p.x == bx and pipe_blocks_cell(p, by):
            return True

    return False


def collides(world: World) -> bool:
    return collides_bounds(world) or collides_pipe(world)


def move_pipes_left(world: World, dx: int = 1) -> None:
    for p in world.pipes:
        p.x -= dx


def remove_offscreen_pipes(world: World) -> None:
    world.pipes = [p for p in world.pipes if p.x >= 0]


def update_score(world: World) -> None:
    bx = world.bird.x
    for p in world.pipes:
        if (not p.passed) and p.x < bx:
            p.passed = True
            world.score += 1


def advance_world(world: World, *, gravity: float) -> None:
    world.bird.apply_gravity(gravity)
    world.bird.step()

    move_pipes_left(world, dx=1)
    update_score(world)
    remove_offscreen_pipes(world)


def add_pipe(world: World, pipe: Pipe) -> None:
    world.pipes.append(pipe)
