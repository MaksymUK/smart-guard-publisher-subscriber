import argparse
import asyncio
import logging


from client.client_abstraction import ServiceBusClientFactory
from message.message_publisher import TopicMessageSenderStrategy

from utils.auth import (namespace_name, topic_name)
from utils.pubsub_utils import ServiceBusPublisher
from utils.azure_monitor import configure_logging

# Connection String Based Publisher If It Set to True Otherwise Use Default Azure Login
USE_CONNECTION_STR = True


TOPIC = topic_name()
NAMESPACE = namespace_name()

PUBLISHER = ServiceBusPublisher(namespace=NAMESPACE,
                                strategy=TopicMessageSenderStrategy,
                                use_connection_str=USE_CONNECTION_STR)


async def publish_message(message: str) -> None:
    await PUBLISHER.send_message(queue_or_topic_name=TOPIC,
                                 message_content=message)
    logging.info(f"Message was published successfully in the {TOPIC=}")

    if isinstance(PUBLISHER.factory_object, ServiceBusClientFactory):
        await PUBLISHER.factory_object._credential.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--msg",
                        type=str,
                        required=True,
                        help="The message to publish.")
    parser.add_argument("--pubsub",
                        action="store_true",
                        help="If set, publish the message. Otherwise, only log.")
    args = parser.parse_args()

    if args.msg:
        if args.pubsub:
            asyncio.run(publish_message(args.msg))
        else:
            logging.info(f"Logging message: {args.msg}")


if __name__ == "__main__":
    configure_logging()
    logging.getLogger('azure').setLevel(logging.WARNING)

    main()
