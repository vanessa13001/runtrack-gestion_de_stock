import customtkinter as ctk
import subprocess
import mysql.connector
from tkinter import messagebox
import bcrypt
import os

print("Répertoire de travail actuel :", os.getcwd())

def verify_login(user_id, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="footlocker",
        )
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def on_login():
    user_id = entry1.get()
    password = entry2.get()
    if verify_login(user_id, password):
        # Annuler tous les appels `after` avant de détruire la fenêtre
        app.after_cancel(update_id)
        app.after_cancel(check_dpi_scaling_id)
        app.after_cancel(click_animation_id)

        app.destroy()
        # Utiliser le chemin relatif pour exécuter backend.py
        backend_path = "interface\\backend.py"

        # Vérifier si le fichier existe avant d'essayer de l'exécuter
        try:
            subprocess.run(["python", backend_path])
        except Exception:
            messagebox.showerror("Erreur", f"Fichier introuvable : {backend_path}")
        # if os.path.exists(backend_path):
        #     subprocess.run(["python", backend_path])
        # else:
        #     messagebox.showerror("Erreur", f"Fichier introuvable : {backend_path}")
    else:
        messagebox.showerror("Erreur", "ID ou mot de passe incorrect")

# Initialiser l'application
app = ctk.CTk()
app.geometry("400x300")
app.title("Fenêtre de Connexion")

# Configurer l'apparence et le thème de couleur
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Créer les widgets
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="LOGIN", font=("Helvetica", 24))
label.pack(pady=12, padx=10)

entry1 = ctk.CTkEntry(master=frame, placeholder_text="ID")
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Se connecter", command=on_login)
button.pack(pady=12, padx=10)

# Exemple d'appels `after`
update_id = app.after(1000, lambda: print("Update function"))
check_dpi_scaling_id = app.after(2000, lambda: print("Check DPI scaling"))
click_animation_id = app.after(3000, lambda: print("Click animation"))

# Lancer l'application
app.mainloop()
