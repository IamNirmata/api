# llm_api

## Setup

1. Place your SSL key and certificate in `./certs/` as `key.pem` and `cert.pem`.
2. Build and start with Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `https://<your-host>:8000`.

## Endpoints

- `POST /token`: Obtain JWT by providing `username` and `password`.
- `POST /generate`: Submit `prompt`, `max_tokens`, `temperature`; requires Bearer token.
