import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Parfait1313",  # Remplace par ton mot de passe si nécessaire
        database="footlocker",   # Nom de ta base de données "footlocker"
    )

# Afficher les produits
def display_products(cursor):
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    print("Liste des produits :")
    for product in products:
        print(f"ID: {product[0]}, Nom: {product[1]}, Description: {product[2]}, Prix: {product[3]}, Quantité: {product[4]}, ID Catégorie: {product[5]}")

# Ajouter un produit
def add_product(cursor, db):
    name = input("Entrez le nom du produit : ")
    description = input("Entrez la description du produit : ")
    price = float(input("Entrez le prix du produit : "))
    quantity = int(input("Entrez la quantité en stock : "))
    id_category = int(input("Entrez l'ID de catégorie : "))

    cursor.execute(
        "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
        (name, description, price, quantity, id_category)
    )
    db.commit()
    print(f"Produit '{name}' ajouté avec succès !")

# Supprimer un produit
def delete_product(cursor, db):
    product_id = int(input("Entrez l'ID du produit à supprimer : "))
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    db.commit()
    print(f"Produit avec ID {product_id} supprimé avec succès !")

# Modifier un produit
def modify_product(cursor, db):
    product_id = int(input("Entrez l'ID du produit à modifier : "))
    print("Que voulez-vous modifier ?")
    print("1. Nom")
    print("2. Description")
    print("3. Prix")
    print("4. Quantité")
    print("5. Catégorie")
    choice = int(input("Choisissez une option (1-5) : "))

    if choice == 1:
        new_value = input("Entrez le nouveau nom : ")
        cursor.execute("UPDATE product SET name = %s WHERE id = %s", (new_value, product_id))
    elif choice == 2:
        new_value = input("Entrez la nouvelle description : ")
        cursor.execute("UPDATE product SET description = %s WHERE id = %s", (new_value, product_id))
    elif choice == 3:
        new_value = float(input("Entrez le nouveau prix : "))
        cursor.execute("UPDATE product SET price = %s WHERE id = %s", (new_value, product_id))
    elif choice == 4:
        new_value = int(input("Entrez la nouvelle quantité : "))
        cursor.execute("UPDATE product SET quantity = %s WHERE id = %s", (new_value, product_id))
    elif choice == 5:
        new_value = int(input("Entrez le nouvel ID de catégorie : "))
        cursor.execute("UPDATE product SET id_category = %s WHERE id = %s", (new_value, product_id))

    db.commit()
    print(f"Produit avec ID {product_id} modifié avec succès !")

# Afficher les marques
def display_brands(cursor):
    cursor.execute("SELECT * FROM marques")
    brands = cursor.fetchall()
    print("Liste des marques :")
    for brand in brands:
        print(f"ID: {brand[0]}, Nom: {brand[1]}")

# Ajouter une marque
def add_brand(cursor, db):
    name = input("Entrez le nom de la marque : ")
    cursor.execute("INSERT INTO marques (nom) VALUES (%s)", (name,))
    db.commit()
    print(f"Marque '{name}' ajoutée avec succès !")

# Afficher les tailles
def display_sizes(cursor):
    cursor.execute("SELECT * FROM tailles")
    sizes = cursor.fetchall()
    print("Liste des tailles :")
    for size in sizes:
        print(f"ID: {size[0]}, Taille: {size[1]}")

# Ajouter une taille
def add_size(cursor, db):
    size = input("Entrez la taille (XS, S, M, L, XL, XXL) : ")
    cursor.execute("INSERT INTO tailles (taille) VALUES (%s)", (size,))
    db.commit()
    print(f"Taille '{size}' ajoutée avec succès !")

# Menu principal
def menu():
    db = connect_to_db()
    cursor = db.cursor()

    while True:
        print("\n----- Menu -----")
        print("1. Afficher les produits")
        print("2. Ajouter un produit")
        print("3. Supprimer un produit")
        print("4. Modifier un produit")
        print("5. Afficher les marques")
        print("6. Ajouter une marque")
        print("7. Afficher les tailles")
        print("8. Ajouter une taille")
        print("9. Quitter")
        
        choice = input("Choisissez une option (1-9) : ")

        if choice == "1":
            display_products(cursor)
        elif choice == "2":
            add_product(cursor, db)
        elif choice == "3":
            delete_product(cursor, db)
        elif choice == "4":
            modify_product(cursor, db)
        elif choice == "5":
            display_brands(cursor)
        elif choice == "6":
            add_brand(cursor, db)
        elif choice == "7":
            display_sizes(cursor)
        elif choice == "8":
            add_size(cursor, db)
        elif choice == "9":
            print("Au revoir !")
            break
        else:
            print("Option invalide, essayez encore.")

    cursor.close()
    db.close()

if __name__ == "__main__":
    menu()
