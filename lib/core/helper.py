import tkinter as tk
from typing import Callable

from .context import ctx
from .event.helper import on
from .event.types import DestroyEvent
from .node.virtual import Node
from .signal import Accessor, Effect

# --------------------------------------------
# lifetime
# --------------------------------------------

def on_destroy(fn: Callable[[], None]) -> None:
    ctx().subscribe(on(DestroyEvent, lambda _: fn()))

# --------------------------------------------
# decorators
# --------------------------------------------

def memo[T](fn: Callable[[T | None], T]) -> Callable[[], T]:
    prev = None

    def wrapper() -> T:
        nonlocal prev
        prev = fn(prev)
        return prev

    return wrapper

# --------------------------------------------
# tkinter specific converter
# --------------------------------------------

def to_string_var(root: Node | None, value: Accessor[str]) -> tk.StringVar:
    var = tk.StringVar(root)
    Effect(lambda: var.set(value()))
    return var

def to_bool_var(root: Node, value: Accessor[bool]) -> tk.BooleanVar:
    var = tk.BooleanVar(root)
    Effect(lambda: var.set(value()))
    return var

def to_int_var(root: Node, value: Accessor[int]) -> tk.IntVar:
    var = tk.IntVar(root)
    Effect(lambda: var.set(value()))
    return var

def to_float_var(root: Node, value: Accessor[float]) -> tk.DoubleVar:
    var = tk.DoubleVar(root)
    Effect(lambda: var.set(value()))
    return var

# --------------------------------------------
# diff
# --------------------------------------------

class Diff[T]:
    __prev: list[T]
    __next: list[T]

    __added: set[T]
    __removed: set[T]

    def __init__(self, prev: list[T], next: list[T]):
        self.__added = set()
        self.__removed = set(prev)

        self.__prev = prev
        self.__next = next

        for item in self.__next:
            if item in self.__removed:
                self.__removed.remove(item)
            else:
                self.__added.add(item)

    def size(self) -> int:
        return len(self.__added) + len(self.__removed)

    def added(self) -> set[T]:
        return self.__added

    def removed(self) -> set[T]:
        return self.__removed

    def next(self) -> list[T]:
        return self.__next

    def prev(self) -> list[T]:
        return self.__prev
