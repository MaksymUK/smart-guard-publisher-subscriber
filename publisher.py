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


async def run_publisher_continuous() -> None:
    while True:
        event_occurred = check_for_event()
        if event_occurred:
            message = "Event detected! Sending message."
            await publish_message(message)
        await asyncio.sleep(5)  # Adjust sleep time as needed


def check_for_event() -> bool:
    # Replace with actual event detection logic
    # Returning True as a placeholder to simulate an event.
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--msg",
                        type=str,
                        help="The message to publish.")
    parser.add_argument("--pubsub",
                        action="store_true",
                        help="If set, publish the message. Otherwise, only log.")
    parser.add_argument("--continuous",
                        action="store_true",
                        help="Run publisher continuously.")
    args = parser.parse_args()

    if args.continuous:
        asyncio.run(run_publisher_continuous())
    elif args.msg:
        if args.pubsub:
            asyncio.run(publish_message(args.msg))
        else:
            logging.info(f"Logging message: {args.msg}")


if __name__ == "__main__":
    configure_logging()
    logging.getLogger('azure').setLevel(logging.WARNING)

    main()
