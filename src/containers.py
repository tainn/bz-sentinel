from dataclasses import dataclass


@dataclass
class EntryContainer:
    author_name: str = None
    author_url: str = None

    last_post_url: str = None
    last_post_id: str = None

    forum_name: str = None
    forum_url: str = None

    thread_name: str = None
    thread_url: str = None
