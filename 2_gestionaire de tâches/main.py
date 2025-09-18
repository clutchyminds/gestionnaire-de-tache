import json
import tkinter as tk
from tkinter import messagebox
import os
import threading

if os.path.exists("donnees.json"):
    with open("donnees.json", "r") as f:
        try:
            taches = json.load(f)
        except json.JSONDecodeError:
            taches = []
else:
    taches = []

def demarrer_timer_visuel(titre, minutes):
    window_timer = tk.Toplevel(root)
    window_timer.title(f"Timer - {titre}")
    window_timer.geometry("300x150")

    label_temps = tk.Label(window_timer, font=("Arial", 20))
    label_temps.pack(pady=20)

    def update_timer(remaining):
        if remaining > 0:
            mins, secs = divmod(remaining, 60)
            label_temps.config(text=f"{mins:02d}:{secs:02d}")
            window_timer.after(1000, update_timer, remaining - 1)
        else:
            label_temps.config(text="Temps écoulé !", fg="red")
            messagebox.showwarning("⏰ Temps écoulé", f"La tâche '{titre}' a dépassé la limite !")

    update_timer(minutes * 60)

def aj_tâche():
    def update_and_save():
        titre = entry_titre.get()
        try:
            limite = int(entry_temps.get())
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide. Entrez un nombre entier.")
            return

        if titre.strip() != "":
            nouvelle_tache = {"titre": titre, "durée": limite}
            taches.append(nouvelle_tache)
            with open('donnees.json', 'w') as f:
                json.dump(taches, f, indent=4)
            entry_titre.delete(0, tk.END)
            entry_temps.delete(0, tk.END)
            update_label()
            demarrer_timer_visuel(titre, limite)

    def update_label():
        affichage.config(text="\n".join([f"{t['titre']} - {t['durée']} min" for t in taches]))

    window_add = tk.Toplevel(root)
    window_add.title("Ajouter une tâche")
    window_add.geometry("400x250")

    tk.Label(window_add, text="Nom de la tâche :").pack()
    entry_titre = tk.Entry(window_add, width=30)
    entry_titre.pack(pady=5)

    tk.Label(window_add, text="Durée (en minutes) :").pack()
    entry_temps = tk.Entry(window_add, width=10)
    entry_temps.pack(pady=5)

    button = tk.Button(window_add, text="Ajouter et démarrer", command=update_and_save)
    button.pack(pady=10)

    affichage = tk.Label(window_add, text="", justify="left")
    affichage.pack(pady=10)

def tâches():
    window_display = tk.Toplevel(root)
    window_display.title("Tâches enregistrées")
    window_display.geometry("400x300")

    affichage = "\n".join([f"{t['titre']} - {t['durée']} min" for t in taches])
    label = tk.Label(window_display, text=affichage, justify="left")
    label.pack(pady=10)

def modifier_tache():
    window_edit = tk.Toplevel(root)
    window_edit.title("Modifier une tâche")
    window_edit.geometry("400x300")

    listbox = tk.Listbox(window_edit, width=40)
    listbox.pack(pady=10)
    for t in taches:
        listbox.insert(tk.END, f"{t['titre']} - {t['durée']} min")

    entry_modif = tk.Entry(window_edit, width=30)
    entry_modif.pack(pady=5)

    entry_temps_modif = tk.Entry(window_edit, width=10)
    entry_temps_modif.pack(pady=5)

    def valider_modif():
        index = listbox.curselection()
        if index:
            nouveau_titre = entry_modif.get()
            try:
                nouvelle_duree = int(entry_temps_modif.get())
            except ValueError:
                messagebox.showerror("Erreur", "Durée invalide.")
                return
            taches[index[0]] = {"titre": nouveau_titre, "durée": nouvelle_duree}
            with open('donnees.json', 'w') as f:
                json.dump(taches, f, indent=4)
            window_edit.destroy()

    button_valider = tk.Button(window_edit, text="Valider la modification", command=valider_modif)
    button_valider.pack(pady=10)

def supprimer_tache():
    window_del = tk.Toplevel(root)
    window_del.title("Supprimer une tâche")
    window_del.geometry("400x300")

    listbox = tk.Listbox(window_del, width=40)
    listbox.pack(pady=10)
    for t in taches:
        listbox.insert(tk.END, f"{t['titre']} - {t['durée']} min")

    def valider_suppression():
        index = listbox.curselection()
        if index:
            taches.pop(index[0])
            with open('donnees.json', 'w') as f:
                json.dump(taches, f, indent=4)
            window_del.destroy()

    button_supprimer = tk.Button(window_del, text="Supprimer", command=valider_suppression)
    button_supprimer.pack(pady=10)

def sauvegarder_quitter():
    with open('donnees.json', 'w') as f:
        json.dump(taches, f, indent=4)
    root.quit()

root = tk.Tk()
root.title("🗂️ Gestionnaire de tâches")
root.geometry("400x350")

tk.Button(root, text="Ajouter une tâche", command=aj_tâche).pack(pady=5)
tk.Button(root, text="Afficher les tâches", command=tâches).pack(pady=5)
tk.Button(root, text="Modifier une tâche", command=modifier_tache).pack(pady=5)
tk.Button(root, text="Supprimer une tâche", command=supprimer_tache).pack(pady=5)
tk.Button(root, text="Sauvegarder et quitter", command=sauvegarder_quitter).pack(pady=5)

root.mainloop()
