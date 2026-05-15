from typing import Callable

class Subject[T = None]:
    __listeners: list[Callable[[T]]]

    def __init__(self) -> None:
        self.__listeners = []

    def subscribe(self, fn: Callable[[T]]) -> Callable:
        self.__listeners.append(fn)

        return lambda: self.unsubscribe(fn)

    def unsubscribe(self, fn: Callable[[T]]):
        if fn in self.__listeners:
            self.__listeners.remove(fn)

    def emit(self, event: T):
        # @hint: make copy to avoid unsubscribe side effects
        # that would break the loop by modifying listeners
        listeners = [*self.__listeners]

        for listener in listeners:
            listener(event)

    def destroy(self):
        self.__listeners = []
