import requests
import tkinter as tk

url = "http://127.0.0.1:8000/reception_demande/"

def recup_info():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    ville = entry_ville.get()
    email = entry_email.get()
    type_immobilier = entry_type.get()
    nombre_piece = entry_piece.get()
    montant = entry_montant.get()
    revenu = entry_revenu.get()
    depenses = entry_depenses.get()

    data = {
    "nom": nom,
    "prenom": prenom,
    "ville": ville,
    "email": email,
    "type_immobilier": type_immobilier,
    "montant": montant,
    "nombre_piece": nombre_piece,
    "revenu": revenu,
    "depenses": depenses
    }

    response = requests.post(url, json=data)

    
    try:
        if response.text:
            print(response.json())
        else:
            print("La réponse est vide.")
    except requests.exceptions.JSONDecodeError:
        print("La réponse n'est pas au format JSON.")
        print("Contenu brut de la réponse:", response.text)

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Formulaire de demande de prêt")

label_nom = tk.Label(root, text="Nom : ")
label_nom.grid(row=0, column=0)
entry_nom = tk.Entry(root)
entry_nom.grid(row=0, column=1)

label_prenom = tk.Label(root, text="Prénom : ")
label_prenom.grid(row=1, column=0)
entry_prenom = tk.Entry(root)
entry_prenom.grid(row=1, column=1)

label_ville = tk.Label(root, text="Ville : ")
label_ville.grid(row=2, column=0)
entry_ville = tk.Entry(root)
entry_ville.grid(row=2, column=1)

label_email = tk.Label(root, text="Email : ")
label_email.grid(row=3, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1)

label_type = tk.Label(root, text="Type d'immobilier : ")
label_type.grid(row=4, column=0)
entry_type = tk.Entry(root)
entry_type.grid(row=4, column=1)

label_piece = tk.Label(root, text="Nombre de pièces : ")
label_piece.grid(row=5, column=0)
entry_piece = tk.Entry(root)
entry_piece.grid(row=5, column=1)

label_montant = tk.Label(root, text="Montant : ")
label_montant.grid(row=6, column=0)
entry_montant = tk.Entry(root)
entry_montant.grid(row=6, column=1)

label_revenu = tk.Label(root, text="Revenu : ")
label_revenu.grid(row=7, column=0)
entry_revenu = tk.Entry(root)
entry_revenu.grid(row=7, column=1)

label_depenses = tk.Label(root, text="Dépenses : ")
label_depenses.grid(row=8, column=0)
entry_depenses = tk.Entry(root)
entry_depenses.grid(row=8, column=1)

submit_button = tk.Button(root, text="Soumettre", command=recup_info)
submit_button.grid(row=9, column=1)

root.mainloop()
