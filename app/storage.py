import json
import os
from pathlib import Path


class JsonScheduleRepository:
    def __init__(self, file_path=None):
        self.file_path = Path(file_path) if file_path else self._default_data_path()
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _default_data_path():
        # Windows 使用 APPDATA，避免程序安装目录无写权限。
        appdata = os.getenv("APPDATA")
        if appdata:
            return Path(appdata) / "DailyScheduler" / "scheduler.json"
        return Path("scheduler.json")

    def load_all(self):
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("schedules", [])
        except (json.JSONDecodeError, OSError):
            return []

    def save_all(self, schedules):
        payload = {"schedules": schedules}
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
