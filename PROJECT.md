# ECE Big Data Processing Project

## Contributors

| Name | Email
| Jade Vigouroux |
| Melchior Gerrier | melchior.gerrier13@gmail.com
| Adam Kheloufi | 

## Requirements

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose v2
- At least 8 GB of memory allocated to Docker (Docker Desktop: Settings > Resources)
- About 10 GB of free disk space for the IMDb dataset and its Parquet copies

## Setup

1. Clone the repository:

    ```bash
    git clone <repo-url>
    cd <repo-name>
    ```

2. Build and start the containers (Kafka and Spark):

    ```bash
    docker compose up -d --build
    ```

3. Download the IMDb dataset (about 1.5 GB) into `data/raw/`:

    ```bash
    docker compose exec spark python scripts/download_imdb.py
    ```

4. Check that everything works:

    ```bash
    docker compose exec spark python scripts/check_env.py
    ```

## Running the project

<!-- To be completed as each part is merged -->

1. Data preparation: TODO
2. Data exploration: TODO
3. Data enrichment: TODO
4. Streaming: TODO
5. Open question: TODO

## Stopping the environment

```bash
docker compose down        # stop the containers
docker compose down -v     # also delete the cached Kafka connector
```

## AI/LLM tools used

| Tool | Member | Task |
| --- | --- | --- |
| Claude (Anthropic) | Jade Vigouroux | Initial project setup: `docker-compose.yml`, Spark `Dockerfile`, `src/common/`, `scripts/download_imdb.py`, `scripts/check_env.py`, PR template |
