import random
from typing import Any, Generic, Hashable, Optional, Type, TypeVar

T = TypeVar('T', int, float)


class Range(Generic[T]):
    __slots__ = 'start', 'stop', 'step', 'default', 'type'

    def __init__(self, start: T, stop: T, step: Optional[T] = None, default: Optional[T] = None):
        self.start: Any = start
        self.stop: Any = stop
        self.step: Optional[T] = step
        self.default: Optional[T] = default

        self.type: Type[T]
        if isinstance(start, int) and isinstance(stop, int):
            self.type = int
        else:
            self.type = float

    def random(self, seed: Optional[Hashable] = None) -> T:
        if seed:
            random.seed(seed)

        if self.type == int:
            if self.step is None:
                return random.randrange(self.start, self.stop)

            return random.randrange(
                self.start, self.stop, self.step)  # type: ignore

        if self.step is None:
            return random.random() * (self.stop - self.start) + self.start

        return random.randint(0, int((self.stop - self.start) / self.step)) * self.step + self.start
