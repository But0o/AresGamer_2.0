"""Dibujo de menus por consola muestra y pide opciones."""

from tabulate import tabulate

def mostrar_menu(titulo, opciones):

    filas = []
    for numero in opciones:
        filas.append([numero, opciones[numero]])

    print()
    print(titulo)
    print(tabulate(filas, headers=["Opciones", "Descripcion"], tablefmt="grid")) 
    #headers y talbefmt son parametreos de tabulate.


def pedir_opcion(opciones):

    while True:
        elegida = input("\nElegi una opcion: ").strip() # strip limpia los espacios que el usuario puede llegar a tipear
        if elegida in opciones:
            return elegida
        print("Opcion invalida. Intenta de nuevo.")