# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set an environment variable to specify the path to the .env file
ENV ENV_FILE_PATH=/app/.env

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Expose the port the app runs on (optional, for documentation purposes)
EXPOSE 80

# Default command to run when starting the container
ENTRYPOINT ["./entrypoint.sh"]
