from flappy_cli.model import Bird, Pipe, World, advance_world, collides


def make_world(*, bird_x=5, bird_y=5.0, width=20, height=10) -> World:
    return World(
        width=width,
        height=height,
        bird=Bird(x=bird_x, y=bird_y),
        pipes=[],
        score=0
    )


def test_collision_out_of_bounds_top():
    world = make_world(bird_y=-1.0)
    assert collides(world) is True


def test_collision_out_of_bounds_bottom():
    world = make_world(bird_y=100.0, height=10)
    assert collides(world) is True


def test_no_collision_with_pipe_when_not_in_gap():
    world = make_world(bird_y=2.0)
    pipe = Pipe(x=world.bird.x, gap_y=5, gap_h=2) 
    world.pipes.append(pipe)
    assert collides(world) is True


def test_no_collision_with_pipe_when_in_gap():
    world = make_world(bird_x=5, bird_y=5.0)
    pipe = Pipe(x=world.bird.x, gap_y=5, gap_h=3) 
    world.pipes.append(pipe)
    assert collides(world) is False


def test_score_increments_once_when_pipe_passes_bird():
    world = make_world(bird_x=5, bird_y=5.0)
    pipe = Pipe(x=6, gap_y=0, gap_h=10)  
    world.pipes.append(pipe)
    assert world.score == 0

    advance_world(world, gravity=0.0)  
    assert world.score == 0

    advance_world(world, gravity=0.0)  
    assert world.score == 1

    advance_world(world, gravity=0.0)  
    assert world.score == 1


def test_offscreen_pipes_removed():
    world = make_world()
    pipe = Pipe(x=0, gap_y=0, gap_h=10)    
    world.pipes.append(pipe)
    advance_world(world, gravity=0.0)  
    assert len(world.pipes) == 0
