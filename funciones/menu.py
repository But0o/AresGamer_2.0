"""Dibujo de menus por consola muestra y pide opciones."""

from tabulate import tabulate

def mostrar_menu(titulo, opciones):
    """
    Contrato: Muestra por consola un titulo y una tabla con las opciones del menu
    Precondiciones:titulo es un string. opciones es un diccionario {numero: descripcion}, ambos string
    Postcondiciones: Imprime el titulo y la tabla en pantalla. No modifica opciones ni devuelve nada
    """

    filas = []
    for numero in opciones:
        filas.append([numero, opciones[numero]])

    print()
    print(titulo)
    print(tabulate(filas, headers=["Opciones", "Descripcion"], tablefmt="grid")) 
    #headers y talbefmt son parametreos de tabulate.


def pedir_opcion(opciones):
    """
    Contrato: Pide al usuario una opcion hasta que ingrese una que exista en el menu
    Precondiciones: opciones es un diccionario no vacio cuyas claves son strings
    Postcondiciones: Devuelve una clave valida de opciones. Imprime un mensaje de error oir cada entrada invalida
    """

    while True:
        elegida = input("\nElegi una opcion: ").strip() # strip limpia los espacios que el usuario puede llegar a tipear
        if elegida in opciones:
            return elegida
        print("Opcion invalida. Intenta de nuevo.")