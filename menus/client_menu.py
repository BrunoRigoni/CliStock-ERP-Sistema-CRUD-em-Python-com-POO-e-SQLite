
from menus.admin_menu import storageDAO
from utils.utils import clear, pause
from view.view_products import view_products


def client_menu(user_id, name):
    dao = storageDAO()
    while True:
        print(f"\n[CLIENTE] Bem-vindo, {name}")
        print("[1] VER PRODUTOS")
        print("[2] FAZER PEDIDO")
        print("[3] SAIR")
        try:
            options = int(input("OPÇÃO QUE DESEJA REALIZAR: "))
        except ValueError:
            continue

        if options == 1:
            products = dao.get_produtcs_client()
            if not products:
                print(f"Nenhum produto disponivel ")
            else:
                view_products(products)

            pause()

        elif options == 2:
            clear()
            products = dao.get_produtcs_client()
            view_products(products)

            try:
                product_id = int(input(f"DIGITE O ID DO PRODUTO: "))
                products_quantity = int(input("DIGITE A QUANTIDADE: "))
            except ValueError:
                print("Valores inválidos.")
                pause()
                continue

            result = dao.create_new_order(
                user_id, product_id, products_quantity)
            print(result)
            pause()

        elif options == 3:
            clear()
            print(f"Saindo...")
            break

        else:
            print(f"Opção inválida!")
            pause()
