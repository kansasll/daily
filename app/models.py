from dataclasses import dataclass


@dataclass
class Schedule:
    id: str
    title: str
    start_time: str
    end_time: str
    priority: int
    completed: bool
    date: str

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "priority": self.priority,
            "completed": self.completed,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=str(data.get("id", "")),
            title=str(data.get("title", "未命名")),
            start_time=str(data.get("start_time", "00:00")),
            end_time=str(data.get("end_time", "00:00")),
            priority=int(data.get("priority", 2)),
            completed=bool(data.get("completed", False)),
            date=str(data.get("date", "")),
        )
