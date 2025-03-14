from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import pymysql
import csv
from datetime import datetime
import numpy as np

window = tkinter.Tk()
window.title("Stock Management System")
window.geometry("720x640")
my_tree = ttk.Treeview(window, show='headings', height=20)
style = ttk.Style()

placeholderArray = ['', '', '', '', '']

# fonction de connexion à la base de données (si nécessaire)
# def connection():
#     conn = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='Parfait1313',
#         db='footlocker'
#     )
#     return conn
# conn = connection()
# cursor = conn.cursor()

for i in range(0, 5):
    placeholderArray[i] = tkinter.StringVar()

dummydata = [
    [''],
]

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    
    for index, array in enumerate(dummydata):
        my_tree.insert(parent='', index='end', iid=str(index), text="", values=array, tags="orow")

    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.pack()

def generate_id():
    """Fonction pour générer un identifiant unique et remplir le champ Item ID."""
    new_id = random.randint(1000, 9999)  # Générer un ID aléatoire entre 1000 et 9999
    placeholderArray[0].set(str(new_id))  # Placer cet ID dans le champ 'Item ID'

def save_data():
    """Fonction pour sauvegarder les données dans le tableau."""
    item_id = placeholderArray[0].get()
    name = placeholderArray[1].get()
    price = placeholderArray[2].get()
    quantity = placeholderArray[3].get()
    category = placeholderArray[4].get()

    # Validation des champs (par exemple, vérifier si tous les champs sont remplis)
    if item_id and name and price and quantity and category:
        # Ajouter les nouvelles données dans le tableau
        new_row = [item_id, name, price, quantity, category, str(datetime.now())]
        dummydata.append(new_row)
        refreshTable()  # Rafraîchir la table pour afficher les nouvelles données
    else:
        messagebox.showerror("Error", "All fields must be filled!")

frame = tkinter.Frame(window, bg='#02577A')
frame.pack()

btnColor = '#196E78'

manageFrame = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
manageFrame.grid(row=0, column=0, sticky="w", padx=[10, 200], pady=20, ipadx=[6])

saveBtn = Button(manageFrame, text="SAVE", width=10, borderwidth=3, bg=btnColor, fg='white', command=save_data)
updateBtn = Button(manageFrame, text="UPDATE", width=10, borderwidth=3, bg=btnColor, fg='white')
deleteBtn = Button(manageFrame, text="DELETE", width=10, borderwidth=3, bg=btnColor, fg='white')
selectBtn = Button(manageFrame, text="SELECT", width=10, borderwidth=3, bg=btnColor, fg='white')
findBtn = Button(manageFrame, text="FIND", width=10, borderwidth=3, bg=btnColor, fg='white')
clearBtn = Button(manageFrame, text="CLEAR", width=10, borderwidth=3, bg=btnColor, fg='white')
exportBtn = Button(manageFrame, text="EXPORT EXCEL", width=10, borderwidth=3, bg=btnColor, fg='white')

saveBtn.grid(row=0, column=0, padx=5, pady=5)
updateBtn.grid(row=0, column=1, padx=5, pady=5)
deleteBtn.grid(row=0, column=2, padx=5, pady=5)
selectBtn.grid(row=0, column=3, padx=5, pady=5)
findBtn.grid(row=0, column=4, padx=5, pady=5)
clearBtn.grid(row=0, column=5, padx=5, pady=5)
exportBtn.grid(row=0, column=6, padx=5, pady=5)

entriesFrame = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
entriesFrame.grid(row=1, column=0, sticky="w", padx=[10, 200], pady=[0, 20], ipadx=[6])

itemIdLabel = Label(entriesFrame, text="ITEM ID", anchor="e", width=10)
nameLabel = Label(entriesFrame, text="NAME", anchor="e", width=10)
priceLabel = Label(entriesFrame, text="PRICE", anchor="e", width=10)
qntLabel = Label(entriesFrame, text="QNT", anchor="e", width=10)
categoryLabel = Label(entriesFrame, text="CATEGORY", anchor="e", width=10)

itemIdLabel.grid(row=0, column=0, padx=10)
nameLabel.grid(row=1, column=0, padx=10)
priceLabel.grid(row=2, column=0, padx=10)
qntLabel.grid(row=3, column=0, padx=10)
categoryLabel.grid(row=4, column=0, padx=10)

categoryArray = ['Women', 'Men', 'Children', 'News', 'Best Seller', 'Promotion', 'Accessories', 'Brands']

itemIdEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[0])
nameEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[1])
priceEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[2])
qntEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[3])
categoryCombo = ttk.Combobox(entriesFrame, width=47, textvariable=placeholderArray[4], values=categoryArray)

itemIdEntry.grid(row=0, column=2, padx=5, pady=5)
nameEntry.grid(row=1, column=2, padx=5, pady=5)
priceEntry.grid(row=2, column=2, padx=5, pady=5)
qntEntry.grid(row=3, column=2, padx=5, pady=5)
categoryCombo.grid(row=4, column=2, padx=5, pady=5)

generateIdBtn = Button(entriesFrame, text="GENERATE ID", borderwidth=3, bg=btnColor, fg='white', command=generate_id)
generateIdBtn.grid(row=0, column=3, padx=5, pady=5)

style.configure(window)
my_tree['columns'] = ("Item Id", "Name", "Price", "Quantity", "Category", "Date")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Item Id", anchor=W, width=70)
my_tree.column("Name", anchor=W, width=125)
my_tree.column("Price", anchor=W, width=125)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Category", anchor=W, width=150)
my_tree.column("Date", anchor=W, width=150)
my_tree.heading("Item Id", text="Item Id", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Category", text="Category", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)
my_tree.tag_configure('orow', background="#EEEEEE")
my_tree.pack()

# Cette partie garantit que les champs sont bien sélectionnés au focus
for entry in [itemIdEntry, nameEntry, priceEntry, qntEntry, categoryCombo]:
    entry.bind("<FocusIn>", lambda event: event.widget.select())

refreshTable()

window.resizable(False, False)
window.mainloop()
