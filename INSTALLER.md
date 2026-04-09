# 安装包方案（Windows）

本项目使用 **Inno Setup 6** 生成安装程序（`.exe` 安装向导）。

## 目标

- 用户机器无需安装 Python。
- 安装后可从开始菜单和桌面快捷方式启动。
- 支持标准卸载流程。

## 前置条件

1. 已完成 EXE 打包，存在 `dist\DailyScheduler.exe`
2. 已安装 Inno Setup 6（包含 `ISCC.exe`）

## 一键构建安装包

在项目根目录双击：

`build_installer.bat`

构建成功后，输出目录为：

`installer\output`

## 安装包行为

- 默认安装目录：`%LOCALAPPDATA%\Programs\Daily Scheduler`
- 启动入口：`DailyScheduler.exe`
- 创建开始菜单快捷方式
- 可选创建桌面快捷方式
- 安装完成可直接运行应用

## 卸载行为

- 通过“应用和功能”或卸载程序移除安装目录文件。
- 用户数据保存在 `%APPDATA%\DailyScheduler\scheduler.json`，默认不随卸载删除。

