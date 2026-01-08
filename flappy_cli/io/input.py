from __future__ import annotations

import msvcrt

from dataclasses import dataclass

from typing import Optional, Protocol


class KeyReader(Protocol):
    def read_key(self) -> Optional[str]: ...
    def flush(self) -> None: ...


@dataclass(slots=True)
class WindowsKeyReader:
    def read_key(self) -> Optional[str]:
        if not msvcrt.kbhit():
            return None

        ch = msvcrt.getwch()

        return ch.lower()

    def flush(self) -> None:
        while msvcrt.kbhit():
            msvcrt.getwch()


@dataclass(slots=True)
class NullKeyReader:
    def read_key(self) -> Optional[str]:
        return None

    def flush(self) -> None:
        return
