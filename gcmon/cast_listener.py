from pychromecast import Chromecast
from pychromecast.controllers.media import MediaStatus

from gcmon.types import CastListenerInterface, MessageBrokerInterface, MessageCreatorInterface


class CastListener(CastListenerInterface):

    class CastListenerDeviceAdapter:
        def __init__(self, ctx: "CastListener", device: Chromecast):
            self.ctx = ctx
            self.device = device

        def new_media_status(self, status: MediaStatus):
            self.ctx.new_media_status(self.device, status)

    def __init__(self, message_broker: MessageBrokerInterface, message_creator: MessageCreatorInterface):
        self.message_creator = message_creator
        self.message_broker = message_broker

    def register_device(self, device: Chromecast):
        print(f"Registering device {device.name}")
        device.media_controller.register_status_listener(CastListener.CastListenerDeviceAdapter(self, device))

    def new_media_status(self, device: Chromecast, status: MediaStatus):
        message = self.message_creator.create_message(device, status)
        self.message_broker.publish_message(message)
