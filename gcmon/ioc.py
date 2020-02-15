from dnry.config import IConfigSection
from pyioc3 import StaticContainerBuilder, ScopeEnum
from pychromecast import get_chromecasts

from gcmon.cast_listener import CastListener
from gcmon.message_creator import MessageCreator
from gcmon.types import GetChromecastDelegate, EntryInterface, CastListenerInterface, MessageCreatorInterface, \
    MessageBrokerInterface


def build_entry(entry_type: EntryInterface, config: IConfigSection) -> EntryInterface:

    ioc_builder = StaticContainerBuilder()

    ioc_builder.bind_constant(
        annotation=IConfigSection,
        value=config)

    ioc_builder.bind_constant(
        annotation=GetChromecastDelegate,
        value=get_chromecasts)

    ioc_builder.bind(
        annotation=CastListenerInterface,
        implementation=CastListener,
        scope=ScopeEnum.TRANSIENT)

    ioc_builder.bind(
        annotation=MessageCreatorInterface,
        implementation=MessageCreator,
        scope=ScopeEnum.TRANSIENT)

    ioc_builder.bind(
        annotation=entry_type,
        implementation=entry_type,
        scope=ScopeEnum.TRANSIENT)

    if config.get("MessageBroker:Type") == "RabbitMQ":
        from gcmon.rabbit_message_broker import RabbitMessageBroker as MessageBroker
    elif config.get("MessageBroker:Type") == "Kafka":
        from gcmon.kafka_message_broker import KafkaMessageBroker as MessageBroker
    else:
        raise RuntimeError("Unsupported message broker.")

    ioc_builder.bind(
        annotation=MessageBrokerInterface,
        implementation=MessageBroker,
        scope=ScopeEnum.TRANSIENT)

    provider = ioc_builder.build()
    return provider.get(entry_type)
