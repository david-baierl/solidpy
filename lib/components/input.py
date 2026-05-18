import tkinter as tk

from ..core.helper import on_destroy, to_string_var
from ..core.node.component import component
from ..core.node.tk import TKNode
from ..core.node.virtual import Node
from ..core.signal import Signal

@component
def Input(
    value: Signal[str],

    *args,
    **kwargs,
):

    def render(root: Node):
        # dual binding
        var = to_string_var(root, value)
        name = var.trace_add('write', lambda a, b, c: value.set(var.get()))
        on_destroy(lambda: var.trace_remove("write", name))

        return tk.Entry(root, textvariable=var, *args, **kwargs)

    return TKNode(render)
