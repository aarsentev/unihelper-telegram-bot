import time
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class BotStats:
    started_at: float = field(default_factory=time.time)
    user_ids: set[int] = field(default_factory=set)
    commands: Counter[str] = field(default_factory=Counter)

    @property
    def uptime_seconds(self) -> int:
        return int(time.time() - self.started_at)

    def seen_user(self, user_id: int) -> None:
        self.user_ids.add(user_id)

    def bump(self, command: str) -> None:
        self.commands[command] += 1


stats = BotStats()
