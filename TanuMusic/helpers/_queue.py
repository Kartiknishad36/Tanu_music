from collections import defaultdict, deque
from typing import Union
from TanuMusic.helpers._dataclass import Media, Track

MediaItem = Union[Media, Track]


class Queue:
    def __init__(self):
        self.queues = defaultdict(deque)
        self.history = defaultdict(list)

    def put(self, chat_id: int, item: MediaItem) -> int:
        self.queues[chat_id].append(item)
        return len(self.queues[chat_id]) - 1

    def add(self, chat_id: int, item: MediaItem) -> tuple:
        pos = self.put(chat_id, item)
        track = (
            item.title[:30] if getattr(item, "title", None) else str(getattr(item, "id", None)),
        )
        return pos, track

    def force_add(self, chat_id: int, item: MediaItem, remove: int | bool = False) -> None:
        if remove is False:
            self.queues[chat_id].appendleft(item)
        else:
            self.remove_current(chat_id)
            self.queues[chat_id].appendleft(item)
            if remove is not True:
                self.queues[chat_id].rotate(-remove)
                self.queues[chat_id].popleft()
                self.queues[chat_id].rotate(remove)

    def get_current(self, chat_id: int) -> MediaItem | None:
        return self.queues[chat_id][0] if self.queues[chat_id] else None

    def get_next(self, chat_id: int, check: bool = False) -> MediaItem | None:
        if not self.queues[chat_id]:
            return None
        if check:
            return self.queues[chat_id][1] if len(self.queues[chat_id]) > 1 else None

        popped_item = self.queues[chat_id].popleft()
        self.history[chat_id].append(popped_item)
        return self.queues[chat_id][0] if self.queues[chat_id] else None

    def get_previous(self, chat_id: int) -> MediaItem | None:
        if not self.history[chat_id]:
            return None
        prev_item = self.history[chat_id].pop()
        self.queues[chat_id].appendleft(prev_item)
        return prev_item

    def get_queue(self, chat_id: int) -> list:
        return list(self.queues[chat_id])

    def get_all(self, chat_id: int) -> list:
        return self.get_queue(chat_id)

    def remove_current(self, chat_id: int) -> None:
        if self.queues[chat_id]:
            self.history[chat_id].append(self.queues[chat_id].popleft())

    def clear(self, chat_id: int) -> None:
        self.queues[chat_id].clear()
        self.history[chat_id].clear()

    def peek_next(self, chat_id: int, count: int = 2) -> list:
        if not self.queues[chat_id] or len(self.queues[chat_id]) <= 1:
            return []
        queue_list = list(self.queues[chat_id])
        return queue_list[1 : min(len(queue_list), count + 1)]

    @staticmethod
    def is_downloaded(item: MediaItem) -> bool:
        return bool(getattr(item, "file_path", None))
