from collections.abc import Callable
from typing import Protocol


class HasId(Protocol):
    id: str


type Predicate[T] = Callable[[T], bool]


class InMemoryStore[T: HasId]:
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def set(self, item: T) -> None:
        self._items[item.id] = item

    def get(self, item_id: str) -> T | None:
        return self._items.get(item_id)

    def delete(self, item_id: str) -> bool:
        return self._items.pop(item_id, None) is not None

    def find_all(self) -> list[T]:
        return list(self._items.values())

    def find_by(self, predicate: Predicate[T]) -> list[T]:
        return [item for item in self.find_all() if predicate(item)]

    def delete_by(self, predicate: Predicate[T]) -> None:
        for item_id, item in list(self._items.items()):
            if predicate(item):
                del self._items[item_id]
