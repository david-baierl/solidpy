import tkinter as tk
from typing import Callable
from .event import Event, EventHandler

# ignores events that bubble up from children
# like <Destroy>
def bind_direct(master: tk.Misc, name: str, fn: Callable[[tk.Event[tk.Misc]], None]):
    def handle(event: tk.Event[tk.Misc]):
        if master == event.widget:
            fn(event)

    master.bind(name, handle)

def on[T: Event](event_type: type[T], fn: EventHandler[T]) -> EventHandler[Event]:
    def filter(event: Event) -> None:
        if type(event) != event_type:
            return

        fn(event)

    return filter
