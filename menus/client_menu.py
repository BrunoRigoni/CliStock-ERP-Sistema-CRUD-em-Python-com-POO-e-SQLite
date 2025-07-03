
from menus.admin_menu import storageDAO
from utils.utils import clear, pause
from view.view_products import view_products


def client_menu(name):
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
        elif options == 3:
            clear()
            print(f"Saindo...")
            break

        else:
            print(f"Opção inválida!")
            pause()
