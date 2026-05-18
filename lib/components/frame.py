import tkinter as tk
from typing import Any

from ..core.node.component import component
from ..core.node.tk import TKNode
from ..core.node.types import Child_Prop
from ..core.node.virtual import Node

vertical = {
    "side": tk.TOP,
    "fill": "y",
    "anchor": "nw",
}

horizontal = {
    "side": tk.LEFT,
    "fill": "x",
    "anchor": "nw"
}

inline = {
    "side": tk.LEFT,
    "fill": "none",
    "anchor":"nw"
}

@component
def Frame(
    children: Child_Prop,
    styles: dict[str, Any] = {},

    *args,
    **kwargs,
):

    def render(root: Node):
        frame = tk.Frame(root, *args, **kwargs)

        for child in children():
            if child == None:
                continue

            child.render(frame).pack(**{
                **vertical,
                **styles
            })

        return frame

    return TKNode(render)
