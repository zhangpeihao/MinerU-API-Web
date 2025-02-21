#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your MINERU_TOKEN"
    exit 1
fi

# Build and start the containers
docker compose up --build -d

# Wait for the service to be ready
echo "Waiting for service to start..."
sleep 5

# Check if the service is running
if curl -s http://localhost:8501/_stcore/health > /dev/null; then
    echo "Service is running!"
    echo "Access the application at http://localhost:8501"
else
    echo "Error: Service failed to start!"
    docker compose logs
fi