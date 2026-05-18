import tkinter as tk
from typing import Any

from .foreach import dynamic_foreach_renderer
from ..core.node.component import component
from ..core.node.tk import TKNode
from ..core.node.types import Child_Prop, Child_Prop_2D
from ..core.node.virtual import Node, VirtualNode
from ..core.signal import Accessor

@component
def Grid(
    children: Child_Prop_2D,
    styles: dict[str, Any] = {},
    rotate: bool = False,

    *args,
    **kwargs,
):

    def pack(node: VirtualNode, x: int, y: int):
        if rotate:
            node.grid(x, y, **styles)
        else:
            node.grid(y, x, **styles)

    def render(root: Node):
        frame = tk.Frame(root, *args, **kwargs)

        for x, row in enumerate(children()):
            for y, child in enumerate(row):
                if child == None:
                    continue

                pack(child.render(frame), x, y)

        return frame

    return TKNode(render)

@component
def Grid_Dynamic[T](
    data: Accessor[list[T]],
    children: Child_Prop[[T, int]],
    rotate: bool = False,

    styles: dict[str, Any] = {},
    *args,
    **kwargs,
):
    def pack(node: VirtualNode, x: int, y: int):
        if rotate:
            node.grid(x, y, **styles)
        else:
            node.grid(y, x, **styles)

    return TKNode(dynamic_foreach_renderer(
        data=data,
        children=children,
        pack=pack,

        *args,
        **kwargs,
    ))
