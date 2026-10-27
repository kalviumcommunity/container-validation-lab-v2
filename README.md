# Container Validation Lab

`incident-api` is a small Python service that lists incidents from a data file baked into the image.

**A container that says `Up` is not the same as a service that works.** This image starts, restarts, reports health and serves data, and something is wrong at each step. Your job is to validate it properly, find each problem from evidence, fix it, and prove the final container is healthy and serving correct data.

## Expected behaviour when everything is fixed

| Check | Expected |
|---|---|
| `docker ps` | `incident-api` shows `Up ... (healthy)` |
| `docker inspect -f '{{.RestartCount}}' incident-api` | `0` |
| `curl -i http://localhost:8080/health` | `HTTP/1.0 200 OK`, `{"status": "ok"}` |
| `curl -i http://localhost:8080/version` | `{"version": "1.1"}` |
| `curl -i http://localhost:8080/incidents` | `200 OK`, 3 incidents |

## Rules

- Keep port 8080, the routes and the version number.
- Do not change the Python code in `app.py`.
- Docker on your own machine only.

## Start

```bash
docker build -t incident-api:1.1 .
sh run.sh
```

## Useful commands

```bash
docker ps -a --filter "name=^incident-api$"
docker logs incident-api
docker inspect -f '{{.RestartCount}} {{.State.ExitCode}}' incident-api
docker inspect -f '{{json .State.Health}}' incident-api
docker inspect -f '{{.Image}}' incident-api
docker images incident-api
```

Windows: use Git Bash, or PowerShell with `curl.exe`. In PowerShell, run the `docker run` command from `run.sh` yourself.

## Clean up

```bash
docker rm -f incident-api
```
