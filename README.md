# Daily Scheduler - 每日行程计划工具

一个简单易用的桌面行程管理应用，帮助您规划和管理每日任务。

## 功能特性

- 添加行程任务（任务名、起止时间、优先级）
- 勾选任务完成状态
- 删除选中任务
- 实时进度统计
- 时间冲突提醒（可选择继续添加）
- 本地 JSON 持久化

## 运行模式

### 模式 A：最终用户（推荐）

无需安装 Python，直接运行打包后的 `DailyScheduler.exe`。

### 模式 B：开发者模式

安装 Python 后运行源码：

```bash
python main.py
```

## 快速启动（Windows）

双击 `start.bat`，启动优先级如下：

1. `DailyScheduler.exe`
2. `dist\\DailyScheduler.exe`
3. `python main.py`（当本机安装了 Python）

## 打包 EXE（Windows）

### 方式 1：一键脚本

双击 `build_exe.bat`，完成安装 PyInstaller 和打包。

### 方式 2：命令行

```bash
python -m pip install -r requirements-build.txt
python -m PyInstaller --noconfirm --clean --onefile --noconsole --name DailyScheduler main.py
```

打包产物：`dist\\DailyScheduler.exe`

## 生成安装包（Windows）

### 前置条件

1. 先完成 EXE 打包（确保 `dist\\DailyScheduler.exe` 存在）
2. 安装 Inno Setup 6（含 `ISCC.exe`）

### 一键生成安装包

双击 `build_installer.bat`

安装包产物目录：`installer\\output`

## GitHub Actions 自动打包（推荐）

已内置工作流文件：`.github/workflows/windows-build.yml`

触发方式：

1. 推送到 `main` 分支自动触发
2. 在 GitHub 仓库 `Actions -> Build Windows App -> Run workflow` 手动触发

构建完成后可在对应的 Action 运行页下载两个产物：

- `DailyScheduler-exe`
- `DailyScheduler-setup`

## 数据存储位置

- Windows：`%APPDATA%\\DailyScheduler\\scheduler.json`
- 非 Windows 回退：程序当前目录下 `scheduler.json`

备份与恢复：复制/替换 `scheduler.json` 文件即可。

## 项目结构

```text
daily-scheduler/
├── app/
│   ├── models.py           # 数据模型
│   ├── service.py          # 业务逻辑层
│   ├── storage.py          # 存储层
│   └── ui.py               # Tkinter 界面层
├── main.py                 # 启动入口
├── start.bat               # 启动脚本（优先 EXE）
├── build_exe.bat           # Windows 打包脚本
├── build_installer.bat     # Windows 安装包构建脚本
├── installer/
│   └── daily_scheduler.iss # Inno Setup 安装脚本
├── INSTALLER.md            # 安装包方案说明
├── requirements-build.txt  # 打包依赖
├── TESTING.md              # 测试文档
└── README.md               # 使用说明
```

## 常见问题

**Q: 用户机器没有 Python，能运行吗？**  
A: 可以，分发 `DailyScheduler.exe` 即可。

**Q: 为什么双击 `start.bat` 没反应？**  
A: 请先确认同目录存在 `DailyScheduler.exe` 或 `dist\\DailyScheduler.exe`；若都不存在，请先执行 `build_exe.bat`。

**Q: 数据会丢失吗？**  
A: 数据存储在本地 JSON 文件，不卸载系统配置目录通常不会丢失。

## 版本信息

- 版本：1.1.0
- 更新日期：2026-04-09
- 适用系统：Windows 10/11
