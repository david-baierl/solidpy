from typing import Callable, Literal

from core.event.subject import Subject

type EventBubble = Literal['none', 'upstream', 'downstream']
type EventHandler[T: Event] = Callable[[T], None]

class Event:
    __bubble: EventBubble

    def __init__(
        self,
        bubble: EventBubble = 'upstream'
    ) -> None:
        self.__bubble = bubble

    @property
    def bubble(self) -> EventBubble:
        return self.__bubble

    def stop(self):
        self.__bubble = 'none'

    def clone(self) -> Event:
        return type(self)()

class EventEmitter(Subject[Event]):
    ...
