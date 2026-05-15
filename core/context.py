from contextlib import contextmanager
from typing import Any

from core.event.node import EventNode
from core.injectable import Injectable

INTERNAL_CURRENT_CONTEXT_SCOPE: Context | None = None

class Context[P: Context[Any] = Context](EventNode[P]):
    __cache: dict[int, Any]

    # ------------------------------------------------------------------------ #
    # lifetime
    # ------------------------------------------------------------------------ #

    def __init__(self, parent: P | None = None):
        super().__init__(parent)
        self.__cache = {}

    # ------------------------------------------------------------------------ #
    # provider
    # ------------------------------------------------------------------------ #

    def insert[T](self, injectable: Injectable[T], instance: T | None = None) -> T:
        if instance == None:
            instance = injectable.new()

        self.__cache[injectable.id()] = instance
        return instance

    def get[T](self, injectable: Injectable[T]) -> T | None:
        cached = self.__cache.get(injectable.id())

        if cached == None and self._parent != None:
            cached = self._parent.get(injectable)

        return cached

    def get_or_insert[T](self, injectable: Injectable[T], instance: T | None = None) -> T:
        cached = self.get(injectable)

        if cached != None:
            return cached

        return self.insert(injectable, instance)

    def drop[T](self, injectable: Injectable[T]) -> T | None:
        cached = self.get(injectable)
        id = injectable.id()

        if id in self.__cache:
            del self.__cache[injectable.id()]

        return cached

    # ------------------------------------------------------------------------ #
    # scopes
    # ------------------------------------------------------------------------ #

    def create_scope(self) -> Context:
        return Context(self)

    @contextmanager
    def scope(self):
        global INTERNAL_CURRENT_CONTEXT_SCOPE

        prev = INTERNAL_CURRENT_CONTEXT_SCOPE
        next = self.create_scope()

        try:
            INTERNAL_CURRENT_CONTEXT_SCOPE = next
            yield next
        finally:
            INTERNAL_CURRENT_CONTEXT_SCOPE = prev

    @contextmanager
    def self(self):
        global INTERNAL_CURRENT_CONTEXT_SCOPE
        prev = INTERNAL_CURRENT_CONTEXT_SCOPE
        next = self

        try:
            INTERNAL_CURRENT_CONTEXT_SCOPE = next
            yield next
        finally:
            INTERNAL_CURRENT_CONTEXT_SCOPE = prev

def ctx() -> Context:
    global INTERNAL_CURRENT_CONTEXT_SCOPE
    assert(INTERNAL_CURRENT_CONTEXT_SCOPE)
    return INTERNAL_CURRENT_CONTEXT_SCOPE
