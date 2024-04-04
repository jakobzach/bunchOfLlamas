# bunchOfLlamas

## Setup Instructions

To start the application using Docker, run the following commands in your terminal:

1. Build the Docker image:
```bash
docker build -t bunchofllamasapp .
```

2. Run the Docker container:
```bash
docker run --name bunchofllamas -p 80:80 -d --env-file ../.env bunchofllamasapp
```

or just run
```bash
docker-compose up -d
```