from typing import Callable, Sequence

from core.node.virtual import VirtualNode


type ChildNode = VirtualNode | None
type Children = Sequence[ChildNode]

type Child_Prop[**T = []] = Callable[T, Children]
type Child_Prop_2D[**T = []] = Callable[T, Sequence[Children]]
