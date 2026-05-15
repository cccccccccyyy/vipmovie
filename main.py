import os
import sys
import webbrowser

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from core import get_vip_url

ZH_FONT = 'ChineseFont'


def _find_chinese_font():
    candidates = []
    if hasattr(sys, 'getandroidapilevel'):
        candidates = [
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/NotoSansCJK-Regular.ttc',
        ]
    elif sys.platform == 'win32':
        candidates = [
            os.path.expandvars(r'%SystemRoot%\Fonts\msyh.ttc'),
            os.path.expandvars(r'%SystemRoot%\Fonts\simhei.ttf'),
            os.path.expandvars(r'%SystemRoot%\Fonts\simsun.ttc'),
        ]
    else:
        candidates = [
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        ]
    candidates.append('fonts/DroidSansFallback.ttf')
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def _setup_font():
    font_path = _find_chinese_font()
    if font_path:
        LabelBase.register(ZH_FONT, fn_regular=font_path)
        return ZH_FONT
    return None


DEFAULT_FONT = _setup_font()


class VipMovieApp(App):
    def build(self):
        self.vip_url = get_vip_url()
        font_args = {'font_name': DEFAULT_FONT} if DEFAULT_FONT else {}
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        layout.add_widget(Label(
            text='VIP视频解析', font_size=24, size_hint=(1, 0.2),
            **font_args))
        self.url_input = TextInput(
            hint_text='请粘贴电影网址', multiline=False,
            size_hint=(1, 0.15), **font_args)
        layout.add_widget(self.url_input)
        btn = Button(text='立即解析', size_hint=(1, 0.2), **font_args)
        btn.bind(on_press=self.parse)
        layout.add_widget(btn)
        layout.add_widget(Label(text='', size_hint=(1, 0.45)))
        return layout

    def parse(self, instance):
        webbrowser.open(self.vip_url + self.url_input.text)


if __name__ == '__main__':
    VipMovieApp().run()
