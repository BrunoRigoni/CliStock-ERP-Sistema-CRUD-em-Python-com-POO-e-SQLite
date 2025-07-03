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
        self.create_order()

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

    def update_product_name(self, id, new_name):
        self.cursor.execute(
            "UPDATE products SET name = ? WHERE id = ?", (new_name, id))
        self.connect.commit()

    def update_product_quantity(self, id, new_quantity):
        self.cursor.execute(
            "UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, id))
        self.connect.commit()

    def update_product_price(self, id, new_price):
        self.cursor.execute(
            "UPDATE products SET price = ? WHERE id = ?", (new_price, id))
        self.connect.commit()

    def remove(self, id):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (id,))
        self.connect.commit()

    def get_produtcs_client(self):
        self.cursor.execute("SELECT id, name, quantity, price FROM products")
        return self.cursor.fetchall()

    def create_order(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS new_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
                            )
""")
        self.connect.commit()

    def create_new_order(self, user_id, product_id, quantity):
        # Verificar se o produto existe e tem estoque suficiente
        self.cursor.execute("""
        SELECT quantity FROM products WHERE id = ?
""", (product_id,))

        result = self.cursor.fetchone()

        if not result:
            return "Produto não encontrado."

        current_storage = result[0]

        if current_storage < quantity:
            return "Estoque insuficiente"
        # Registrar o pedido
        self.cursor.execute("""
        INSERT INTO new_order (user_id, product_id, quantity) VALUES (?, ?, ?)
""", (user_id, product_id, quantity)
        )

        # Atualizar estoque
        new_storage = current_storage - quantity
        self.cursor.execute("""
        UPDATE products SET quantity = ? WHERE id = ?
                            """, (new_storage, product_id))

        self.connect.commit()
        return "Pedido realizado com sucesso!"

    def get_client_orders(self, user_id,):
        self.cursor.execute("""
        SELECT o.id, p.name, o.quantity, p.price, o.data
        FROM new_order o
        JOIN products p ON o.product_id = p.id
        WHERE o.user_id = ?
        ORDER BY o.data DESC
 """, (user_id,))
        return self.cursor.fetchall()

    def get_all_orders(self):
        self.cursor.execute("""
        SELECT o.id, u.name AS client, p.name AS products, o.quantity, p.price, o.data
        FROM new_order o
        JOIN users u ON o.user_id = u.id
        JOIN products p ON o.product_id = p.id
        ORDER BY o.data DESC
 """)
        return self.cursor.fetchall()


def detailed_products(user_id, products):
    total_price = 0
    print("\nID | NOME | QUANTIDADE | PREÇO")
    for p in products:
        subtotal = p[2] * p[3]
        total_price += subtotal
        print(
            f"{p[0]} | {p[1]} | {p[2]} UN | R$ {p[3]:.2f} | R$ {str(f'{subtotal:.2f}').replace('.', ',')}")
    print("-" * 50)
    print(
        f"TOTAL GERAL DO ESTOQUE DO ADM ({user_id}): R$ {str(f'{total_price:.2f}').replace('.', ',')}")


def simple_products(products):
    print("\nID | NOME | QUANTIDADE | PREÇO")
    for p in products:
        print(
            f"{p[0]} | {p[1]} | {p[2]} UN | R$ {str(f'{p[3]:.2f}').replace('.', ',')}")


def admin_menu(user_id, name):
    storage_DAO = storageDAO()
    while True:
        print(f"Seja bem vindo {name}!")
        print("""
        [1] ADICIONAR PRODUTO
        [2] LISTAR
        [3] ATUALIZAR PRODUTO
        [4] REMOVER PRODUTO
        [5] VER TODOS OS PEDIDOS
        [6] VOLTAR
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
        elif sub_option == 2:
            clear()
            products = storage_DAO.show_products(user_id)
            if not products:
                print("Nenhum produto cadastrado!")
            else:
                detailed_products(user_id, products)
                pause()
                clear()
        elif sub_option == 3:
            clear()
            while True:
                print("""
[1]ATUALIZAR NOME
[2]ATUALIZAR ESTOQUE
[3]ATUALIZAR PREÇO
[4] SAIR
                      """)
                products = storage_DAO.show_products(user_id)
                try:
                    update_options = int(input("DIGITE A OPÇÃO: "))
                except ValueError:
                    print("Digite uma opção válida.")

                if update_options == 1:
                    clear()

                    if not products:
                        print("Nenhum produto cadastrado!")
                    else:
                        simple_products(user_id, products)

                        try:
                            id_update = int(
                                input("ID do produto que deseja alterar o nome: "))
                        except ValueError:
                            print("Digite um ID válido.")
                            continue
                        name_update = input("NOVO NOME: ")
                        storage_DAO.update_product_name(id_update, name_update)
                        print(
                            f"O nome do produto ID {id_update} foi alterado para -> {name_update}")
                        pause()
                elif update_options == 2:
                    clear()
                    if not products:
                        print("Nenhum produto cadastrado!")
                    else:
                        simple_products(user_id, products)
                        try:
                            id_update = int(
                                input("ID do produto que deseja alterar o estoque: "))
                        except ValueError:
                            print("Digite um ID válido.")
                            continue
                        storage_update = int(
                            input("NOVA QUANTIDADE EM ESTOQUE: "))
                        storage_DAO.update_product_quantity(
                            id_update, storage_update, )
                        print(
                            f"O estoque do produto ID {id_update} foi alterado para -> {storage_update}un")
                        pause()

                elif update_options == 3:
                    clear()
                    if not products:
                        print("Nenhum produto cadastrado!")
                    else:
                        simple_products(user_id, products)
                        try:
                            id_update = int(
                                input("ID do produto que deseja alterar o estoque: "))
                        except ValueError:
                            print("Digite um ID válido.")
                            continue
                        price_update = float(
                            input("NOVO VALOR: ").replace(",", "."))
                        storage_DAO.update_product_price(
                            id_update, price_update, )
                        print(
                            f"O preço do produto -> ID {id_update} foi alterado para -> {price_update:.2f} R$")
                        pause()

                elif update_options == 4:
                    print("Voltando...")
                    pause()
                    break

                else:
                    print("Digite uma opção válida.")
                    pause()
        elif sub_option == 4:
            clear()
            products = storage_DAO.show_products(user_id)

            if not products:
                print("Nenhum produto cadastrado!")
            else:
                simple_products(user_id, products)
                try:
                    id_delete = int(
                        input("ID do produto que deseja deletar: "))
                except ValueError:
                    print("Digite um ID válido.")
                else:
                    storage_DAO.remove(id_delete)
                    print(f"Produto com ID {id_delete} removido com sucesso.")

        elif sub_option == 5:
            clear()
            orders = storage_DAO.get_all_orders()
            if not orders:
                print("Nenhum pedido foi realizado ainda.")
            else:
                print(
                    "\nID | CLIENTE | PRODUTO | QUANTIDADE | VALOR un | VALOR TOTAL | DATA")
                print("-" * 70)
                for order in orders:
                    order_price = order[3] * order[4]
                    print(f"{order[0]} | {order[1]} | {order[2]} | {order[3]} | R$ {str(f'{order[4]}').replace('.', ',')} | R$ {str(f'{order_price:.2f}').replace(
                        '.', ',')} | {order[5]}")
                pause()

        elif sub_option == 6:
            print("SAINDO")
            break

        else:
            print("DIGITE UMA OPÇÃO VÁLIDA!")
