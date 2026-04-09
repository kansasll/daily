import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from app.service import SchedulerService


class AddScheduleDialog:
    def __init__(self, parent, on_submit):
        self.on_submit = on_submit
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("添加行程")
        self.dialog.geometry("350x280")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (280 // 2)
        self.dialog.geometry(f"350x280+{x}+{y}")

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.dialog, text="任务名称:").pack(pady=(20, 5), anchor="w", padx=20)
        self.title_entry = tk.Entry(self.dialog, width=40)
        self.title_entry.pack(padx=20)

        tk.Label(self.dialog, text="开始时间 (HH:MM):").pack(pady=(10, 5), anchor="w", padx=20)
        self.start_time_entry = tk.Entry(self.dialog, width=40)
        self.start_time_entry.pack(padx=20)

        tk.Label(self.dialog, text="结束时间 (HH:MM):").pack(pady=(10, 5), anchor="w", padx=20)
        self.end_time_entry = tk.Entry(self.dialog, width=40)
        self.end_time_entry.pack(padx=20)

        tk.Label(self.dialog, text="优先级:").pack(pady=(10, 5), anchor="w", padx=20)
        priority_frame = tk.Frame(self.dialog)
        priority_frame.pack(padx=20)

        self.priority_var = tk.IntVar(value=2)
        tk.Radiobutton(priority_frame, text="低", variable=self.priority_var, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(priority_frame, text="中", variable=self.priority_var, value=2).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(priority_frame, text="高", variable=self.priority_var, value=3).pack(side=tk.LEFT)

        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="确定", width=10, command=self._on_ok).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="取消", width=10, command=self._on_cancel).pack(side=tk.LEFT, padx=10)

        self.dialog.bind("<Return>", lambda _: self._on_ok())
        self.dialog.bind("<Escape>", lambda _: self._on_cancel())

    def _on_ok(self):
        title = self.title_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        priority = self.priority_var.get()

        if not title:
            messagebox.showwarning("警告", "请输入任务名称")
            return

        if not start_time or not end_time:
            messagebox.showwarning("警告", "请输入开始和结束时间")
            return

        try:
            self.on_submit(title, start_time, end_time, priority)
        except ValueError as exc:
            messagebox.showwarning("警告", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("错误", f"添加行程失败: {exc}")
            return

        self.dialog.destroy()

    def _on_cancel(self):
        self.dialog.destroy()


class ScheduleApp:
    def __init__(self, root, service: SchedulerService):
        self.root = root
        self.service = service

        self.root.title("今日行程计划")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.selected_var = tk.IntVar(value=-1)
        self.visible_schedules = []

        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        title_frame.pack(fill=tk.X)

        today = datetime.now().strftime("%Y-%m-%d")
        title_label = tk.Label(
            title_frame,
            text=f"📅 今日行程计划        {today}",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg="#2c3e50",
            fg="white",
        )
        title_label.pack(pady=10)

        button_frame = tk.Frame(self.root, pady=10, bg="#ecf0f1")
        button_frame.pack(fill=tk.X)

        tk.Button(
            button_frame,
            text="+ 添加行程",
            width=15,
            bg="#3498db",
            fg="white",
            font=("Microsoft YaHei UI", 10),
            relief=tk.FLAT,
            command=self.add_schedule,
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            button_frame,
            text="🗑 删除选中",
            width=15,
            bg="#e74c3c",
            fg="white",
            font=("Microsoft YaHei UI", 10),
            relief=tk.FLAT,
            command=self.delete_schedule,
        ).pack(side=tk.RIGHT, padx=20)

        tk.Frame(self.root, height=2, bg="#bdc3c7").pack(fill=tk.X, pady=5)

        list_container = tk.Frame(self.root)
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(list_container, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.list_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        tk.Frame(self.root, height=2, bg="#bdc3c7").pack(fill=tk.X, pady=5)

        progress_frame = tk.Frame(self.root, pady=15, bg="#ecf0f1")
        progress_frame.pack(fill=tk.X)

        self.progress_label = tk.Label(progress_frame, text="进度: 0/0 (0%)", bg="#ecf0f1", font=("Microsoft YaHei UI", 9))
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(progress_frame, mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, padx=50)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Horizontal.TProgressbar", background="#2ecc71", troughcolor="#ecf0f1")

    def _on_frame_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def refresh(self):
        self.visible_schedules = sorted(self.service.list_today(), key=lambda x: x.start_time)
        self._render_schedules()
        self._update_progress()

    def add_schedule(self):
        AddScheduleDialog(self.root, self._on_schedule_added)

    def _on_schedule_added(self, title, start_time, end_time, priority):
        conflict = self.service.check_time_conflict(start_time, end_time)
        if conflict:
            confirm = messagebox.askyesno("时间冲突", f"该时间段与以下行程冲突：\n\n{conflict}\n\n是否继续添加？")
            if not confirm:
                return

        self.service.add_schedule(title, start_time, end_time, priority)
        self.selected_var.set(-1)
        self.refresh()

    def delete_schedule(self):
        selected = self.selected_var.get()
        if selected < 0 or selected >= len(self.visible_schedules):
            messagebox.showinfo("提示", "请先选择要删除的行程")
            return

        item = self.visible_schedules[selected]
        if messagebox.askyesno("确认", f"确定要删除「{item.title}」吗？"):
            self.service.delete_schedule(item.id)
            self.selected_var.set(-1)
            self.refresh()

    def toggle_complete(self, schedule_id):
        self.service.toggle_complete(schedule_id)
        self.refresh()

    def _render_schedules(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.visible_schedules:
            tk.Label(
                self.list_frame,
                text="📝 点击「+ 添加行程」开始规划您的一天",
                font=("Arial", 12),
                fg="#95a5a6",
                pady=20,
            ).pack(expand=True)
            return

        priority_map = {1: "低", 2: "中", 3: "高"}
        priority_color = {1: "#27ae60", 2: "#f39c12", 3: "#e74c3c"}

        for idx, schedule in enumerate(self.visible_schedules):
            row = tk.Frame(self.list_frame, pady=5)
            row.pack(fill=tk.X, pady=2)

            tk.Radiobutton(row, variable=self.selected_var, value=idx, width=2).pack(side=tk.LEFT, padx=2)

            var = tk.BooleanVar(value=schedule.completed)
            tk.Checkbutton(
                row,
                variable=var,
                command=lambda s=schedule: self.toggle_complete(s.id),
                width=3,
            ).pack(side=tk.LEFT, padx=5)

            tk.Label(
                row,
                text=f"{schedule.start_time} - {schedule.end_time}",
                font=("Arial", 10),
                width=18,
                anchor="w",
            ).pack(side=tk.LEFT)

            title_text = schedule.title
            if schedule.completed:
                title_text = f"~~{title_text}~~"

            tk.Label(row, text=title_text, font=("Arial", 10), anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

            tk.Label(
                row,
                text=f"[{priority_map.get(schedule.priority, '中')}]",
                fg=priority_color.get(schedule.priority, "#f39c12"),
                font=("Arial", 9, "bold"),
                width=6,
            ).pack(side=tk.LEFT, padx=5)

    def _update_progress(self):
        completed, total, percentage = self.service.progress(self.visible_schedules)
        self.progress_label.config(text=f"进度: {completed}/{total} ({percentage}%)")
        self.progress_bar["value"] = percentage
