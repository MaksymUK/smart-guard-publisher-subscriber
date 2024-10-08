from typing import Dict

from azure.identity import DefaultAzureCredential
from azure.servicebus import TransportType
from azure.servicebus.aio import ServiceBusClient



class ServiceBusClientFactory:
    _instances: Dict[str, ServiceBusClient] = {}
    _credential = DefaultAzureCredential()

    @staticmethod
    async def get_client(namespace: str) -> ServiceBusClient:
        if namespace not in ServiceBusClientFactory._instances:
            ServiceBusClientFactory._instances[namespace] = ServiceBusClient(
                fully_qualified_namespace=namespace,
                credential=ServiceBusClientFactory._credential,
                transport_type=TransportType.AmqpOverWebsocket,
                logging_enable=True
            )
        return ServiceBusClientFactory._instances[namespace]


class ServiceBusClientFactoryString:
    _instances: Dict[str, ServiceBusClient] = {}

    def __init__(self, connection_str) -> None:
        self.connection_str = connection_str

    async def get_client(self, namespace: str) -> ServiceBusClient:
        if namespace not in ServiceBusClientFactoryString._instances:
            ServiceBusClientFactoryString._instances[namespace] = ServiceBusClient.from_connection_string(
                conn_str=self.connection_str,
                transport_type=TransportType.AmqpOverWebsocket,
                logging_enable=True
            )
        return ServiceBusClientFactoryString._instances[namespace]
