from typing import Callable

from ..context import ctx
from .virtual import Node, VirtualNode

class ComponentNode(VirtualNode):
    __child: VirtualNode

    def __init__(self, child: VirtualNode):
        super().__init__()
        self.__child = child

    # -----------------------------------------------
    # builder pattern
    # -----------------------------------------------

    def styles(self, **styles) -> ComponentNode:
        self.__child.styles(**styles)
        return self

    # -----------------------------------------------
    # lifetime
    # -----------------------------------------------

    def render(self, root: Node) -> ComponentNode:
        self.__child.render(root)
        return self

    def pack(self, **styles) -> None:
        self.__child.pack(**styles)

    def grid(self, x: int, y: int, **styles) -> None:
        self.__child.grid(x, y, **styles)

# ---------------------------------------------------------------------------- #
# lifetime
# ---------------------------------------------------------------------------- #

type Component[**P = []] = Callable[P, VirtualNode]
def component[**P](factory: Component[P]) -> Component[P]:

    def wrapper(*args: P.args, **kwargs: P.kwargs):
        with ctx().scope():
            return ComponentNode(factory(*args, **kwargs))

    return wrapper
