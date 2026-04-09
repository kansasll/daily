"""Daily Scheduler 启动入口"""

import tkinter as tk
from tkinter import messagebox

from app.service import SchedulerService
from app.storage import JsonScheduleRepository
from app.ui import ScheduleApp


def main():
    root = tk.Tk()
    repository = JsonScheduleRepository()
    service = SchedulerService(repository)

    try:
        ScheduleApp(root, service)
    except Exception as exc:
        messagebox.showerror("启动失败", f"程序初始化失败: {exc}")
        raise

    root.mainloop()


if __name__ == "__main__":
    main()
