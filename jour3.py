import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Parfait1313",  # Remplace par ton mot de passe si nécessaire
        database="footlocker",   # Nom de ta base de données "footlocker"
    )

# l'utilisateur peut afficher tous les produits
def display_products(cursor):
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    print("Liste des produits :")
    for product in products:
        print(f"ID: {product[0]}, Nom: {product[1]}, Description: {product[2]}, Prix: {product[3]}, Quantité: {product[4]}, ID Catégorie: {product[5]}")

# l'utilisateur peut ajouter un produit
def add_product(cursor, db):
    name = input("Entrez le nom du produit : ")
    description = input("Entrez la description du produit : ")
    price = float(input("Entrez le prix du produit : "))
    quantity = int(input("Entrez la quantité en stock : "))
    id_category = int(input("Entrez l'ID de catégorie (1: Femmes, 2: Hommes, 3: Enfants, 4: Nouveautés, 5: Marques, 6: Best sellers, 7: Sport, 8: Promotions accessoires) : "))

    cursor.execute(
        "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
        (name, description, price, quantity, id_category)
    )
    db.commit()
    print(f"Produit '{name}' ajouté avec succès !")

# l'utilisateur peut supprimer un produit
def delete_product(cursor, db):
    product_id = int(input("Entrez l'ID du produit à supprimer : "))
    
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    db.commit()
    print(f"Produit avec ID {product_id} supprimé avec succès !")

# l'utilisateur peut modifier un produit
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
        new_name = input("Entrez le nouveau nom du produit : ")
        cursor.execute("UPDATE product SET name = %s WHERE id = %s", (new_name, product_id))
    elif choice == 2:
        new_description = input("Entrez la nouvelle description du produit : ")
        cursor.execute("UPDATE product SET description = %s WHERE id = %s", (new_description, product_id))
    elif choice == 3:
        new_price = float(input("Entrez le nouveau prix du produit : "))
        cursor.execute("UPDATE product SET price = %s WHERE id = %s", (new_price, product_id))
    elif choice == 4:
        new_quantity = int(input("Entrez la nouvelle quantité en stock : "))
        cursor.execute("UPDATE product SET quantity = %s WHERE id = %s", (new_quantity, product_id))
    elif choice == 5:
        new_category = int(input("Entrez le nouvel ID de catégorie : "))
        cursor.execute("UPDATE product SET id_category = %s WHERE id = %s", (new_category, product_id))

    db.commit()
    print(f"Produit avec ID {product_id} modifié avec succès !")


def menu():
    db = connect_to_db()
    cursor = db.cursor()

    while True:
        print("\n----- Menu -----")
        print("1. Afficher les produits")
        print("2. Ajouter un produit")
        print("3. Supprimer un produit")
        print("4. Modifier un produit")
        print("5. Quitter")
        
        choice = input("Choisissez une option (1-5) : ")

        if choice == "1":
            display_products(cursor)
        elif choice == "2":
            add_product(cursor, db)
        elif choice == "3":
            delete_product(cursor, db)
        elif choice == "4":
            modify_product(cursor, db)
        elif choice == "5":
            print("Au revoir !")
            break
        else:
            print("Option invalide, essayez encore.")

    cursor.close()
    db.close()

if __name__ == "__main__":
    menu()
