from __future__ import annotations

from collections import deque
from threading import Lock
from time import time
from uuid import uuid4

from app.schemas.planner import FakeEvent, FakeEventCreate


class FakeEventStore:
    def __init__(self) -> None:
        self._events: deque[FakeEvent] = deque()
        self._lock = Lock()

    def push(self, payload: FakeEventCreate) -> FakeEvent:
        event = FakeEvent(
            id=uuid4().hex,
            created_at=int(time()),
            event_type=payload.event_type,
            destination=payload.destination,
            day_index=payload.day_index,
            old_value=payload.old_value,
            new_value=payload.new_value,
            note=payload.note,
        )
        with self._lock:
            self._events.append(event)
        return event

    def consume(self, limit: int = 20) -> list[FakeEvent]:
        with self._lock:
            count = max(0, min(limit, len(self._events)))
            return [self._events.popleft() for _ in range(count)]


fake_event_store = FakeEventStore()
