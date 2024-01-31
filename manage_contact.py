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
        writer.writerow([contact[0], contact[1], contact[2]])


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

def supprimer_contact(contact_to_delete, fichier='contacts.csv'):
    if contact_to_delete is None:
        return

    # Read existing contacts
    contacts = lire_contacts(fichier)

    # Identify the index or identifier of the contact to delete
    index_to_delete = -1
    for index, contact in enumerate(contacts):
        if contact.get_nom() == contact_to_delete.get_nom() and contact.get_telephone() == contact_to_delete.get_telephone():
            index_to_delete = index
            break

    # Remove the contact if found
    if index_to_delete != -1:
        del contacts[index_to_delete]

        # Write back the updated contacts to the CSV file
        with open(fichier, 'w', newline='') as file:
            writer = csv.writer(file)
            for contact in contacts:
                writer.writerow([contact.nom, contact.email, contact.telephone])
    
