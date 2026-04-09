import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from app.service import SchedulerService


class AddScheduleDialog:
    def __init__(self, parent, on_submit):
        self.on_submit = on_submit
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("添加行程")
        self.dialog.geometry("420x380")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # 设置圆角窗口效果（使用透明边框）
        self.dialog.configure(bg="#f8f9fa")

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (420 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (380 // 2)
        self.dialog.geometry(f"420x380+{x}+{y}")

        self._setup_ui()

    def _setup_ui(self):
        # 主容器
        container = tk.Frame(self.dialog, bg="#f8f9fa")
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # 标题
        tk.Label(
            container,
            text="✨ 添加新行程",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        ).pack(pady=(0, 15))

        # 任务名称
        tk.Label(container, text="任务名称", font=("Microsoft YaHei UI", 9), bg="#f8f9fa", fg="#5a6c7d").pack(anchor="w")
        self.title_entry = tk.Entry(
            container,
            font=("Microsoft YaHei UI", 10),
            relief=tk.FLAT,
            bd=0,
            bg="white",
            highlightthickness=1,
            highlightcolor="#6366f1",
            highlightbackground="#e2e8f0"
        )
        self.title_entry.pack(fill=tk.X, pady=(5, 15))

        # 时间选择区域
        time_container = tk.Frame(container, bg="#f8f9fa")
        time_container.pack(fill=tk.X, pady=(0, 15))

        # 开始时间
        start_frame = tk.Frame(time_container, bg="#f8f9fa")
        start_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(start_frame, text="开始时间", font=("Microsoft YaHei UI", 9), bg="#f8f9fa", fg="#5a6c7d").pack(anchor="w")
        self.start_hour = self._create_spinbox(start_frame, 0, 23)
        self.start_minute = self._create_spinbox(start_frame, 0, 59)

        # 结束时间
        end_frame = tk.Frame(time_container, bg="#f8f9fa")
        end_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(end_frame, text="结束时间", font=("Microsoft YaHei UI", 9), bg="#f8f9fa", fg="#5a6c7d").pack(anchor="w")
        self.end_hour = self._create_spinbox(end_frame, 0, 23)
        self.end_minute = self._create_spinbox(end_frame, 0, 59)

        # 优先级选择
        tk.Label(container, text="优先级", font=("Microsoft YaHei UI", 9), bg="#f8f9fa", fg="#5a6c7d").pack(anchor="w")
        priority_frame = tk.Frame(container, bg="#f8f9fa")
        priority_frame.pack(fill=tk.X, pady=(5, 15))

        self.priority_var = tk.IntVar(value=2)

        # 优先级按钮
        for idx, (text, color) in enumerate([("低", "#10b981"), ("中", "#f59e0b"), ("高", "#ef4444")], 1):
            btn = tk.Frame(priority_frame, bg=color, cursor="hand2")
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8 if idx < 3 else 0))
            btn.bind("<Button-1>", lambda _, v=idx: self._select_priority(v))

            tk.Label(
                btn,
                text=text,
                font=("Microsoft YaHei UI", 9, "bold"),
                bg=color,
                fg="white",
                cursor="hand2"
            ).pack(expand=True)

        self._priority_buttons = priority_frame.winfo_children()[::2]  # 获取按钮Frame

        # 按钮
        button_frame = tk.Frame(container, bg="#f8f9fa")
        button_frame.pack(fill=tk.X)

        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            font=("Microsoft YaHei UI", 9),
            bg="white",
            fg="#5a6c7d",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._on_cancel
        )
        cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        confirm_btn = tk.Button(
            button_frame,
            text="✓ 添加",
            font=("Microsoft YaHei UI", 9, "bold"),
            bg="#6366f1",
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._on_ok
        )
        confirm_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))

        # 初始化优先级按钮状态
        self._select_priority(2)

        # 绑定快捷键
        self.dialog.bind("<Return>", lambda _: self._on_ok())
        self.dialog.bind("<Escape>", lambda _: self._on_cancel())

    def _create_spinbox(self, parent, from_, to):
        """创建时间选择器"""
        values = [f"{i:02d}" for i in range(from_, to + 1)]
        spinbox = ttk.Spinbox(parent, values=values, width=5, font=("Microsoft YaHei UI", 10))
        spinbox.pack(side=tk.LEFT, padx=2)
        return spinbox

    def _select_priority(self, value):
        """选择优先级"""
        self.priority_var.set(value)
        for i, btn in enumerate(self._priority_buttons):
            bg = btn.cget("bg")
            new_bg = bg
            if i + 1 == value:
                # 选中状态：保持原色，加深
                if i == 0:
                    new_bg = "#059669"
                elif i == 1:
                    new_bg = "#d97706"
                else:
                    new_bg = "#dc2626"
            else:
                # 未选中状态：变浅
                if i == 0:
                    new_bg = "#d1fae5"
                elif i == 1:
                    new_bg = "#fde68a"
                else:
                    new_bg = "#fca5a5"
            btn.configure(bg=new_bg)
            # 更新Label颜色
            for child in btn.winfo_children():
                child.configure(
                    bg=new_bg,
                    fg="white" if i + 1 == value else "#5a6c7d"
                )

    def _on_ok(self):
        title = self.title_entry.get().strip()
        start_time = f"{self.start_hour.get()}:{self.start_minute.get()}"
        end_time = f"{self.end_hour.get()}:{self.end_minute.get()}"
        priority = self.priority_var.get()

        if not title:
            messagebox.showwarning("提示", "请输入任务名称")
            return

        try:
            self.on_submit(title, start_time, end_time, priority)
        except ValueError as exc:
            messagebox.showwarning("提示", str(exc))
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
        # 标题栏 - 渐变色效果
        title_frame = tk.Frame(self.root, bg="white", height=70)
        title_frame.pack(fill=tk.X)

        # 左侧装饰色块
        decor_frame = tk.Frame(title_frame, bg="#6366f1", width=6)
        decor_frame.pack(side=tk.LEFT, fill=tk.Y)

        title_container = tk.Frame(title_frame, bg="white")
        title_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

        today = datetime.now().strftime("%Y-%m-%d")
        tk.Label(
            title_container,
            text="📅 今日行程计划",
            font=("Microsoft YaHei UI", 16, "bold"),
            bg="white",
            fg="#1e293b"
        ).pack(anchor="w", pady=(15, 3))

        tk.Label(
            title_container,
            text=today,
            font=("Microsoft YaHei UI", 10),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w")

        # 按钮区域
        button_frame = tk.Frame(self.root, pady=15, bg="white")
        button_frame.pack(fill=tk.X)

        tk.Button(
            button_frame,
            text="+ 添加行程",
            width=18,
            bg="#6366f1",
            fg="white",
            font=("Microsoft YaHei UI", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.add_schedule,
        ).pack(side=tk.LEFT, padx=25)

        tk.Button(
            button_frame,
            text="🗑 删除选中",
            width=18,
            bg="#f1f5f9",
            fg="#64748b",
            font=("Microsoft YaHei UI", 10),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.delete_schedule,
        ).pack(side=tk.RIGHT, padx=25)

        # 分隔线
        tk.Frame(self.root, height=1, bg="#e2e8f0").pack(fill=tk.X)

        # 列表区域
        list_container = tk.Frame(self.root, bg="white")
        list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(list_container, highlightthickness=0, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.list_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # 分隔线
        tk.Frame(self.root, height=1, bg="#e2e8f0").pack(fill=tk.X)

        # 进度区域
        progress_frame = tk.Frame(self.root, pady=20, bg="white")
        progress_frame.pack(fill=tk.X)

        self.progress_label = tk.Label(progress_frame, text="进度: 0/0 (0%)", bg="white", font=("Microsoft YaHei UI", 9), fg="#64748b")
        self.progress_label.pack(pady=(0, 10))

        self.progress_bar = ttk.Progressbar(progress_frame, mode="determinate", style="Modern.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, padx=25)

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Modern.Horizontal.TProgressbar",
            background="#6366f1",
            troughcolor="#f1f5f9",
            borderwidth=0,
            thickness=8
        )

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
                font=("Microsoft YaHei UI", 11),
                fg="#94a3b8",
                pady=30,
                bg="white"
            ).pack(expand=True)
            return

        priority_map = {1: "低", 2: "中", 3: "高"}
        priority_bg = {1: "#ecfdf5", 2: "#fffbeb", 3: "#fef2f2"}
        priority_fg = {1: "#059669", 2: "#d97706", 3: "#dc2626"}

        for idx, schedule in enumerate(self.visible_schedules):
            # 行程卡片
            card = tk.Frame(
                self.list_frame,
                bg="#f8fafc",
                pady=12,
                padx=15
            )
            card.pack(fill=tk.X, pady=6)

            # 左侧优先级色条
            tk.Frame(
                card,
                bg=priority_fg.get(schedule.priority, "#64748b"),
                width=4
            ).pack(side=tk.LEFT, fill=tk.Y)

            # 内容区
            content = tk.Frame(card, bg="#f8fafc")
            content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12)

            # 单选按钮
            tk.Radiobutton(
                content,
                variable=self.selected_var,
                value=idx,
                bg="#f8fafc",
                activebackground="#f8fafc"
            ).pack(side=tk.LEFT, padx=(0, 8))

            # 时间标签
            tk.Label(
                content,
                text=f"{schedule.start_time} - {schedule.end_time}",
                font=("Microsoft YaHei UI", 10, "bold"),
                bg="#f8fafc",
                fg="#334155"
            ).pack(side=tk.LEFT, padx=(0, 15))

            # 任务名称
            title_text = schedule.title
            title_fg = "#334155"
            if schedule.completed:
                title_text = f"✓ {title_text}"
                title_fg = "#94a3b8"

            tk.Label(
                content,
                text=title_text,
                font=("Microsoft YaHei UI", 10),
                bg="#f8fafc",
                fg=title_fg
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

            # 优先级标签
            tk.Label(
                card,
                text=priority_map.get(schedule.priority, "中"),
                font=("Microsoft YaHei UI", 8, "bold"),
                bg=priority_bg.get(schedule.priority, "#f1f5f9"),
                fg=priority_fg.get(schedule.priority, "#64748b"),
                padx=8,
                pady=2
            ).pack(side=tk.RIGHT)

    def _update_progress(self):
        completed, total, percentage = self.service.progress(self.visible_schedules)
        self.progress_label.config(text=f"进度: {completed}/{total} ({percentage}%)")
        self.progress_bar["value"] = percentage
