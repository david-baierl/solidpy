import tkinter as tk
from typing import Any, Callable

from core.event.types import DestroyEvent
from core.node.virtual import VirtualNode

type Node = tk.Widget

class TKNode(VirtualNode):
    __render: Callable[[Node], Node]
    __styles: dict[str, Any] = {}
    __node: Node | None = None

    def __init__(self, render: Callable[[Node], Node]):
        self.__render = render
        self.__styles = {}
        self.__node = None

        super().__init__()

    # -----------------------------------------------
    # builder pattern
    # -----------------------------------------------

    def styles(self, **styles) -> TKNode:
        self.__styles = {
            **self.__styles,
            **styles,
        }

        return self

    # -----------------------------------------------
    # lifetime
    # -----------------------------------------------

    def render(self, root: Node) -> TKNode:
        if self.__node != None:
            self.__node.destroy()

        with self._ctx.self():
            self.__node = self.__render(root)

        return self

    def pack(self, **styles) -> None:
        if self.__node == None:
            return;

        self.__node.pack_forget()
        self.__node.pack(**{
            **styles,
            **self.__styles,
        })

    def grid(self, x: int, y: int, **styles) -> None:
        if self.__node == None:
            return;

        self.__node.grid_forget()
        self.__node.grid(column=x, row=y, **{
            **styles,
            **self.__styles,
        })

    def destroy(self, event: DestroyEvent | None = None) -> None:
        super().destroy(event)

        if self.__node == None:
            return;

        self.__node.destroy()
        self.__node = None
