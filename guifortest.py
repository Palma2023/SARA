from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard
import send_mail
import send_sms
import lire_valeur

class InterfaceApp(App):
    
    def read_value_button_pressed(self,instance):
        lire_valeur.read_value()
    
    def send_sms_button_pressed(self,instance):
        send_sms.sendSms()
    
    def send_mail_button_pressed(self, instance):
        text = "Bonjour, nous vous informons que le seuil d'alarme a été atteint, veuillez contrôler l'équipement"
        subject = "ALERTE SURVEILLANCE EQUIPEMENT"
        send_mail.sendMail(subject,text)

    def build(self):
        self.val_ref = None  # Variable to store the input value
        self.value_type = None  # Keep track of the type of value being entered
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical')

        # Top section
        top_section = BoxLayout(orientation='horizontal')
        top_left = Button(text='DEFINIR UN SEUIL D\'ALARME\nMenu:\n-Analogique\n-Numerique\nPuis saisir la valeur')
        top_left.bind(on_release=self.show_value_input_menu)  # Bind this button to show the value input menu
        top_right = Button(text='LIRE UNE VALEUR ET\nL\'AFFICHER')
        top_right.bind(on_release=self.read_value_button_pressed)
        top_section.add_widget(top_left)
        top_section.add_widget(top_right)
        
        # Bottom section
        bottom_section = BoxLayout(orientation='horizontal')
        bottom_left = Button(text='LISTE DES CONTACTS')
        bottom_right = BoxLayout(orientation='vertical')
        email_button = Button(text='ENVOYER UN EMAIL')
        email_button.bind(on_release=self.send_mail_button_pressed)
        sms_button = Button(text='ENVOYER UN SMS')
        sms_button.bind(on_release=self.send_sms_button_pressed)
        call_button = Button(text='PASSER UN APPEL')
        bottom_right.add_widget(email_button)
        bottom_right.add_widget(sms_button)
        bottom_right.add_widget(call_button)
        bottom_section.add_widget(bottom_left)
        bottom_section.add_widget(bottom_right)
        
        # Combine sections
        main_layout.add_widget(top_section)
        # You might need to add some logic here to create spacing
        main_layout.add_widget(bottom_section)
        
        return main_layout

    def show_value_input_menu(self, instance):
        # Create the content for the popup
        content = BoxLayout(orientation='vertical')
        analog_button = Button(text='Valeur analogique')
        digital_button = Button(text='Valeur numérique')
        analog_button.bind(on_release=lambda btn: self.show_keyboard('analog'))
        digital_button.bind(on_release=lambda btn: self.show_keyboard('digital'))
        content.add_widget(analog_button)
        content.add_widget(digital_button)

        # Create the popup
        self.popup = Popup(title='Choisir type de valeur', content=content, size_hint=(0.8, 0.5))
        self.popup.open()

    def show_keyboard(self, value_type):
        self.popup.dismiss()  # Dismiss the value type menu
        self.value_type = value_type  # Set the type of value being entered
        self.vkeyboard = VKeyboard()
        self.vkeyboard.bind(on_key_up=self.on_keyboard_up)

        # Create a popup for the keyboard
        self.keyboard_popup = Popup(title=f'Saisir la valeur ({value_type})', content=self.vkeyboard, size_hint=(1, 0.5))
        self.keyboard_popup.open()

    def on_keyboard_up(self, keyboard, keycode, text, modifiers):
        # Validate the input based on the type of value
        if self.value_type == 'analog':
            if text in ('1', '0'):
                self.val_ref = text
                self.keyboard_popup.dismiss()
            else:
                # Invalid input; could show an error message or clear the keyboard
                self.vkeyboard.text = ''
        elif self.value_type == 'digital':
            if text.isdigit() and len(text) <= 5:
                self.val_ref = text
                self.keyboard_popup.dismiss()
            else:
                # Invalid input; could show an error message or clear the keyboard
                self.vkeyboard.text = ''
        print("Value entered:", self.val_ref)  # Just for demonstration
        
if __name__ == '__main__':
    InterfaceApp().run()

