#!/bin/sh
# Check if the .env file exists and export the variables
if [ -f "$ENV_FILE_PATH" ]; then
    export $(cat $ENV_FILE_PATH | sed 's/#.*//g' | xargs)
fi

case $1 in
    run_publisher)
        echo "Starting the publisher..."
        python -u publisher.py --continuous
        ;;
    run_subscriber)
        echo "Starting the subscriber..."
        python -u subscriber.py --continuous
        ;;
    *)
        exec "$@"
        ;;
esac

tail -f /dev/null
