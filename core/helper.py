import tkinter as tk
from typing import Callable

from core.context import ctx
from core.event.helper import bind_direct, on
from core.event.types import DestroyEvent
from core.node.virtual import Node
from core.signal import Computed, Effect, ReadonlySignal

# --------------------------------------------
# decorators
# --------------------------------------------

def computed[T](fn: Callable[[], T]) -> Computed[T]:
    _computed = Computed(fn)

    ctx().subscribe(on(
        DestroyEvent,
        lambda _: _computed.destroy(),
    ))

    return _computed

def effect(fn: Callable[[], Callable | None]) -> Effect:
    _effect = Effect(fn)

    ctx().subscribe(on(
        DestroyEvent,
        lambda _: _effect.destroy(),
    ))

    return _effect

# --------------------------------------------
# tkinter specific converter
# --------------------------------------------

def to_string_var(root: Node | None, signal: ReadonlySignal[str]) -> tk.StringVar:
    var = tk.StringVar(root)
    effect(lambda: var.set(signal()))
    return var

def to_bool_var(root: Node, signal: ReadonlySignal[bool]) -> tk.BooleanVar:
    var = tk.BooleanVar(root)
    effect(lambda: var.set(signal()))
    return var

def to_int_var(root: Node, signal: ReadonlySignal[int]) -> tk.IntVar:
    var = tk.IntVar(root)
    effect(lambda: var.set(signal()))
    return var

def to_float_var(root: Node, signal: ReadonlySignal[float]) -> tk.DoubleVar:
    var = tk.DoubleVar(root)
    effect(lambda: var.set(signal()))
    return var

# --------------------------------------------
# diff
# --------------------------------------------

class Diff[T]:
    __prev: list[T]
    __next: list[T]

    # __added: set[T]
    __removed: set[T]

    def __init__(self, prev: list[T], next: list[T]):
        # self.__added = set()
        self.__removed = set(prev)

        self.__prev = prev
        self.__next = next

        for item in self.__next:
            if item in self.__removed:
                self.__removed.remove(item)
            # else:
            #     self.__added.add(item)

    # def added(self) -> set[T]:
    #     return self.__added

    def removed(self) -> set[T]:
        return self.__removed

    def next(self) -> list[T]:
        return self.__next

    def prev(self) -> list[T]:
        return self.__prev
