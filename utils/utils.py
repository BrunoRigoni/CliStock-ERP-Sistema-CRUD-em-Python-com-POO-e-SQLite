import os


def clear():
    if os.name == "nt":
        _ = os.system("cls")


def pause():
    input("ENTER para continuar.")
