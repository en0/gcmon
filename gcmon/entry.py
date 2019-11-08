from gcmon.config import ConfigurationLoader
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
    from argparse import ArgumentParser
    ap = ArgumentParser(description="Publish Google Cast events to a message broker")
    ap.add_argument("-c", "--config", help="Path to a configuration file.")
    opts = ap.parse_args()
    config = ConfigurationLoader(opts.config).load()
    entry = build_entry(Entry, config)
    entry()
