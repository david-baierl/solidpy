import tkinter as tk
from typing import Any, Iterable

from core.node.component import component
from core.node.tk import TKNode
from core.node.types import Child_Prop
from core.node.virtual import Node

@component
def Table[T](
    data: Iterable[T],
    headers: Child_Prop,
    row: Child_Prop[[T, int]],
    styles: dict[str, Any] = {},

    *args,
    **kwargs,
):

    def render(root: Node):
        frame = tk.Frame(root, *args, **kwargs)

        for x, header in enumerate(headers()):
            if header == None:
                continue
            header.render(frame).grid(x, 0, **styles)

        for y, item in enumerate(data):
            for x, child in enumerate(row(item, y)):
                if child == None:
                    continue
                child.render(frame).grid(x, y+1, **styles)

        return frame

    return TKNode(render)
