#!/usr/bin/env python3

import json
import os
import time
from logging import Logger, getLogger

import httpx
from bs4 import BeautifulSoup, ResultSet, Tag
from cordhook import Form
from httpx import Response

import logutil
from containers import EntryContainer


def main() -> None:
    domain: str = os.getenv("BZS_DOMAIN")
    url: str = f"{domain}/search.php?search_id=active_topics"
    res: Response = httpx.get(url, timeout=10)

    soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")
    entries: ResultSet = soup.find_all("div", {"class": "list-inner"})

    persistence_path: str = os.getenv("BZS_PERSISTENCE_JSON")

    if not os.path.exists(persistence_path):
        with open(persistence_path, "w") as wf:
            wf.write("[]")

    with open(persistence_path, "r") as rf:
        struct: list[str] = json.load(rf)

    for entry in entries:
        if entry.find("div", {"class": "responsive-show"}) is None:
            continue

        triple: Tag = entry.find("div", {"class": "responsive-show"})  # author, last post, forum
        triple_data: ResultSet = triple.find_all("a")
        single: Tag = entry.find("a", {"class": "topictitle"})  # thread

        ec: EntryContainer = EntryContainer()

        ec.author_name = triple_data[0].text
        ec.author_url = url_parse(triple_data[0]["href"])

        ec.last_post_url = url_parse(triple_data[1]["href"], post=True)
        ec.last_post_id = ec.last_post_url.split('#')[-1]

        ec.forum_name = triple_data[2].text
        ec.forum_url = url_parse(triple_data[2]["href"])

        ec.thread_name = single.text
        ec.thread_url = url_parse(single["href"])

        if ec.last_post_id in struct:
            logger.debug(f"Post previously already collected: {ec.last_post_id}")
            continue

        logger.info(f"New post collected: {ec.last_post_id}")

        struct.append(ec.last_post_id)

        if len(struct) > int(os.getenv("BZS_PERSIST_QUANTITY")):
            struct.pop(0)

        with open(persistence_path, "w") as wf:
            json.dump(struct, wf, indent=4)

        discord_webhook(ec)


def url_parse(raw_url: str, post: bool = False) -> str:
    clean_url: str = raw_url.split("sid=")[0].replace("amp;", "").strip("&")

    if post:
        post_id: str = clean_url.split("=")[-1]
        clean_url: str = f"{clean_url}#p{post_id}"

    return f"{os.getenv('BZS_DOMAIN')}/{clean_url[2:]}"


def discord_webhook(ec: EntryContainer) -> None:
    description: str = (
        f"New [**post**]({ec.last_post_url}) "
        f"by [{ec.author_name}]({ec.author_url}) "
        f"in [{ec.thread_name}]({ec.thread_url})"
    )

    form: Form = Form()

    form.username(os.getenv("BZS_WEBHOOK_USERNAME"))
    form.avatar_url(os.getenv("BZS_WEBHOOK_AVATAR"))
    form.embed_color(0000000)
    form.embed_description(description)

    for hook in json.loads(os.getenv("BZS_WEBHOOK_CHANNELS")):
        form.post(hook)


if __name__ == "__main__":
    logutil.configure()
    logger: Logger = getLogger(__name__)

    while True:
        try:
            main()
            time.sleep(float(os.getenv("BZS_MONITOR_INTERVAL")))
        except Exception as e:
            logger.error(f"Global exception caught: {e}")
            time.sleep(float(os.getenv("BZS_ERR_RETRY_INTERVAL")))
