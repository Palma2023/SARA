from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import csv

class CSVDisplayApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')    
        # Lire les données du fichier CSV et les ajouter à la mise en page
        with open('contacts.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                text = ', '.join(row)
                label = Label(text=text, color=(1, 1, 1, 1))  # Texte en blanc
                layout.add_widget(label)
        return layout
    
if __name__ == '__main__':
    CSVDisplayApp().run()

