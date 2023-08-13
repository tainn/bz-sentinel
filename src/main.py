#!/usr/bin/env python3

import json
import os
import time
from logging import Logger, getLogger

import httpx
from bs4 import BeautifulSoup, ResultSet, Tag
from cordhook import Form
from httpx import Response

from utils import Struct, conf_logs


def main() -> None:
    domain: str = os.getenv("BZS_DOMAIN", "https://forums.bzflag.org")
    url: str = f"{domain}/search.php?search_id=active_topics"
    res: Response = httpx.get(url, timeout=10)

    soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")
    entries: ResultSet = soup.find_all("div", {"class": "list-inner"})

    persistence_path: str = "/src/data/persistence.json"

    if not os.path.exists(persistence_path):
        with open(persistence_path, "w") as wf:
            wf.write("[]")

    with open(persistence_path, "r") as rf:
        persist: list[str] = json.load(rf)

    for entry in entries:
        if entry.find("div", {"class": "responsive-show"}) is None:
            continue

        auth_lp_forum: Tag = entry.find("div", {"class": "responsive-show"})
        auth_lp_forum_data: ResultSet = auth_lp_forum.find_all("a")
        thread: Tag = entry.find("a", {"class": "topictitle"})

        struct: Struct = Struct()

        struct.author_name = auth_lp_forum_data[0].text
        struct.author_url = url_parse(auth_lp_forum_data[0]["href"])
        struct.last_post_url = url_parse(auth_lp_forum_data[1]["href"], post=True)
        struct.last_post_id = struct.last_post_url.split('#')[-1]
        struct.forum_name = auth_lp_forum_data[2].text
        struct.forum_url = url_parse(auth_lp_forum_data[2]["href"])
        struct.thread_name = thread.text
        struct.thread_url = url_parse(thread["href"])

        if struct.last_post_id in persist:
            logger.debug(f"Post previously already collected: {struct.last_post_id}")
            continue

        logger.info(f"New post collected: {struct.last_post_id}")

        persist.append(struct.last_post_id)

        if len(persist) > int(os.getenv("BZS_PERSIST_QUANTITY", 20)):
            persist.pop(0)

        with open(persistence_path, "w") as wf:
            json.dump(persist, wf, indent=4)

        discord_webhook(struct)


def url_parse(raw_url: str, post: bool = False) -> str:
    clean_url: str = raw_url.split("sid=")[0].replace("amp;", "").strip("&")

    if post:
        post_id: str = clean_url.split("=")[-1]
        clean_url: str = f"{clean_url}#p{post_id}"

    return f"{os.getenv('BZS_DOMAIN')}/{clean_url[2:]}"


def discord_webhook(ec: Struct) -> None:
    description: str = (
        f"New [**post**]({ec.last_post_url}) "
        f"by [{ec.author_name}]({ec.author_url}) "
        f"in [{ec.thread_name}]({ec.thread_url})"
    )

    form: Form = Form()

    form.username(os.getenv("BZS_WEBHOOK_USERNAME", "BZSentinel"))
    form.avatar_url(os.getenv("BZS_WEBHOOK_AVATAR", "https://i.imgur.com/FHLEi2t.png"))
    form.embed_color(0000000)
    form.embed_description(description)

    for hook in json.loads(os.getenv("BZS_WEBHOOK_CHANNELS")):
        form.post(hook)


if __name__ == "__main__":
    conf_logs()
    logger = getLogger(__name__)

    while True:
        try:
            main()
            time.sleep(float(os.getenv("BZS_MONITOR_INTERVAL", 60)))
        except Exception as e:
            logger.error(f"Global exception caught: {e}")
            time.sleep(float(os.getenv("BZS_ERR_RETRY_INTERVAL", 120)))
