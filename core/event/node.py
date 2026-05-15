from typing import Any

from core.event.event import Event, EventEmitter

class EventNode[P: EventNode[Any] = EventNode](EventEmitter):
    _parent: P | None

    # ------------------------------------------------------------------------ #
    # lifetime
    # ------------------------------------------------------------------------ #

    def __init__(self, parent: P | None = None):
        super().__init__()
        self._parent = parent
        self.__bind_events()

    def destroy(self) -> None:
        self.__unbind_events()
        super().destroy()

    # ------------------------------------------------------------------------ #
    # events
    # ------------------------------------------------------------------------ #

    def __bind_events(self) -> None:
        if self._parent == None:
            return

        self._parent.subscribe(self.__bubble_downstream)
        self.subscribe(self.__bubble_upstream)

    def __unbind_events(self) -> None:
        if self._parent == None:
            return

        self._parent.unsubscribe(self.__bubble_downstream)

    # upstream events bubble downstream
    def __bubble_downstream(self, event: Event):
        if event.bubble != "downstream":
            return

        self.emit(event.clone())

    # downstream events bubble upstream
    def __bubble_upstream(self, event: Event):
        if self._parent == None:
            return

        if event.bubble != "upstream":
            return

        self._parent.emit(event)
