from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.behaviors import DragBehavior
import threading
import lire_valeur
import send_sms
import time
import read_analog
import manage_contact
import csv
import send_mail

# class DraggableBar(DragBehavior, BoxLayout):
#     pass

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

class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)
        self.last_submit_time = 0
        # scroll_view = ScrollView()

        # scroll_layout = BoxLayout(orientation='vertical', size_hint_y=1.5, spacing=5)
        # scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        self.layout = BoxLayout(orientation='vertical', size_hint_y=1,spacing=5)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.name_contact = DebouncedTextInput(hint_text='Nom du contact', input_type='text',size_hint_y=None, height=100)
        self.num_contact = DebouncedTextInput(hint_text='Numéro du contact', input_type='tel',size_hint_y=None, height=100)
        self.mail_contact = DebouncedTextInput(hint_text='Mail du contact', input_type='text',size_hint_y=None, height=100)
        self.submit_button = Button(text='Ajouter contact',size_hint=(1, None), height=80)
        self.submit_button.bind(on_press=self.add_contact)

        # Adding a back button
        self.back_button = Button(text='Retour',height=30)
        self.back_button.bind(on_press=self.go_back)

        self.layout.add_widget(self.name_contact)
        self.layout.add_widget(self.num_contact)
        self.layout.add_widget(self.mail_contact)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

        # # Add the BoxLayout to the ScrollView
        # scroll_layout.add_widget(self.layout)

        # # Add the ScrollView to the main screen
        # scroll_view.add_widget(scroll_layout)
        # self.add_widget(scroll_view)


    def add_contact(self, instance):
        name_contact = self.name_contact.text
        num_contact = self.num_contact.text
        mail_contact = self.mail_contact.text

        contact=(name_contact,mail_contact,num_contact)
        manage_contact.ajouter_contact(contact, fichier='contacts.csv')

        # Reload the contact list on the ContactListScreen
        contact_list_screen = self.manager.get_screen('contact_list')
        contact_list_screen.reload_contacts(instance)

        self.name_contact.text = ''
        self.num_contact.text = ''
        self.mail_contact.text = ''

    def go_back(self, instance):
        # Navigate back to the HomeScreen
        self.manager.current = 'home'

class ContactListScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactListScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=2, spacing=10)  # Set the number of columns to 2
        self.contact_buttons = []
        self.selected_contact = None
        selected_phone_number = None
        selected_email = None

        # Populate contact buttons dynamically from the CSV file
        contacts = manage_contact.lire_contacts(fichier='contacts.csv')
        for contact in contacts:
            btn_contact = Button(text=f'{contact.get_nom()} - {contact.get_telephone()}')
            btn_contact.bind(on_press=lambda instance, contact=contact: self.select_contact(contact))
            self.contact_buttons.append(btn_contact)
            self.layout.add_widget(btn_contact)

        #Delete button
        delete_button = Button(text='Supprimer')
        delete_button.bind(on_press=lambda instance: self.delete_contact(instance))
        self.layout.add_widget(delete_button)

        # Back button to return to the home screen
        back_button = Button(text='Retour')
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)
    
    def select_contact(self, contact):
        # Set the selected contact attribute
        self.selected_contact = contact
        #print(f"Selected contact: {contact.get_nom()} - {contact.get_telephone()}")
        ContactListScreen.selected_phone_number = contact.get_telephone()
        ContactListScreen.selected_email = contact.get_email()
        print(ContactListScreen.selected_email)
        print(ContactListScreen.selected_phone_number)

    def delete_contact(self, instance):
        if self.selected_contact:
            manage_contact.supprimer_contact(contact_to_delete=self.selected_contact, fichier='contacts.csv')
            self.manager.current = 'contact_list'
            self.manager.current_screen.reload_contacts(instance)

    def reload_contacts(self, instance):
        self.layout.clear_widgets()
        self.contact_buttons = []
        contacts = manage_contact.lire_contacts(fichier='contacts.csv')
        for contact in contacts:
            btn_contact = Button(text=f'{contact.get_nom()} - {contact.get_telephone()}')
            btn_contact.bind(on_press=lambda instance, contact=contact: self.select_contact(contact))
            self.contact_buttons.append(btn_contact)
            self.layout.add_widget(btn_contact)
        self.layout.add_widget(Button(text='Supprimer contact', on_press=self.delete_contact))
        self.layout.add_widget(Button(text='Retour', on_press=self.go_back))

    def go_back(self, instance):
        # Navigate back to the HomeScreen
        self.manager.current = 'home'

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal')  # Modifier l'orientation en horizontal
        self.btn_layout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=200)
        self.selected_contact = None
        self.value_labels = {}

        # Bouton pour configurer l'alarme
        btn_to_alarm = Button(text='Configurer Alarme')
        btn_to_alarm.bind(on_press=self.go_to_alarm_screen)
        self.btn_layout.add_widget(btn_to_alarm)

        # Bouton pour gérer les contacts
        btn_to_contact = Button(text='Gérer Contacts')
        btn_to_contact.bind(on_press=self.go_to_contact_screen)
        self.btn_layout.add_widget(btn_to_contact)

        # Bouton pour gérer les contacts
        btn_to_contact = Button(text='Voir Contacts')
        btn_to_contact.bind(on_press=self.go_to_contact_list_screen)
        self.btn_layout.add_widget(btn_to_contact)

        # Bouton pour envoyer le rapport
        btn_send_report = Button(text='Envoyer Rapport')
        btn_send_report.bind(on_press=self.send_report)
        self.btn_layout.add_widget(btn_send_report)

        self.layout.add_widget(self.btn_layout)

        # Section pour afficher les valeurs
        self.values_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.layout.add_widget(self.values_layout)

        self.add_widget(self.layout)

    def go_to_alarm_screen(self, instance):
        self.manager.current = 'alarm'

    def go_to_contact_screen(self, instance):
        self.manager.current = 'contact'

    def go_to_contact_list_screen(self, instance):
        print("Button pressed - Going to view contacts screen")
        contact_list_screen = self.manager.get_screen('contact_list')
        contact_list_screen.selected_contact = None  # Reset selected_contact when navigating to the contact list
        self.manager.current = 'contact_list'
        
    def update_value_labels(self, pin_number, value):
        # Vérifier si le label pour ce pin existe déjà
        if pin_number not in self.value_labels:
            # Créer un nouveau label et l'ajouter au dictionnaire
            label = Label(text=f'Pin {pin_number}: {value}')
            self.values_layout.add_widget(label)
            self.value_labels[pin_number] = label
        else:
            # Mettre à jour le label existant 
            self.value_labels[pin_number].text = f'Pin {pin_number}: {value}'

    def send_report(self, instance):
        to_address = ContactListScreen.selected_email
        subject = "Rapport d'alarme"
        body = "Veuillez trouver ci-joint le rapport des alarmes."
        attachment_path = 'rapport.csv'
        try:
            send_mail.send_mail(to_address, subject, body, attachment_path)
            print("Rapport envoyé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'envoi du rapport : {e}")

