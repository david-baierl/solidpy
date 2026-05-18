from tkinter import ttk

from ..core.helper import on_destroy, to_string_var
from ..core.node.virtual import Node
from ..core.signal import ReadonlySignal
from ..core.node.tk import TKNode
from ..core.node.component import component

class Options[T](ReadonlySignal[T]):
    __values: list[T] = []
    __labels: list[str] = []

    def __init__(self, options: dict[T, str], default: T | None = None):
        self.__values = list(options.keys())
        self.__labels = list(options.values())
        super().__init__(default if default else self.__values[0])

    def labels(self) -> list[str]:
        return self.__labels

    def select(self, key: str) -> None:
        index = self.__labels.index(key)
        value = self.__values[index]
        self._set(value)

    def current(self) -> str:
        value = self._get()
        index = self.__values.index(value)
        return self.__labels[index]

@component
def Select[V](
    options: Options[V],

    *args,
    **kwargs,
):

    def render(parent: Node) -> Node:
        # dual binding
        var = to_string_var(parent, options.current)
        name = var.trace_add('write', lambda a, b, c: options.select(var.get()))
        on_destroy(lambda: var.trace_remove("write", name))

        combo_box =  ttk.Combobox(
            parent,
            textvariable=var,
            values=options.labels(),
            state="readonly",

            *args,
            **kwargs
        )

        return combo_box

    return TKNode(render)
