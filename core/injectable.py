from typing import Callable

def gen_ids(start: int = 0):
    i = start

    while True:
        yield i
        i += 1

ids = gen_ids()

class Injectable[T]:
    __id: int
    __factory: Callable[[], T] | None

    def __init__(self, factory: Callable[[], T] | None = None):
        self.__id = ids.__next__()
        self.__factory = factory

    def id(self) -> int:
        return self.__id

    def new(self) -> T:
        if self.__factory == None:
            raise Exception("construct injectable without factory")

        return self.__factory()
