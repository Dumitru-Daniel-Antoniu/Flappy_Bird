from __future__ import annotations

import atexit
import ctypes
import os
import shutil
import sys

from dataclasses import dataclass

from typing import Protocol

from ..model import World


def _enable_windows_vt() -> None:
    if os.name != "nt":
        return

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    mode = ctypes.c_uint()
    if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)


def _hide_cursor() -> None:
    sys.stdout.write("\x1b[?25l")
    sys.stdout.flush()


def _show_cursor() -> None:
    sys.stdout.write("\x1b[?25h")
    sys.stdout.flush()


class Renderer(Protocol):
    def render(self, world: World, *, message: str = "") -> None: ...


@dataclass(slots=True)
class AsciiRenderer:
    clear_once: bool = True
    _initialized: bool = False

    def _init_console(self) -> None:
        if self._initialized:
            return

        _enable_windows_vt()
        _hide_cursor()
        atexit.register(_show_cursor)

        if self.clear_once:
            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.flush()

        self._initialized = True

    def render(self, world: World, *, message: str = "") -> None:
        self._init_console()

        grid = [[" " for _ in range(world.width)] for _ in range(world.height)]

        for pipe in world.pipes:
            if 0 <= pipe.x < world.width:
                for y in range(world.height):
                    in_gap = pipe.gap_y <= y < pipe.gap_y + pipe.gap_h
                    if not in_gap:
                        grid[y][pipe.x] = "|"

        by = world.bird.cell_y
        bx = world.bird.x
        if 0 <= bx < world.width and 0 <= by < world.height:
            grid[by][bx] = "@"

        term_cols, term_rows = shutil.get_terminal_size(fallback=(120, 30))

        top = "+" + "-" * world.width + "+"
        frame_width = len(top)

        hud1 = f"Score: {world.score}"
        hud2 = message or ""

        lines: list[str] = []
        lines.append("\x1b[2K" + hud1.ljust(world.width + 2))
        lines.append("\x1b[2K" + hud2.ljust(world.width + 2))
        lines.append(top)

        for row in grid:
            lines.append("|" + "".join(row) + "|")

        lines.append(top)

        frame_height = len(lines)

        left_pad = max(0, (term_cols - frame_width) // 2)
        pad_spaces = " " * left_pad

        top_pad = max(0, (term_rows - frame_height) // 2)
        pad_newlines = "\n" * top_pad

        padded_lines = [pad_spaces + line for line in lines]
        frame = pad_newlines + "\n".join(padded_lines) + "\n"

        sys.stdout.write("\x1b[H" + frame + "\x1b[J")
        sys.stdout.flush()


@dataclass(slots=True)
class NullRenderer:
    def render(self, world: World, *, message: str = "") -> None:
        return
