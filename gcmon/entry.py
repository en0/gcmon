from gcmon.ioc import build_entry
from gcmon.types import GetChromecastDelegate, CastListenerInterface
from threading import Event
import signal


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
    from sys import argv
    entry = build_entry(Entry)
    entry(argv)
