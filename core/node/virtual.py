from abc import abstractmethod
import tkinter as tk

from core.context import Context, ctx
from core.event.helper import on
from core.event.types import DestroyEvent

type Node = tk.Widget

class VirtualNode:
    _ctx: Context

    def __init__(self):
        self._ctx = ctx()
        self._ctx.subscribe(on(DestroyEvent, self.destroy))

    def destroy(self, event: DestroyEvent | None = None) -> None:
        # don't emit again
        # this is allready a downstream bubbling event
        if event == None:
            self._ctx.emit(DestroyEvent())

    @abstractmethod
    def styles(self, **styles) -> VirtualNode:
        ...

    @abstractmethod
    def render(self, root: Node) -> VirtualNode:
        ...

    @abstractmethod
    def pack(self, **styles) -> None:
        ...

    @abstractmethod
    def grid(self, x: int, y: int, **styles) -> None:
        ...
