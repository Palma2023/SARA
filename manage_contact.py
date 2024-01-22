# manage_contact.py

import csv

class Contact:
    def __init__(self, nom, email, telephone):
        self.nom = nom
        self.email = email
        self.telephone = telephone

    def set_nom(self, nom):
        self.nom = nom

    def get_nom(self):
        return self.nom

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_telephone(self, telephone):
        self.telephone = telephone

    def get_telephone(self):
        return self.telephone

    def __str__(self):
        return f"Contact: {self.nom}, E-mail: {self.email}, Téléphone: {self.telephone}"

def ajouter_contact(contact, fichier='contacts.csv'):
    with open(fichier, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([contact.nom, contact.email, contact.telephone])

def lire_contacts(fichier='contacts.csv'):
    contacts = []
    try:
        with open(fichier, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                contacts.append(Contact(*row))
    except FileNotFoundError:
        print("Le fichier n'existe pas encore.")
    return contacts
    
