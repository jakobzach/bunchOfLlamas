# bunchOfLlamas

Run the following CLI commands to start the docker:
docker build -t bunchofllamasapp .
docker run --name bunchofllamas -p 80:80 -d --env-file ../.env bunchofllamasapp