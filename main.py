""" AresGamer 2.0"""

from funciones.menu import mostrar_menu, pedir_opcion
from funciones.juegos import mostrar_juegos, cargar_juegos

TITULO = "===== AresGamer 2.0 ====="
JUEGOS = cargar_juegos()

opciones_inicio = {
    "1": "Login",
    "2": "Busqueda de juegos disponibles",
    "3": "Listado de juegos en la biblioteca",
    "4": "Consultar juegos instalados",
    "5": "Salir"
}

def menu_inicial():

    while True:
        mostrar_menu(TITULO, opciones_inicio)
        opcion = pedir_opcion(opciones_inicio)

        if opcion == "1":
            print("\n[Pendiente] Login.")
        elif opcion == "2":
            print("\n[Pendiente] Busqueda de juegos disponibles.")
        elif opcion == "3":
            {mostrar_juegos(JUEGOS)}
        elif opcion == "4":
            print("\n[Pendiente] Consultar juegos instalados") 
        elif opcion == "5":
            print("\n Hasta luego.")
            break

if __name__ == "__main__":
    menu_inicial()