from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class Todo:
    id: int
    user_id: int
    text: str
    done: bool
    created_at: datetime

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            text=row["text"],
            done=bool(row["done"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )