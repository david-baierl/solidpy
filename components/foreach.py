import tkinter as tk
from typing import Any, Callable, Iterable, Sequence

from core.helper import Diff, computed, effect
from core.node.component import component
from core.node.tk import TKNode
from core.node.types import Child_Prop, Children
from core.node.virtual import Node, VirtualNode
from core.signal import ReadonlySignal

@component
def Foreach[T](
    data: Iterable[T],
    children: Child_Prop[[T, int]],

    styles: dict[str, Any] = {},
    *args,
    **kwargs,
):

    def render(root: Node):
        frame = tk.Frame(root, *args, **kwargs)

        for x, item in enumerate(data):
            for child in children(item, x):
                if child == None:
                    continue
                child.render(frame).pack(**styles)

        return frame

    return TKNode(render)

def dynamic_foreach_renderer[T](
    data: ReadonlySignal[list[T]],
    children: Child_Prop[[T, int]],
    pack: Callable[[VirtualNode, int, int], None],

    *args,
    **kwargs,
):
    def render(root: Node):
        prev: list[T] = []
        cache: dict[str, Children] = {}
        frame = tk.Frame(root, *args, **kwargs)

        def get_or_insert(item: T, index: int) -> Children:
            name = repr(id(item))
            cached = cache.get(name)

            if cached != None:
                return cached

            _children = children(item, index)
            cache[name] = _children

            for node in _children:
                if node == None:
                    continue

                node.render(frame)

            return _children

        @computed
        def diff():
            nonlocal prev
            _diff = Diff(prev, data())
            prev = _diff.next()
            return _diff

        @effect
        def update():
            next = diff().next()
            removed = diff().removed()

            for x, item in enumerate(next):
                cached = get_or_insert(item, x)

                for y, node in enumerate(cached):
                    if node == None:
                        continue
                    pack(node, x, y)

            for item in removed:
                name = repr(id(item))
                cached = cache.get(name)

                if cached == None:
                    continue

                for node in cached:
                    if node == None:
                        continue
                    node.destroy()

        return frame
    return render

@component
def Foreach_Dynamic[T](
    data: ReadonlySignal[list[T]],
    children: Child_Prop[[T, int]],

    styles: dict[str, Any] = {},
    *args,
    **kwargs,
):
    def pack(node: VirtualNode, x: int, y: int):
        node.pack(**styles)

    return TKNode(dynamic_foreach_renderer(
        data=data,
        children=children,
        pack=pack,

        *args,
        **kwargs,
    ))

