# bz-sentinel

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A monitoring app that posts a Discord channel webhook whenever a new forum post is recorded on
the [BZFlag forums](https://forums.bzflag.org).

### Network

Uses an external network that has to be predefined.

```commandline
docker network create bzf
```

### Env vars

A collection of configurable environment variables is read by the app, all of which should be specified in an `.env`
file inside the project's root. See `.env.example` for a reference and defaults, excluding the
sensitive `BZS_WEBHOOK_CHANNELS` list.

| env var                  | description                               |
|--------------------------|-------------------------------------------|
| `BZS_LOGGING_JSON`       | path to the log config file               |
| `BZS_PERSISTENCE_JSON`   | path to the file-based persistence        |
| `BZS_DOMAIN`             | domain of the phpBB forum                 |
| `BZS_PERSIST_QUANTITY`   | amount of last posts to persist           |
| `BZS_MONITOR_INTERVAL`   | request interval in seconds               |
| `BZS_ERR_RETRY_INTERVAL` | on-error retry interval in seconds        |
| `BZS_WEBHOOK_USERNAME`   | webhook's appeared username               |
| `BZS_WEBHOOK_AVATAR`     | webhook's displayed avatar                |
| `BZS_WEBHOOK_CHANNELS`   | a list of webhook channel urls, minimum 1 |

### Run

With a provided compose file, the app can be run as a daemon using docker-compose.

```commandline
docker-compose up -d
```
