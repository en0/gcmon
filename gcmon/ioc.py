from pyioc3 import StaticContainerBuilder, ScopeEnum
from pychromecast import get_chromecasts

from gcmon.cast_listener import CastListener
from gcmon.config import ConfigurationLoader, Configuration
from gcmon.message_creator import MessageCreator
from gcmon.types import GetChromecastDelegate, EntryInterface, CastListenerInterface, MessageCreatorInterface, \
    MessageBrokerInterface


def build_entry(entry_type: EntryInterface, config_path: str = None) -> EntryInterface:

    config = ConfigurationLoader(config_path).load()
    ioc_builder = StaticContainerBuilder()

    ioc_builder.bind_constant(
        annotation=Configuration,
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
        from gcmon.rabbit_message_broker import RabbitMessageBroker
        ioc_builder.bind(
            annotation=MessageBrokerInterface,
            implementation=RabbitMessageBroker,
            scope=ScopeEnum.TRANSIENT)
    else:
        raise RuntimeError("Unsupported message broker.")

    provider = ioc_builder.build()
    return provider.get(entry_type)
