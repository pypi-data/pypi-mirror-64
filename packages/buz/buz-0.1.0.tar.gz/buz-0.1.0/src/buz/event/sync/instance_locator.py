from collections import defaultdict
from typing import List, DefaultDict

from buz.event import Subscriber
from buz.event.sync import (
    SubscriberAlreadyRegisteredException,
    SubscriberNotRegisteredException,
)


class InstanceLocator:
    def __init__(self) -> None:
        self.__mapping: DefaultDict[str, List[Subscriber]] = defaultdict(lambda: [])

    def register(self, subscriber: Subscriber) -> None:
        event_fqn = subscriber.event_subscribed_to()
        if subscriber in self.__mapping[event_fqn]:
            raise SubscriberAlreadyRegisteredException(subscriber)
        self.__mapping[event_fqn].append(subscriber)

    def unregister(self, subscriber: Subscriber) -> None:
        event_fqn = subscriber.event_subscribed_to()
        if subscriber not in self.__mapping[event_fqn]:
            raise SubscriberNotRegisteredException(subscriber)
        self.__mapping[event_fqn].remove(subscriber)

    def get(self, fqn: str) -> List[Subscriber]:
        return self.__mapping.get(fqn, [])
