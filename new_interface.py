from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import threading
import lire_valeur
import send_sms
import time
import read_analog

# Sous-classe DebouncedTextInput pour éviter la double saisie
class DebouncedTextInput(TextInput):
    def __init__(self, **kwargs):
        super(DebouncedTextInput, self).__init__(**kwargs)
        self.last_insert = ''
        self.last_time = 0
        self.debounce_duration = 0.3  # 300 ms

    def insert_text(self, substring, from_undo=False):
        current_time = time.time()
        if substring == self.last_insert and (current_time - self.last_time) <= self.debounce_duration:
            return
        super(DebouncedTextInput, self).insert_text(substring, from_undo)
        self.last_insert = substring
        self.last_time = current_time

class ValuePopup(Popup):
    def __init__(self, **kwargs):
        super(ValuePopup, self).__init__(**kwargs)
        self.content = Label(text="Initialisation...")
        self.title = "Valeur Actuelle"
        self.size_hint = (None, None)
        self.size = (400, 200)

    def update_value(self, value):
        self.content.text = f"Valeur actuelle: {value}"

class AlarmApp(App):
    def build(self):
        self.last_submit_time = 0
        self.layout = BoxLayout(orientation='vertical')
        self.value_input = DebouncedTextInput(hint_text='Valeur d\'alarme', input_type='number')
        self.pin_input = DebouncedTextInput(hint_text='Numéro du pin', input_type='number')
        self.submit_button = Button(text='Configurer')
        self.submit_button.bind(on_press=self.setup_alarm)

        self.layout.add_widget(self.value_input)
        self.layout.add_widget(self.pin_input)
        self.layout.add_widget(self.submit_button)

        self.popup = ValuePopup()
        return self.layout

    def check_alarm(self, alarm_value, pin_number):
        if (alarm_value != 1 or 0):
            while True:
                gpio_value = read_analog.read_analog(pin_number)
                Clock.schedule_once(lambda dt: self.popup.update_value(gpio_value))
                if gpio_value < alarm_value:
                    send_sms.sendSms()   
        else: 
            while True:
                gpio_value = lire_valeur.read_value(pin_number)
                Clock.schedule_once(lambda dt: self.popup.update_value(gpio_value))
                if gpio_value != alarm_value:
                    send_sms.sendSms()

    def setup_alarm(self, instance):
        current_time = time.time()
        if current_time - self.last_submit_time > 0.3:  # Debounce de 0.3 secondes
            alarm_value = float(self.value_input.text)
            pin_number = int(self.pin_input.text)

            self.popup.open()
            alarm_thread = threading.Thread(target=self.check_alarm, args=(alarm_value, pin_number))
            alarm_thread.daemon = True
            alarm_thread.start()

            self.last_submit_time = current_time

if __name__ == '__main__':
    AlarmApp().run()
