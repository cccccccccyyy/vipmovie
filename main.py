import webbrowser

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from core import get_vip_url


class VipMovieApp(App):
    def build(self):
        self.vip_url = get_vip_url()
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        layout.add_widget(Label(
            text='VIP视频解析', font_size=24, size_hint=(1, 0.2)))
        self.url_input = TextInput(
            hint_text='请粘贴电影网址', multiline=False, size_hint=(1, 0.15))
        layout.add_widget(self.url_input)
        btn = Button(text='立即解析', size_hint=(1, 0.2))
        btn.bind(on_press=self.parse)
        layout.add_widget(btn)
        layout.add_widget(Label(text='', size_hint=(1, 0.45)))
        return layout

    def parse(self, instance):
        webbrowser.open(self.vip_url + self.url_input.text)


if __name__ == '__main__':
    VipMovieApp().run()
