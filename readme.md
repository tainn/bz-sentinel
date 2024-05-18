# bz-sentinel

a monitoring app that posts a discord channel webhook whenever a new forum post is recorded on
the [bzflag forums](https://forums.bzflag.org)

## env vars

a collection of configurable environment variables is read by the app, all of which can be specified in an **.env** file
inside the project's root. see **.env.example** for a reference and defaults, excluding the
sensitive **BZS_WEBHOOK_CHANNELS** list

## run

uses an external network that has to be predefined

```console
docker network create bzf
docker compose up -d
```
