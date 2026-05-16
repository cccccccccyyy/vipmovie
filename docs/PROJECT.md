# VIP视频解析 - 技术文档

## 项目概述

一款跨平台 VIP 视频解析工具。用户粘贴视频链接后自动调用第三方解析接口，在系统默认浏览器中播放。支持 **Windows / Linux / Android** 三平台。

## 需求演进

| 阶段 | 需求 | 解决方案 |
|------|------|----------|
| 1 | 初始脚本，硬编码 Windows Edge 路径，仅单人能用 | - |
| 2 | 跨平台，任何人直接能用 | `webbrowser` 替换 `DrissionPage` |
| 3 | 打包为独立可执行文件分发 | PyInstaller (Win/Linux) + Buildozer (Android) |
| 4 | Android 必须打 APK，一键安装 | Kivy GUI + Buildozer + Docker |
| 5 | 中文字体显示正常 | 系统字体自动检测，多路径 fallback |
| 6 | 自动构建，推送即出包 | GitHub Actions 三平台 CI |

## 架构设计

```
core.py          共享逻辑层（获取解析接口）
├── vipmovie.py  桌面端终端入口 (Windows / Linux)
└── main.py      Android Kivy GUI 入口
```

### 分层说明

- **core.py**：调用 `https://www.niudh.cn/tools/vip/` 获取可用的 VIP 解析接口 URL
- **vipmovie.py**：`while True` 循环读取用户输入，拼接 URL 后用 `webbrowser.open()` 打开
- **main.py**：Kivy 图形界面，支持 Android；自动检测并使用系统中文字体

### 为什么桌面端和 Android 用不同入口

| | 桌面端 | Android |
|---|---|---|
| 交互方式 | 终端 `input()` | Kivy GUI |
| 产物大小 | 11MB (Win) / 22MB (Linux) | 22MB APK |
| 打包工具 | PyInstaller | Docker + Buildozer |
| 构建时间 | ~45s | ~15min |
| 字体方案 | 系统字体 | 自动检测 `/system/fonts/DroidSansFallback.ttf` |

桌面端保持终端交互有两个原因：Kivy 在 Windows 上编译缓慢（PyInstaller 打包 Kivy 需 30+ 分钟），且桌面用户对终端操作接受度高。

## 构建流水线

```
git push → GitHub Actions
  ├── build-windows  (windows-latest, PyInstaller, 45s)
  ├── build-linux    (ubuntu-latest,  PyInstaller, 45s)
  └── build-android  (ubuntu-latest,  Docker kivy/buildozer, 15min)
```

### Android 构建优化历程

| 尝试 | 方案 | 结果 |
|------|------|------|
| 1 | 本地 Buildozer | NDK 版本 404，许可证未接受 |
| 2 | GitHub Actions + Buildozer | `LT_SYS_SYMBOL_USCORE` 宏未定义 |
| 3 | 注入 autoconf 兼容宏 + Python 3.12 | 编译成功但 hostpython 耗时 >30min |
| 4 | **Docker kivy/buildozer 镜像** | 最终采用方案，环境预配置，缓存 SDK/NDK |

### CI 缓存策略

```yaml
~/.buildozer  # Android SDK / NDK，按 buildozer.spec hash 缓存
~/.gradle     # Gradle 分发版缓存
```

首次冷构建 ~20 分钟，热构建（缓存命中）~5-10 分钟。

## 关键问题与解决方案

### 问题 1：硬编码 Windows 浏览器路径

**现象**：脚本硬编码了特定浏览器的安装路径，仅限开发者的电脑能运行

**解决**：用 Python 内置 `webbrowser.open()` 替代，零依赖、全平台自动调用系统默认浏览器

### 问题 2：Android NDK 版本不存在

**现象**：`android-ndk-r25.2.9519653-linux.zip` → HTTP 404

**解决**：注释 `android.ndk`，让 Buildozer 自动选择可用版本（最终选用 r28c）

### 问题 3：Android SDK 许可证未接受

**现象**：`build-tools;37.0.0 could not be installed`

**解决**：`buildozer.spec` 添加 `android.accept_sdk_license = True`

### 问题 4：autoconf 宏 LT_SYS_SYMBOL_USCORE 未定义

**现象**：Python 3.11 源码 `configure.ac` 引用了新版 libtool 已移除的宏

**解决**：
- CI 中注入兼容宏：`AC_DEFUN([LT_SYS_SYMBOL_USCORE], ...)`
- 升级到 Python 3.12：`p4a.python_version = 3.12`

### 问题 5：APK 入口文件问题

**现象**：python-for-android 要求入口文件必须为 `main.py`

**解决**：创建 `main.py` 作为 Kivy App 入口

### 问题 6：Android 中文显示为方块

**现象**：Kivy 默认字体（Roboto）不含 CJK 字符

**解决**：启动时自动检测系统字体路径：
```
Android:  /system/fonts/DroidSansFallback.ttf
Windows:  C:\Windows\Fonts\msyh.ttc
Linux:    /usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf
```
通过 `LabelBase.register()` 注册后全局使用，避免打包 19MB 字体文件。

### 问题 7：GitHub 网络不可达

**现象**：国内网络间歇性无法连接 github.com:443

**解决**：通过 Git HTTP 代理配置使推送命令走代理通道访问 GitHub

### 问题 8：Kivy Windows 构建极慢

**现象**：PyInstaller 打包 Kivy 在 GitHub Actions Windows runner 上 >30 分钟

**解决**：桌面端回归终端版（`vipmovie.py`），避免 Kivy 在 Windows 上的编译开销

## 代码审计结果

| 文件 | 行数 | 职责 | 评分 |
|------|------|------|------|
| `core.py` | 9 | API 调用 | 简洁，无冗余 |
| `vipmovie.py` | 9 | 桌面端入口 | 极简，循环无退出 |
| `main.py` | 77 | Android Kivy UI + 字体 | 结构清晰，平台检测合理 |
| `buildozer.spec` | 30 | Android 打包配置 | 已清理重复字段 |
| `build.yml` | 95 | CI 三平台构建 | 并行作业，缓存策略正确 |

- 无安全漏洞（无用户输入执行、无文件操作、仅 HTTP GET）
- 无性能问题（单次网络请求，浏览器打开后脚本无额外消耗）
- 依赖最小化：桌面端 2 个外部依赖，Android 4 个

## 技术栈

| 组件 | 用途 |
|------|------|
| Python 3.11+ | 核心语言 |
| requests | HTTP 请求 |
| BeautifulSoup4 | HTML 解析 |
| Kivy | Android GUI 框架 |
| PyInstaller | 桌面端打包 |
| Buildozer | Android APK 打包 |
| Docker | CI 中环境隔离 |
| GitHub Actions | CI/CD |

## 项目文件结构

```
VIPMoive/
├── core.py                          # 共享逻辑
├── vipmovie.py                      # 桌面端入口
├── main.py                          # Android Kivy 入口
├── buildozer.spec                   # Android 构建配置
├── requirements.txt                 # Python 依赖
├── icon.png                         # 应用图标
├── 原神.png                          # 原始图标
├── fonts/.gitkeep                   # 字体目录占位
├── .gitignore
├── .github/workflows/build.yml      # CI 构建流水线
├── dist/release/                    # 最终产物
│   ├── vipmovie-windows.exe
│   ├── vipmovie-linux
│   └── vipmovie-android.apk
├── docs/
│   └── PROJECT.md                   # 本文档
└── README.md                        # 项目说明
```
