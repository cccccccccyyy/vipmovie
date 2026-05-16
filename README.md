# VIP视频解析

粘贴视频链接，自动跳转解析页面播放。支持 Windows / Linux / Android。

## 下载

| 平台 | 文件 | 大小 |
|------|------|------|
| Windows | [vipmovie-windows.exe](https://github.com/cccccccccyyy/vipmovie/releases/latest/download/vipmovie-windows.exe) | 11MB |
| Linux | [vipmovie-linux](https://github.com/cccccccccyyy/vipmovie/releases/latest/download/vipmovie-linux) | 22MB |
| Android | [vipmovie-android.apk](https://github.com/cccccccccyyy/vipmovie/releases/latest/download/vipmovie-android.apk) | 22MB |

## 使用

### Windows
双击 `vipmovie-windows.exe` → 粘贴链接 → 回车 → 浏览器打开播放

### Linux
```bash
chmod +x vipmovie-linux
./vipmovie-linux
```

### Android
安装 APK → 打开 → 粘贴链接 → 点击「立即解析」→ 跳转浏览器

## 开发

```bash
git clone https://github.com/cccccccccyyy/vipmovie.git
cd vipmovie
pip install -r requirements.txt
python vipmovie.py        # 桌面终端版
python main.py            # Kivy 图形版（需 pip install kivy）
```

推送即自动构建：GitHub Actions 编译三平台产物，去 [Actions](https://github.com/cccccccccyyy/vipmovie/actions) 下载。

## 架构

```
core.py        共享逻辑（API 调用）
├── vipmovie.py 桌面端终端入口
└── main.py     Android Kivy GUI 入口
```

## 技术栈

Python · requests · BeautifulSoup4 · Kivy · PyInstaller · Buildozer · Docker · GitHub Actions

## 许可证

MIT
