from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Callable


class InMemoryRateLimiter:
    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._clock = clock or time.monotonic
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str, limit_per_minute: int) -> bool:
        if limit_per_minute <= 0:
            return False

        now = self._clock()
        window_start = now - 60.0
        bucket = self._requests[key]

        while bucket and bucket[0] <= window_start:
            bucket.popleft()

        if len(bucket) >= limit_per_minute:
            return False

        bucket.append(now)
        return True
