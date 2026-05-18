import tkinter as tk

from ..core.helper import to_string_var
from ..core.node.component import component
from ..core.node.tk import TKNode
from ..core.node.virtual import Node
from ..core.signal import Accessor

@component
def Label(
    textvariable: Accessor[str] | None = None,

    *args,
    **kwargs,
):

    def render(root: Node):
        if textvariable != None:
            kwargs["textvariable"] = to_string_var(root, textvariable)

        return tk.Label(root, *args, **kwargs)

    return TKNode(render)
