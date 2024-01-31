from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import time

class TestApp(App):
    def build(self):
        self.last_click_time = 0
        self.count = 0
        self.label = Label(text='Nombre de clics: 0')
        self.button = Button(text='Cliquez-moi')
        self.button.bind(on_press=self.increment_on_press)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.button)

        return layout

    def increment_on_press(self, instance):
        # Vérifier si le dernier clic était il y a plus de 0.3 secondes
        if time.time() - self.last_click_time > 0.3:
            self.count += 1
            self.label.text = f'Nombre de clics: {self.count}'
            self.last_click_time = time.time()

if __name__ == '__main__':
    TestApp().run()

