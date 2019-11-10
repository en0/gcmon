import signal
from threading import Event

from dnry.config import ConfigFactory

from gcmon.config import ConfigSource
from gcmon.ioc import build_entry
from gcmon.types import GetChromecastDelegate, CastListenerInterface


class Entry:

    def __init__(self, get_devices: GetChromecastDelegate, listener: CastListenerInterface):
        self.listener = listener
        self.get_devices = get_devices
        self.event = Event()

    def install_shutdown_hook(self):
        def handler(signum, frame):
            self.event.set()

        signal.signal(signal.SIGINT, handler)

    def __call__(self, *args, **kwargs):
        self.install_shutdown_hook()
        for device in self.get_devices():
            device.start()
            self.listener.register_device(device)
        self.event.wait()


def main():
    config = ConfigFactory([ConfigSource()]).build()
    entry = build_entry(Entry, config)
    entry()
