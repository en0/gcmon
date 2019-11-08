import pika
from pika.channel import Channel

from gcmon.config import Configuration
from gcmon.types import MessageBrokerInterface
import json


class RabbitMessageBroker(MessageBrokerInterface):
    __channel: Channel

    def __init__(self, config: Configuration):
        config = config.get_section("MessageBroker")
        self.__con_str = config.get("ConnectionString")
        self.__exchange_name = config.get("Exchange") or "gcmon_events"
        self.__exchange_type = config.get("ExchangeType") or "topic"
        self.__routing_key = config.get("RoutingKey") or "media_event"
        self.__channel = None
        if self.__con_str is None:
            raise RuntimeError("No connection string provided for broker.")

    def __del__(self):
        if self.__channel:
            self.__channel.close()

    def __get_channel(self) -> Channel:
        if self.__channel:
            return self.__channel

        params = pika.URLParameters(self.__con_str)
        connection = pika.BlockingConnection(params)

        self.__channel = connection.channel()
        self.__channel.exchange_declare(exchange=self.__exchange_name, exchange_type=self.__exchange_type)
        return self.__channel

    def publish_message(self, message):
        message_json = json.dumps(message)
        channel = self.__get_channel()
        channel.basic_publish(exchange=self.__exchange_name, routing_key=self.__routing_key, body=message_json)
        print(message_json)

