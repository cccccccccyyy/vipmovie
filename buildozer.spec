[app]

title = VIP视频解析
package.name = vipmovie
package.domain = org.vipmovie
source.dir = .
source.include_exts = py
source.include_patterns = core.py,main.py
version = 1.0

requirements = python3,kivy,requests,beautifulsoup4

orientation = portrait
fullscreen = 0
window_clearcolor = 000000

icon.filename = icon.png

# Android permissions
android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.python_version = 3.12
# android.ndk = auto (let buildozer choose)
android.gradle_dependencies = androidx.webkit:webkit:1.8.0

log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
