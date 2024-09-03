import asyncio
import logging

from message.message_subscriber import TopicMessageReceiverStrategy

from client.client_abstraction import ServiceBusClientFactory
from utils.auth import (namespace_name, subscription_name, topic_name)
from utils.pubsub_utils import ServiceBusSubscriber
from utils.azure_monitor import configure_logging
from utils.custom_msg_process import string_message_handler


# Connection String Based Publisher If It Set to True Otherwise Use Default Azure Login
USE_CONNECTION_STR = True

NAMESPACE = namespace_name()
TOPIC = topic_name()
SUBSCRIPTION_NAME = subscription_name()

SUBSCRIBER = ServiceBusSubscriber(namespace=NAMESPACE,
                                  queue_or_topic_name=TOPIC,
                                  strategy=TopicMessageReceiverStrategy,
                                  use_connection_str=USE_CONNECTION_STR)


async def main():
    await SUBSCRIBER.start_listening(message_handler=string_message_handler,
                                     subscription_name=SUBSCRIPTION_NAME)
    if isinstance(SUBSCRIBER.factory_object, ServiceBusClientFactory):
        await SUBSCRIBER.factory_object._credential.close()


if __name__ == "__main__":
    configure_logging()
    logging.getLogger('azure').setLevel(logging.WARNING)

    asyncio.run(main())
