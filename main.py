from models.users import User, UserDAO
from menus.admin_menu import admin_menu
from menus.client_menu import client_menu
from utils.utils import pause, clear
import getpass


def main_menu():
    user_dao = UserDAO()

    while True:
        print(
            """
===== MENU PRINCIPAL =====
[1] Cadastrar
[2] Login
[3] Sair
"""
        )
        try:
            option = int(input(f"\n [Choose an Option: "))
        except ValueError:
            print("Digite uma opção válida.")
            continue

        if option == 1:
            name = input("NOME: ")
            mail = input("EMAIL: ")
            try:
                password = getpass.getpass("SENHA: ")
            except Exception as e:
                print(f"Digite uma senha válida. {e}")
                continue
            isadm = input("[ADM]|[CLIENT: ] ").lower()

            if isadm not in ["adm", "client"]:
                print("Tipo inválido. Use 'ADM ou 'CLIENT'.")
                continue
            else:
                print(f"{mail} -> {name} CADASTRADO COMO {isadm} COM SUCESSO.")
                new_user = User(name, mail, password, isadm)
                user_dao.register(new_user)

        elif option == 2:
            clear()
            mail = input("EMAIL: ")
            password = getpass.getpass("SENHA: ")
            user = user_dao.authenticate(mail, password)

            if user:
                user_id, name, mail, isadm = user
                if isadm == "adm":
                    admin_menu(user_id, name)
                elif isadm == "client":
                    client_menu(user_id, name)
                else:
                    print("Tipo de usuário inválido.")
                    pause()
            else:
                print("Login falhou! Verifique EMAIL/SENHA")
                pause()
        elif option == 3:
            clear()
            print("SAINDO...")
            pause()

        else:
            print("Opção inválida.")
            pause()


main_menu()