class AlarmScreen(Screen):
    def __init__(self, **kwargs):
        super(AlarmScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=10)  # Utilisez GridLayout avec une seule colonne

        # Assurez-vous que chaque widget prend une part égale de la hauteur disponible
        self.state_input = DebouncedTextInput(hint_text='État désiré (0 ou 1) pour signaux numériques', input_type='number', size_hint_y=None, height=100)
        self.min_value_input = DebouncedTextInput(hint_text='Valeur min pour signaux analogiques', input_type='number', size_hint_y=None, height=100)
        self.max_value_input = DebouncedTextInput(hint_text='Valeur max pour signaux analogiques', input_type='number', size_hint_y=None, height=100)
        self.pin_input = DebouncedTextInput(hint_text='Numéro du pin', input_type='number', size_hint_y=None, height=100)
        self.submit_button = Button(text='Configurer', size_hint_y=None, height=100)

        # Bouton de retour
        self.back_button = Button(text='Retour', size_hint_y=None, height=100)
        self.back_button.bind(on_press=self.go_back)

        # Ajout des éléments au GridLayout
        self.layout.add_widget(self.state_input)
        self.layout.add_widget(self.min_value_input)
        self.layout.add_widget(self.max_value_input)
        self.layout.add_widget(self.pin_input)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

        self.submit_button.bind(on_press=self.setup_alarm)

    def go_back(self, instance):
        self.manager.current = 'home'

    def check_alarm(self, pin_number, home_screen, min_value=None, max_value=None, desired_state=None):
        self.alarm_active = False
        self.last_sms_time = 0

        def update_ui(dt):
            gpio_value = lire_valeur.read_value(pin_number)  # Remplacer par votre fonction de lecture

            home_screen.update_value_labels(pin_number, gpio_value)

            # Vérifiez si l'alarme est active et si 4 minutes se sont écoulées depuis le dernier SMS
            current_time = time.time()
            if (current_time - self.last_sms_time) >= 240 or self.last_sms_time == 0:
                # Logique pour les signaux numériques
                if desired_state is not None and gpio_value == desired_state:
                    self.trigger_alarm(pin_number, gpio_value)
                # Logique pour les signaux analogiques
                elif min_value is not None and max_value is not None and (gpio_value < min_value or gpio_value > max_value):
                    self.trigger_alarm(pin_number, gpio_value)

        Clock.schedule_interval(update_ui, 1)

    def trigger_alarm(self, pin_number, gpio_value):
        if not self.alarm_active:
            # Logique pour envoyer un SMS
            send_sms.sendSms('+'+str(ContactListScreen.selected_phone_number))
            self.alarm_active = True
            self.last_sms_time = time.time()

            # Écrire dans le fichier CSV
            with open('rapport.csv', 'a', newline='') as csvfile:
                report_writer = csv.writer(csvfile, delimiter=',')
                report_writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), pin_number, gpio_value])
            
            # Afficher le bouton d'alarme
            self.show_alarm_button()
        else:
            current_time = time.time()
            if (current_time - self.last_sms_time) >= 240:
                send_sms.sendSms('+'+str(ContactListScreen.selected_phone_number))
                self.last_sms_time = current_time

    def show_alarm_button(self):
        alarm_button = Button(text='Alarme! Cliquez pour acquitter', size_hint=(1, None), height=50)
        alarm_button.bind(on_press=self.dismiss_alarm)

        # Ajouter le bouton d'alarme à l'écran actuel
        self.layout.add_widget(alarm_button)

    def dismiss_alarm(self, instance):
        self.alarm_active = False  # Acquitter l'alarme
        self.layout.remove_widget(instance)
        
    def setup_alarm(self, instance):
        pin_number = int(self.pin_input.text)
        home_screen = self.manager.get_screen('home')

        # Déterminer le mode sélectionné par l'utilisateur et passer les arguments appropriés
        if self.state_input.text:  # Mode numérique
            desired_state = int(self.state_input.text)
            alarm_thread = threading.Thread(target=self.check_alarm, args=(pin_number, home_screen), kwargs={'desired_state': desired_state})
        else:  # Mode analogique
            min_value = float(self.min_value_input.text)
            max_value = float(self.max_value_input.text)
            alarm_thread = threading.Thread(target=self.check_alarm, args=(pin_number, home_screen), kwargs={'min_value': min_value, 'max_value': max_value})

        alarm_thread.daemon = True
        alarm_thread.start()
        self.manager.current = 'home'


class AlarmApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AlarmScreen(name='alarm'))
        sm.add_widget(ContactScreen(name='contact'))
        sm.add_widget(ContactListScreen(name='contact_list'))  
        return sm

if __name__ == '__main__':
    AlarmApp().run()          
