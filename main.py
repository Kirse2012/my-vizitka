from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class PlayerScreen(BoxLayout):
    press = False
    def on_greeting(self):
        if self.press:
            self.ids.greeting_btn.text = "Привет"
            self.press = False
        else:
            self.ids.greeting_btn.text = "Ты нажал"
            self.press = True

    pass


class VizitkaApp(App):
    def build(self):
        return PlayerScreen()


VizitkaApp().run()
