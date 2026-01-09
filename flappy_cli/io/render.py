from __future__ import annotations

import atexit
import ctypes
import os
import shutil
import sys

from dataclasses import dataclass

from typing import Protocol

from ..model import World


RESET = "\x1b[0m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"


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


def _center_line(text: str, width: int) -> str:
    inner = text[:width]
    centered = inner.center(width)
    return centered.ljust(width + 2)

class Renderer(Protocol):
    def render(self, world: World, *, message: str = "") -> None: ...


@dataclass(slots=True)
class _Theme:
    tl: str
    tr: str
    bl: str
    br: str
    h_top: str
    h_bottom: str
    v: str

    sky: str
    pipe: str
    bird: str


@dataclass(slots=True)
class AsciiRenderer:
    clear_once: bool = True
    use_colors: bool = True
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

    def _theme(self) -> _Theme:
        tl = "▄"
        tr = "▄"
        bl = "▀"
        br = "▀"
        h_top = "▄"
        h_bottom = "▀"
        v = "█"

        sky = " "

        if self.use_colors:
            bird = YELLOW + "●" + RESET
            pipe = GREEN + "█" + RESET
        else:
            bird = "●"
            pipe = "█"

        return _Theme(
            tl=tl, tr=tr, bl=bl, br=br,
            h_top=h_top, h_bottom=h_bottom, v=v,
            sky=sky, pipe=pipe, bird=bird,
        )

    def _build_grid(self, world: World, theme: _Theme) -> list[list[str]]:
        grid = [[theme.sky for _ in range(world.width)] for _ in range(world.height)]
        self._draw_pipes(world, grid, theme)
        self._draw_bird(world, grid, theme)
        return grid

    def _draw_pipes(self, world: World, grid: list[list[str]], theme: _Theme) -> None:
        for pipe in world.pipes:
            x = pipe.x
            if not (0 <= x < world.width):
                continue

            gap_start = pipe.gap_y
            gap_end = pipe.gap_y + pipe.gap_h
            for y in range(world.height):
                if gap_start <= y < gap_end:
                    continue
                grid[y][x] = theme.pipe

    def _draw_bird(self, world: World, grid: list[list[str]], theme: _Theme) -> None:
        y = world.bird.cell_y
        x = world.bird.x
        if 0 <= x < world.width and 0 <= y < world.height:
            grid[y][x] = theme.bird

    def _build_hud_lines(self, world: World, message: str) -> list[str]:
        hud = [f"Score: {world.score}"]
        if message:
            hud.extend(message.splitlines())
        return hud

    def _build_frame_lines(self, world: World, grid: list[list[str]], hud: list[str], theme: _Theme) -> list[str]:
        top = theme.tl + (theme.h_top * world.width) + theme.tr
        bottom = theme.bl + (theme.h_bottom * world.width) + theme.br

        lines: list[str] = []

        for h in hud:
            inner = _center_line(h, world.width)
            lines.append(inner.ljust(world.width + 2))

        lines.append(top)
        for row in grid:
            lines.append(theme.v + "".join(row) + theme.v)
        lines.append(bottom)

        return lines

    def _pad_frame(self, lines: list[str], *, world_width: int) -> str:
        term_cols, term_rows = shutil.get_terminal_size(fallback=(120, 30))

        frame_width = world_width + 2

        left_pad = max(0, (term_cols - frame_width) // 2)
        pad_spaces = " " * left_pad

        frame_height = len(lines)
        top_pad = max(0, (term_rows - frame_height) // 2)
        pad_newlines = "\n" * top_pad

        padded = [pad_spaces + "\x1b[2K" + line for line in lines]
        return pad_newlines + "\n".join(padded) + "\n"

    def render(self, world: World, *, message: str = "") -> None:
        self._init_console()

        theme = self._theme()
        grid = self._build_grid(world, theme)
        hud = self._build_hud_lines(world, message)
        lines = self._build_frame_lines(world, grid, hud, theme)

        frame = self._pad_frame(lines, world_width=world.width)
        sys.stdout.write("\x1b[H" + frame)
        sys.stdout.flush()


@dataclass(slots=True)
class NullRenderer:
    def render(self, world: World, *, message: str = "") -> None:
        return
