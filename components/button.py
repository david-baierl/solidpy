import tkinter as tk

from core.helper import to_string_var
from core.node.virtual import Node
from core.signal import ReadonlySignal
from core.node.tk import TKNode
from core.node.component import component

@component
def Button(
    textvariable: ReadonlySignal[str] | None = None,

    *args,
    **kwargs,
):

    def render(root: Node):
        if textvariable != None:
            kwargs["textvariable"] = to_string_var(root, textvariable)

        return tk.Button(root, *args, **kwargs)

    return TKNode(render)
