""" AresGamer 2.0"""

from funciones.menu import mostrar_menu, pedir_opcion
from funciones.juegos import mostrar_juegos, cargar_juegos, buscar_juegos
from funciones.login import cargar_cuentas, iniciar_sesion

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
            try:
                cuentas = cargar_cuentas()
                cuenta = iniciar_sesion(cuentas)
            except (FileNotFoundError, ValueError) as error:
                print("\nError al cargar las cuentas:", error)
            else:
                if cuenta == None:
                    print("\nDemasiados intentos fallidos. Volviendo al menu")
                elif cuenta["rol"] == "admin":
                    print("\nBienvenido, administrador")
                    print("[Pendiente] Menu de administrador")
                else:
                    print("\nBienvenido", cuenta["usuario"])
                    print("[Pendiente] Menu de PC-Usuario")
        elif opcion == "2":
            texto = input("\nIngresa nombre o categoria a buscar: ").strip()
            if texto == "":
                print("Tenes que escribir algo para buscar")
            else:
                resultados = buscar_juegos(JUEGOS,texto)
                if len(resultados) == 0:
                    print("No se encontraron juegos para '" + texto + "'")
                else:
                    mostrar_juegos(resultados)
        elif opcion == "3":
            {mostrar_juegos(JUEGOS)}
        elif opcion == "4":
            print("\n[Pendiente] Consultar juegos instalados") 
        elif opcion == "5":
            print("\n Hasta luego.")
            break

if __name__ == "__main__":
    menu_inicial()