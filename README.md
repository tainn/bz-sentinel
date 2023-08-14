# bz-sentinel

[![black](https://img.shields.io/badge/style-black-222222.svg)](https://github.com/psf/black)
[![ruff](https://img.shields.io/badge/lint-ruff-222222.svg)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type-mypy-222222.svg)](https://github.com/python/mypy)

A monitoring app that posts a Discord channel webhook whenever a new forum post is recorded on
the [BZFlag forums](https://forums.bzflag.org).

### Env vars

A collection of configurable environment variables is read by the app, all of which can be specified in an **.env** file
inside the project's root. See **.env.example** for a reference and defaults, excluding the
sensitive `BZS_WEBHOOK_CHANNELS` list.

### Network

Uses an external network that has to be predefined.

```console
docker network create bzf
```

### Run

Run as a daemon using docker-compose.

```console
docker-compose up -d
```
