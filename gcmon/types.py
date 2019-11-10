from abc import ABC, abstractmethod
from typing import NewType, Callable, List
from pychromecast import Chromecast
from pychromecast.controllers.media import MediaStatus

GetChromecastDelegate = NewType("GetChromecastDelegate", Callable[[int, int, int, bool], List[Chromecast]])


class EntryInterface(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplemented()


class CastListenerInterface(ABC):
    @abstractmethod
    def register_device(self, device: Chromecast):
        raise NotImplemented()


class MessageBrokerInterface(ABC):
    @abstractmethod
    def publish_message(self, message):
        raise NotImplemented()


class MessageCreatorInterface(ABC):
    @abstractmethod
    def create_message(self, device: Chromecast, status: MediaStatus):
        raise NotImplemented()
