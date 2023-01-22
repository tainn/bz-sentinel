#!/usr/bin/env python3

import json
import logging
import os
import time
from dataclasses import dataclass

import cordhook
import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response

from utils import logutil


@dataclass
class Entry:
    author_name: str = None
    author_url: str = None
    last_post_url: str = None
    last_post_id: str = None
    forum_name: str = None
    forum_url: str = None
    thread_name: str = None
    thread_url: str = None


def main() -> None:
    domain: str = os.getenv("DOMAIN")
    url: str = f"{domain}/search.php?search_id=active_topics"
    res: Response = requests.get(url, timeout=10)

    soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")
    entries: ResultSet = soup.find_all("div", {"class": "list-inner"})

    persistence_path: str = os.getenv("PERSISTENCE_JSON")

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

        container: Entry = Entry()

        container.author_name = triple_data[0].text
        container.author_url = url_parse(triple_data[0]["href"])
        container.last_post_url = url_parse(triple_data[1]["href"], post=True)
        container.last_post_id = container.last_post_url.split('#')[-1]
        container.forum_name = triple_data[2].text
        container.forum_url = url_parse(triple_data[2]["href"])
        container.thread_name = single.text
        container.thread_url = url_parse(single["href"])

        if container.last_post_id in struct:
            logging.debug(f"Post previously already collected: {container.last_post_id}")
            continue

        logging.info(f"New post collected: {container.last_post_id}")

        struct.append(container.last_post_id)

        if len(struct) > int(os.getenv("PERSIST_QUANTITY")):
            struct.pop(0)

        with open(persistence_path, "w") as wf:
            json.dump(struct, wf, indent=4)

        webhook(container)

    time.sleep(float(os.getenv("MONITOR_INTERVAL")))


def url_parse(raw_url: str, post: bool = False) -> str:
    clean_url: str = raw_url.split("sid=")[0].replace("amp;", "").strip("&")

    if post:
        post_id: str = clean_url.split("=")[-1]
        clean_url: str = f"{clean_url}#p{post_id}"

    return f"{os.getenv('DOMAIN')}/{clean_url[2:]}"


def webhook(container: Entry) -> None:
    description: str = (
        f"New [**post**]({container.last_post_url}) "
        f"by [{container.author_name}]({container.author_url}) "
        f"in [{container.thread_name}]({container.thread_url})"
    )

    form: cordhook.Form = cordhook.Form()

    form.username(os.getenv("WEBHOOK_USERNAME"))
    form.avatar_url(os.getenv("WEBHOOK_AVATAR"))
    form.embed_color(0000000)
    form.embed_description(description)

    for hook in json.loads(os.getenv("WEBHOOK_CHANNELS")):
        form.post(hook)


if __name__ == "__main__":
    logutil.configure()

    while True:
        try:
            main()
        except Exception as e:
            logging.error(f"Wrapping exception handle: {e}")
            time.sleep(float(os.getenv("ERR_RETRY_INTERVAL")))
