from typing import Collection

from buz.event import Event, Subscriber, EventBus
from buz.event.sync import InstanceLocator


class SyncEventBus(EventBus):
    def __init__(self, instance_locator: InstanceLocator):
        self.instance_locator = instance_locator

    def register(self, subscriber: Subscriber) -> None:
        self.instance_locator.register(subscriber)

    def unregister(self, subscriber: Subscriber) -> None:
        self.instance_locator.unregister(subscriber)

    def publish(self, event: Event) -> None:
        subscribers = self.instance_locator.get(event.fqn())
        for subscriber in subscribers:
            subscriber.consume(event)

    def bulk_publish(self, events: Collection[Event]) -> None:
        for event in events:
            self.publish(event)
