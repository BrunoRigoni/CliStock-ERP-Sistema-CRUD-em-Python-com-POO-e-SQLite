from models.users import User, UserDAO
from utils.utils import clear, pause
import os
import sqlite3


class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price


class storageDAO:
    def __init__(self, db_path=None):
        if not db_path:
            db_path = os.path.join(os.path.dirname(
                __file__), "..", 'database', 'system.db')
            db_path = os.path.abspath(db_path)

        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()
        self.create_product_table()

    def create_product_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)

                )
        """)
        self.connect.commit()

    def add_product(self, product, user_id):
        self.cursor.execute("INSERT INTO products (name, quantity, price, user_id) VALUES (?, ? , ?, ?)",
                            (product.name, product.quantity, product.price, user_id)
                            )
        self.connect.commit()

    def show_products(self, user_id):
        self.cursor.execute(
            "SELECT id, name, quantity, price FROM products WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def update_product_name(self, id, product):
        self.cursor.execute(
            "UPDATE products SET name = ? WHERE id = ?", (product.name, id))
        self.connect.commit()

    def update_product_quantity(self, id, product):
        self.cursor.execute(
            "UPDATE products SET quantity = ? WHERE id = ?", (product.quantity, id))
        self.connect.commit()

    def update_product_price(self, id, product):
        self.cursor.execute(
            "UPDATE products SET price = ? WHERE id = ?", (product.price, id))
        self.connect.commit()

    def remove(self, id):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (id,))
        self.connect.commit()


def admin_menu(user_id):
    storage_DAO = storageDAO()
    while True:
        print("""
        [1] ADICIONAR PRODUTO
        [2] LISTAR
        [3] ATUALIZAR PRODUTO
        [4] REMOVER PRODUTO
        [5] VOLTAR
 """)
        try:
            sub_option = int(input("\nDIGITE A OPÇÃO: "))
        except ValueError:
            print("OPÇÃO INVÁLIDA.")
            continue

        if sub_option == 1:
            clear()
            print("- PARA ADICIONAR PRODUTO, DIGITE AS INFORMAÇÕES A SEGUIR -")
            product_name = input("NOME DO PRODUTO: ")
            product_quantity = int(input("QUANTIDADE: UN"))
            product_price = float(input("PREÇO: R$").replace(',', '.'))
            new_product = Product(
                product_name, product_quantity, product_price)
            storage_DAO.add_product(new_product, user_id)
            clear()
            print(
                f"{product_name}, {product_quantity}, R$ {product_price:.2f} foi adicionado com sucesso.")
            pause()

        elif sub_option == 5:
            print("SAINDO")
            quit()

        else:
            print("DIGITE UMA OPÇÃO VÁLIDA!")
