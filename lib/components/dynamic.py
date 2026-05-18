import tkinter as tk
from typing import Any

from ..core.helper import Effect
from ..core.node.component import component
from ..core.node.tk import TKNode
from ..core.node.types import Child_Prop, Children
from ..core.node.virtual import Node
from ..core.signal import Accessor

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
def Dynamic[T](
    data: Accessor[T],
    children: Child_Prop[T],
    styles: dict[str, Any] = {},

    *args,
    **kwargs,
):

    def render(root: Node):
        cache: Children = []
        frame = tk.Frame(root, *args, **kwargs)

        @Effect
        def update():
            nonlocal cache
            item = data()

            for child in cache:
                if child == None:
                    continue

                child.destroy()

            cache = children(item)
            for child in cache:
                if child == None:
                    continue

                child.render(frame).pack(**{
                    **vertical,
                    **styles
                })

        return frame

    return TKNode(render)
