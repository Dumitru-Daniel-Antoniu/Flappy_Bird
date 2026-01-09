# Flappy Bird – CLI

This project is a **command line implementation of a Flappy Bird  game**, written in Python.  
The goal of the project was not only to make the game playable, but also to **structure it correctly**, using **SOLID principles** and **well-known design patterns** in a meaningful way.

The game runs entirely in the terminal and uses ASCII / Unicode characters for rendering.

---

## Features

- Playable Flappy Bird–style gameplay in the terminal
- Gravity, flapping, pipes with gaps, scoring
- Multiple game modes (Easy / Medium / Hard)
- Smooth rendering with configurable FPS and simulation speed
- Clean separation between game logic, rendering and input handling
- Unit tests for core logic and state transitions

---

## Requirements

- Python **3.9+** (tested with Python 3.13)
- Windows (CMD supported)
- `requirements.txt` is provided

---

## Setup and Installation

### 1. Clone the repository
```bash
git clone https://github.com/Dumitru-Daniel-Antoniu/Flappy_Bird.git
cd Flappy_Bird
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run the Game

From the project root directory:

```bash
python -m flappy_cli
```

---

## How to Run Tests

The project uses **pytest** for testing.

From the project root directory:

```bash
python -m pytest
```

---

## Project Structure

```
flappy_cli/
│
├── model.py          # Core game data and logic (Bird, Pipe, World)
├── strategy.py       # Pipe spawning strategies (difficulty handling)
├── config.py         # Game configuration and mode setup
│
├── game/
│   ├── core.py       # Main game loop and orchestration
│   └── states.py     # Game states (Start, Playing, Game Over)
│
├── io/
│   ├── render.py     # ASCII renderer
│   └── input.py      # Keyboard input handling
│
└── __main__.py       # Entry point
```

---

## Design Patterns Used

This project uses **two main design patterns**:

1. **State Pattern**
2. **Strategy Pattern**

Both patterns are part of the **Gang of Four (GoF)** behavioral patterns.

---

## 1. State Pattern

### Why?
The game naturally progresses through different **states**:
- Start menu
- Playing
- Game Over

Each state has different behavior regarding input handling, updates and rendering.  
Using the State pattern avoids large conditional blocks and keeps responsibilities clearly separated.

### Where in the code?
- `flappy_cli/game/states.py`
- Implementations:
  - `StartState`
  - `PlayingState`
  - `GameOverState`
- The `Game` object delegates behavior to the active state.

### What problem it solves?
- Eliminates complex `if/else` logic
- Makes the game flow explicit and easier to follow
- Allows new states to be added easily (e.g., Pause)

---

## 2. Strategy Pattern

### Why?
Difficulty handling is based on **different algorithms**, not different game states.  
Pipe spawning behavior changes depending on the selected difficulty.

### Where in the code?
- `flappy_cli/strategy.py`
- Implementations:
  - `FixedIntervalSpawner` (Easy)
  - `ScalingIntervalSpawner` (Medium / Hard)

### What problem it solves?
- Separates difficulty logic from the game loop
- Allows new difficulty modes without modifying existing code
- Follows the Open/Closed Principle

---

## Summary of Design Patterns

| Pattern   | Type        | Role in the Project |
|----------|------------|---------------------|
| State    | Behavioral | Controls game flow and behavior per state |
| Strategy | Behavioral | Controls difficulty and pipe spawning logic |

---

## Testing Approach

- Core game logic (movement, collisions, scoring) is unit tested
- State transitions are tested using mock input and a `NullRenderer`
- Rendering and keyboard input are excluded from tests

This keeps tests fast, deterministic and focused on logic.

---
