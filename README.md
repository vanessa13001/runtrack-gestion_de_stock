# runtrack-gestion_de_stock

# Stock Management System

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/stock-management-system.git
   ```
2. Install the required dependencies:
   - Python 3.x
   - `tkinter`
   - `mysql.connector`
   - `bcrypt`
   - `customtkinter` (for the login interface)

## Usage

1. Start the application by running the `backend.py` file:
   ```
   python backend.py
   ```
2. The Stock Management System window will appear, allowing you to manage your product inventory.

## API

The `backend.py` file provides the following functions:

- `connect_to_db()`: Connects to the MySQL database.
- `display_products(cursor)`: Retrieves all products from the database.
- `add_product(cursor, db, name, description, price, quantity, category_name)`: Adds a new product to the database.
- `delete_product(cursor, db, product_id)`: Deletes a product from the database.
- `modify_product(cursor, db, product_id, field, new_value)`: Updates a specific field of a product in the database.

The `login.py` file provides the following function:

- `verify_login(user_id, password)`: Verifies the user's login credentials against the database.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Test your changes.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To test the application, you can run the `backend.py` and `login.py` files and interact with the user interface.
