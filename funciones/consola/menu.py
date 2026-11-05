"""Dibujo de menus por consola: muestra y pide opciones."""

from tabulate import tabulate


def mostrar_menu(titulo: str, opciones: dict[str, str]) -> None:
    """
    Contrato: Muestra por consola un titulo y una tabla con las opciones del menu
    Precondiciones: opciones es un diccionario {numero: descripcion}, ambos string
    Postcondiciones: Imprime el titulo y la tabla. No modifica opciones
    """
    filas = []

    for numero in opciones:
        filas.append([numero, opciones[numero]])

    print()
    print(titulo)
    print(tabulate(filas, headers=["Opciones", "Descripcion"], tablefmt="grid"))


def pedir_opcion(opciones: dict[str, str]) -> str:
    """
    Contrato: Pide una opcion hasta que el usuario ingrese una que exista en el menu
    Precondiciones: opciones es un diccionario no vacio cuyas claves son strings
    Postcondiciones: Devuelve una clave valida de opciones. Imprime un mensaje de error por cada entrada invalida
    """
    while True:
        elegida = input("\nElegi una opcion: ").strip()
        if elegida in opciones:
            return elegida
        print("Opcion invalida. Intenta de nuevo.")
