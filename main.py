""" AresGamer 2.0"""

from funciones.menu import mostrar_menu, pedir_opcion
from funciones.juegos import mostrar_juegos, cargar_juegos, buscar_juegos
from funciones.instalaciones import cargar_instalaciones
from funciones.login import cargar_cuentas, iniciar_sesion

TITULO = "===== AresGamer 2.0 ====="
JUEGOS = cargar_juegos()

opciones_no_logueado = {
    "1": "Login",
    "2": "Salir"
}

opciones_admin = {
    "1": "Listado de juegos",
    "2": "Buscar juego",
    "3": "Agregar juego",
    "4": "Eliminar juego",
    "5": "Consultar juegos instalados",
    "6": "Cerrar sesion"
}

opciones_pc = {
    "1": "Listado de juegos instalados",
    "2": "Buscar juego",
    "3": "Cerrar sesion"
}

def menu_inicial():
    usuario_actual = None

    while True:
        mostrar_menu(TITULO, opciones_no_logueado)
        opcion = pedir_opcion(opciones_no_logueado)

        if opcion == "1":
            try:
                cuentas = cargar_cuentas()
                cuenta = iniciar_sesion(cuentas)
            except (FileNotFoundError, ValueError) as error:
                print("\nError al cargar las cuentas:", error)
                continue

            if cuenta is None:
                print("\nDemasiados intentos fallidos. Volviendo al menu")
            else:
                usuario_actual = cuenta
                print("\nBienvenido, " + cuenta["usuario"] + ".")

                while usuario_actual is not None:
                    if usuario_actual["rol"] == "admin":
                        opciones_menu = opciones_admin
                    else:
                        opciones_menu = opciones_pc

                    mostrar_menu(TITULO, opciones_menu)
                    opcion_interna = pedir_opcion(opciones_menu)
                    descripcion = opciones_menu[opcion_interna]

                    if descripcion == "Listado de juegos" or descripcion == "Listado de juegos instalados":
                        instalaciones = cargar_instalaciones()
                        mostrar_juegos(JUEGOS, instalaciones, usuario_actual)
                    elif descripcion == "Buscar juego":
                        texto = input("\nIngresa nombre o categoria a buscar: ").strip()
                        if texto == "":
                            print("Tenes que escribir algo para buscar")
                        else:
                            resultados = buscar_juegos(JUEGOS, texto)
                            if len(resultados) == 0:
                                print("No se encontraron juegos para '" + texto + "'")
                            else:
                                instalaciones = cargar_instalaciones()
                                mostrar_juegos(resultados, instalaciones, usuario_actual)
                    elif descripcion == "Agregar juego":
                        print("\n[Pendiente] Agregar juego.")
                    elif descripcion == "Eliminar juego":
                        print("\n[Pendiente] Eliminar juego.")
                    elif descripcion == "Consultar juegos instalados":
                        print("\n[Pendiente] Consultar juegos instalados.")
                    elif descripcion == "Cerrar sesion":
                        usuario_actual = None
                        print("\nSesion cerrada.")

        elif opcion == "2":
            print("\n Hasta luego.")
            break

if __name__ == "__main__":
    menu_inicial()