from core.event.event import Event

class DestroyEvent(Event):
    def __init__(self) -> None:
        super().__init__(bubble="downstream")

    def clone(self) -> DestroyEvent:
        return DestroyEvent()
