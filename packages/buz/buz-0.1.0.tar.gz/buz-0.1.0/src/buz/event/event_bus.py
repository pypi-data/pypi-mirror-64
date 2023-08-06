from abc import ABC, abstractmethod
from typing import Collection

from buz.event import Event, Subscriber


class EventBus(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        pass

    @abstractmethod
    def bulk_publish(self, events: Collection[Event]) -> None:
        pass

    @abstractmethod
    def register(self, subscriber: Subscriber) -> None:
        pass

    @abstractmethod
    def unregister(self, subscriber: Subscriber) -> None:
        pass
