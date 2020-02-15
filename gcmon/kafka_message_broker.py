from confluent_kafka import Producer
from dnry.config import IConfigSection
from pika.channel import Channel

from gcmon.types import MessageBrokerInterface
import json


class KafkaMessageBroker(MessageBrokerInterface):
    __channel: Channel

    def __init__(self, config: IConfigSection):

        config = config.get_section("MessageBroker")
        self._servers = config.get("Servers") or "localhost"
        self._topic = config.get("Topic") or "gcmon_events"

        if self._servers is None:
            raise RuntimeError("No connection string provided for broker.")

        self._broker = Producer({'bootstrap.servers': self._servers})

    def __del__(self):
        self._broker.flush()

    def publish_message(self, message):
        self._broker.poll(0)
        payload = json.dumps(message)
        self._broker.produce(
            self._topic,
            payload.encode('utf-8'),
            callback=self._delivery_report)

    def _delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

