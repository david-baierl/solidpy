from typing import Callable

from core.event.subject import Subject

# ---------------------------------------------------------------------------- #
# base class
# ---------------------------------------------------------------------------- #

class InternalSignalBase[T](Subject[T]):
    """@internal: Use `ReadonlySignal[T]` (or `Signal[T]`) instead"""

    __value: T

    def __init__(self, init: T) -> None:
        super().__init__()
        self.__value = init

    def __call__(self) -> T:
        return self._get()

    # only used in sub classes
    def _set(self, value: T) -> None:
        if self.__value == value:
            return

        self.__value = value
        self.emit(self.__value)

    def _get(self) -> T:
        global INTERNAL_CURRENT_SIGNAL_SCOPE

        if INTERNAL_CURRENT_SIGNAL_SCOPE != None:
            INTERNAL_CURRENT_SIGNAL_SCOPE.add_dependency(self)

        return self.__value

    def untracked(self) -> T:
        return self.__value

# ---------------------------------------------------------------------------- #
# readonly signal
# ---------------------------------------------------------------------------- #

class ReadonlySignal[T](InternalSignalBase[T]):
    ...

# ---------------------------------------------------------------------------- #
# signal
# ---------------------------------------------------------------------------- #

class Signal[T](InternalSignalBase[T]):

    def set(self, value: T) -> None:
        self._set(value)

# ---------------------------------------------------------------------------- #
# signal scope
# ---------------------------------------------------------------------------- #

INTERNAL_CURRENT_SIGNAL_SCOPE: None | SignalScope = None

class SignalScope[T]:
    __fn: Callable[[], T]
    __dependencies: dict[str, Callable]

    def __init__(self, fn: Callable[[], T]):
        self.__fn = fn
        self.__dependencies = {}

    def _run(self) -> T:
        global INTERNAL_CURRENT_SIGNAL_SCOPE
        self._clear()

        prev_context = INTERNAL_CURRENT_SIGNAL_SCOPE
        INTERNAL_CURRENT_SIGNAL_SCOPE = self
        value = self.__fn()
        INTERNAL_CURRENT_SIGNAL_SCOPE = prev_context

        return value

    def add_dependency(self, parent: InternalSignalBase):
        name = repr(id(parent))

        # allready subscribed
        if name in self.__dependencies:
            return

        self.__dependencies[name] = parent.subscribe(
            lambda _: self._run()
        )

    def _clear(self):
        dependencies = [*self.__dependencies.values()]
        for unsubscribe in dependencies:
            unsubscribe()

        self.__dependencies = {}

    def destroy(self):
        self._clear()

# ---------------------------------------------------------------------------- #
# computed
# ---------------------------------------------------------------------------- #

class Computed[T](InternalSignalBase[T], SignalScope[T]):
    """
    use `@computed` decorator instead to auto destroy (via implicit Context)
    """

    def __init__(self, fn: Callable[[], T]):
        SignalScope.__init__(self, fn)

        # @hint: use super().run() to skip self._set() the first time
        InternalSignalBase.__init__(self, super()._run())

    def _run(self):
        value = super()._run()
        self._set(value)
        return value

# ---------------------------------------------------------------------------- #
# effect
# ---------------------------------------------------------------------------- #

class Effect(SignalScope[Callable | None]):
    """
    use `@effect` decorator instead to auto destroy (via implicit Context)
    """

    __cleanup: Callable | None

    def __init__(self, fn: Callable[[], Callable | None]):
        self.__cleanup = None
        SignalScope.__init__(self, fn)
        self._run()

    def _clear(self):
        if self.__cleanup != None:
            self.__cleanup()
        super()._clear()

    def _run(self):
        self.__cleanup = super()._run()
        return self.__cleanup
