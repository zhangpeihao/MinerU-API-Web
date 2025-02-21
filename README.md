# Mineru Parser Web Application

This is a web application for parsing files using the Mineru API. It supports both single file and batch processing operations.

## Requirements

- Docker
- Docker Compose

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd mineru_parser
```
2. Create a `.env` file in the root directory of the project and add the following environment variables:
```bash
MINERU_API_key=<your-min
```
3. Build the Docker image:
```bash
docker-compose build
```
4. Run the Docker container:
```bash
docker-compose up
```
5. Access the web application at `http://localhost:8000`.
6. To stop the Docker container, press `Ctrl+C` and run:
```bash
docker-compose down
```