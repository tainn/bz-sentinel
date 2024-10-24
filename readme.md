# bz-sentinel

A monitoring app that posts a Discord channel webhook whenever a new forum post is recorded on
the [BZFlag forums](https://forums.bzflag.org).

## Env vars

A collection of configurable environment variables is read by the app, all of which can be specified in an `.env` file
inside the project's root. See `.env.example` for a reference and defaults, excluding the
sensitive `BZS_WEBHOOK_CHANNELS` list.

## Run

```console
docker compose up -d
```
