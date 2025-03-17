from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import mysql.connector
from datetime import datetime
import csv

# Fonctions du backend
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Parfait1313",
        database="footlocker",
    )

def display_products(cursor):
    cursor.execute("SELECT * FROM product")
    return cursor.fetchall()

def add_product(cursor, db, name, description, price, quantity, category_name):
    cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
    category_id = cursor.fetchone()

    if category_id:
        category_id = category_id[0]
        cursor.execute(
            "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
            (name, description, price, quantity, category_id)
        )
        db.commit()
    else:
        raise ValueError(f"Category '{category_name}' not found in the database.")

def delete_product(cursor, db, product_id):
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    db.commit()

def modify_product(cursor, db, product_id, field, new_value):
    cursor.execute(f"UPDATE product SET {field} = %s WHERE id = %s", (new_value, product_id))
    db.commit()

def start_stock_management():
    window = tkinter.Tk()
    window.title("Stock Management System")
    window.geometry("720x640")
    my_tree = ttk.Treeview(window, show='headings', height=20)
    style = ttk.Style()

    placeholderArray = ['', '', '', '', '']

    for i in range(0, 5):
        placeholderArray[i] = tkinter.StringVar()

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)

        db = connect_to_db()
        cursor = db.cursor()
        products = display_products(cursor)
        cursor.close()
        db.close()

        for index, product in enumerate(products):
            my_tree.insert(parent='', index='end', iid=str(index), text="", values=product, tags="orow")

        my_tree.tag_configure('orow', background="#EEEEEE")
        my_tree.pack()

    def generate_id():
        new_id = random.randint(1000, 9999)
        placeholderArray[0].set(str(new_id))

    def save_data():
        item_id = placeholderArray[0].get()
        name = placeholderArray[1].get()
        price = placeholderArray[2].get()
        quantity = placeholderArray[3].get()
        category = placeholderArray[4].get()

        if item_id and name and price and quantity and category:
            db = connect_to_db()
            cursor = db.cursor()
            add_product(cursor, db, name, "", price, quantity, category)
            cursor.close()
            db.close()
            refreshTable()
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def update_data():
        selected_item = my_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a product to update!")
            return

        item_id = my_tree.item(selected_item)['values'][0]
        name = placeholderArray[1].get()
        price = placeholderArray[2].get()
        quantity = placeholderArray[3].get()
        category = placeholderArray[4].get()

        if name and price and quantity and category:
            db = connect_to_db()
            cursor = db.cursor()
            modify_product(cursor, db, item_id, 'name', name)
            modify_product(cursor, db, item_id, 'price', price)
            modify_product(cursor, db, item_id, 'quantity', quantity)

            cursor.execute("SELECT id FROM categories WHERE name = %s", (category,))
            category_id = cursor.fetchone()

            if category_id:
                category_id = category_id[0]
                modify_product(cursor, db, item_id, 'id_category', category_id)
            else:
                raise ValueError(f"Category '{category}' not found in the database.")

            cursor.close()
            db.close()
            refreshTable()
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def delete_data():
        selected_item = my_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a product to delete!")
            return

        item_id = my_tree.item(selected_item)['values'][0]
        db = connect_to_db()
        cursor = db.cursor()
        delete_product(cursor, db, item_id)
        cursor.close()
        db.close()
        refreshTable()

    def select_data():
        selected_item = my_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a product!")
            return

        values = my_tree.item(selected_item)['values']
        placeholderArray[0].set(values[0])
        placeholderArray[1].set(values[1])
        placeholderArray[2].set(values[2])
        placeholderArray[3].set(values[3])
        placeholderArray[4].set(values[4])

    def find_data():
        name = placeholderArray[1].get()
        if not name:
            messagebox.showerror("Error", "Enter a product name to find!")
            return

        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product WHERE name LIKE %s", ('%' + name + '%',))
        products = cursor.fetchall()
        cursor.close()
        db.close()

        for data in my_tree.get_children():
            my_tree.delete(data)

        for index, product in enumerate(products):
            my_tree.insert(parent='', index='end', iid=str(index), text="", values=product, tags="orow")

    def clear_data():
        itemIdEntry.delete(0, END)
        nameEntry.delete(0, END)
        priceEntry.delete(0, END)
        qntEntry.delete(0, END)
        categoryCombo.set('')

    def export_to_csv():
        db = connect_to_db()
        cursor = db.cursor()
        products = display_products(cursor)
        cursor.close()
        db.close()

        with open("products.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Item Id", "Name", "Description", "Category", "Price", "Date"])
            writer.writerows(products)

        messagebox.showinfo("Success", "Data exported to products.csv")

    frame = tkinter.Frame(window, bg='#02577A')
    frame.pack()

    btnColor = '#196E78'

    manageFrame = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
    manageFrame.grid(row=0, column=0, sticky="w", padx=[10, 200], pady=20, ipadx=[6])

    saveBtn = Button(manageFrame, text="SAVE", width=10, borderwidth=3, bg=btnColor, fg='white', command=save_data)
    updateBtn = Button(manageFrame, text="UPDATE", width=10, borderwidth=3, bg=btnColor, fg='white', command=update_data)
    deleteBtn = Button(manageFrame, text="DELETE", width=10, borderwidth=3, bg=btnColor, fg='white', command=delete_data)
    selectBtn = Button(manageFrame, text="SELECT", width=10, borderwidth=3, bg=btnColor, fg='white', command=select_data)
    findBtn = Button(manageFrame, text="FIND", width=10, borderwidth=3, bg=btnColor, fg='white', command=find_data)
    clearBtn = Button(manageFrame, text="CLEAR", width=10, borderwidth=3, bg=btnColor, fg='white', command=clear_data)
    exportBtn = Button(manageFrame, text="EXPORT EXCEL", width=10, borderwidth=3, bg=btnColor, fg='white', command=export_to_csv)

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
    my_tree['columns'] = ("Item Id", "Name", "Description", "Price", "Quantity", "Category", "Date")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Item Id", anchor=W, width=70)
    my_tree.column("Name", anchor=W, width=125)
    my_tree.column("Description", anchor=W, width=125)
    my_tree.column("Price", anchor=W, width=100)
    my_tree.column("Quantity", anchor=W, width=150)
    my_tree.column("Category", anchor=W, width=150)
    my_tree.column("Date", anchor=W, width=150)
    my_tree.heading("Item Id", text="Item Id", anchor=W)
    my_tree.heading("Name", text="Name", anchor=W)
    my_tree.heading("Description", text="Description", anchor=W)
    my_tree.heading("Price", text="Price", anchor=W)
    my_tree.heading("Quantity", text="Quantity", anchor=W)
    my_tree.heading("Category", text="Category", anchor=W)
    my_tree.heading("Date", text="Date", anchor=W)
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.pack()

    for entry in [itemIdEntry, nameEntry, priceEntry, qntEntry]:
        entry.bind("<FocusIn>", lambda event: event.widget.selection_range(0, END))

    refreshTable()

    window.resizable(False, False)
    window.mainloop()

# Appeler la fonction pour démarrer l'application
start_stock_management()
