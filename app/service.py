from datetime import datetime
import uuid

from app.models import Schedule


class SchedulerService:
    def __init__(self, repository):
        self.repository = repository

    @staticmethod
    def today():
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def normalize_time(time_str):
        parts = time_str.strip().split(":")
        if len(parts) != 2:
            raise ValueError("Invalid time format")

        hour = int(parts[0])
        minute = int(parts[1])
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError("Invalid time")
        return f"{hour:02d}:{minute:02d}"

    def list_today(self):
        today = self.today()
        return [
            Schedule.from_dict(item)
            for item in self.repository.load_all()
            if item.get("date") == today
        ]

    def _save_today(self, today_schedules):
        today = self.today()
        all_items = self.repository.load_all()
        others = [item for item in all_items if item.get("date") != today]
        merged = others + [schedule.to_dict() for schedule in today_schedules]
        self.repository.save_all(merged)

    def add_schedule(self, title, start_time, end_time, priority):
        title = title.strip()
        if not title:
            raise ValueError("请输入任务名称")

        normalized_start = self.normalize_time(start_time)
        normalized_end = self.normalize_time(end_time)
        if normalized_start >= normalized_end:
            raise ValueError("结束时间必须晚于开始时间")

        schedules = self.list_today()
        new_schedule = Schedule(
            id=str(uuid.uuid4()),
            title=title,
            start_time=normalized_start,
            end_time=normalized_end,
            priority=priority,
            completed=False,
            date=self.today(),
        )
        schedules.append(new_schedule)
        self._save_today(schedules)
        return new_schedule

    def delete_schedule(self, schedule_id):
        schedules = self.list_today()
        updated = [s for s in schedules if s.id != schedule_id]
        self._save_today(updated)

    def toggle_complete(self, schedule_id):
        schedules = self.list_today()
        for schedule in schedules:
            if schedule.id == schedule_id:
                schedule.completed = not schedule.completed
                break
        self._save_today(schedules)

    def check_time_conflict(self, start_time, end_time):
        start_time = self.normalize_time(start_time)
        end_time = self.normalize_time(end_time)

        conflicts = []
        for schedule in self.list_today():
            if schedule.completed:
                continue

            if not (end_time <= schedule.start_time or start_time >= schedule.end_time):
                conflicts.append(f"- {schedule.title} ({schedule.start_time}-{schedule.end_time})")

        return "\n".join(conflicts) if conflicts else None

    @staticmethod
    def progress(schedules):
        total = len(schedules)
        if total == 0:
            return 0, 0, 0
        completed = sum(1 for s in schedules if s.completed)
        percentage = int((completed / total) * 100)
        return completed, total, percentage
