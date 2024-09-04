# Publisher Subscriber script for Azure Bus Service
This script is a simple implementation of a publisher and subscriber pattern using Azure Service Bus. The publisher sends a message to a topic and the subscriber receives the message from the topic.

# Instalation and running:
1. Clone the repository
```bash
https://github.com/MaksymUK/smart-guard-publisher-subscriber.git
```
2. Change the directory to the cloned repository
```bash
cd smart-guard-publisher-subscriber
```
3. Setup and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
4. Install the required packages
```bash
pip install -r requirements.txt
```
5. Create a .env file in the root directory of the project and add the following variables:
```bash
FULLY_QUALIFIED_NAMESPACE=

# Required Connection String Based Configuration
CONNECTION_STR=
# Required for Password Less Configuration
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
AZURE_TENANT_ID=

# Required for Publisher & Subscriber
TOPIC_NAME=

# Required for Subscriber Only
SUBSCRIPTION_NAME=
```
6. Build the Docker image
```bash
docker build -t smart-guard-publisher-subscriber .
```
7. Run the Docker container
```bash
docker run --env-file .env -p 4001:80 smart-guard:latest run_subscriber
docker run --env-file .env -p 4000:80 smart-guard:latest run_publisher
```