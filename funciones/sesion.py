"""Login y menus: arma las opciones de cada rol y ejecuta la elegida."""

from collections.abc import Callable

from funciones.acciones.biblioteca import (
    agregar_juego,
    buscar_en_biblioteca,
    eliminar_juego,
    listar_juegos,
    listar_sin_instalar,
)
from funciones.acciones.instalaciones import (
    consultar_instalados,
    desinstalar_de_pc,
    instalar_en_pc,
)
from funciones.acciones.pcs import agregar_pc, bloquear_desbloquear_pc, eliminar_pc
from funciones.acciones.permisos import otorgar_admin, quitar_admin
from funciones.consola.menu import mostrar_menu, pedir_opcion
from funciones.datos.archivos import ErrorDeDatos
from funciones.datos.cuentas import (
    ROL_ADMIN,
    cargar_cuentas,
    cuenta_activa,
    verificar_credenciales,
)

TITULO = "===== AresGamer 2.0 ====="
MAX_INTENTOS = 3
CERRAR_SESION = "Cerrar sesion"


def iniciar_sesion(cuentas: list[dict]) -> dict | None:
    """
    Contrato: Pide usuario y clave por consola hasta un maximo de MAX_INTENTOS intentos
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Devuelve la cuenta si las credenciales son correctas y no esta bloqueada. Devuelve None si se agotan los intentos
    """
    intentos = 0

    while intentos < MAX_INTENTOS:
        usuario = input("\nUsuario: ").strip()
        clave = input("Clave: ").strip()

        if usuario == "" or clave == "":
            print("Hay que completar los campos usuario y clave")
        else:
            cuenta = verificar_credenciales(cuentas, usuario, clave)
            if cuenta is None:
                print("Usuario o clave incorrectos")
            elif cuenta_activa(cuenta):
                return cuenta
            else:
                print("Esta cuenta está bloqueada, consultá con el administrador")

        intentos += 1
        if intentos < MAX_INTENTOS:
            print("Intentos restantes:", MAX_INTENTOS - intentos)

    print("Demasiados intentos fallidos, volviendo al menu")
    return None


def opciones_de_usuario(
    juegos: list[dict], usuario: dict
) -> list[tuple[str, Callable[[], None] | None]]:
    """
    Contrato: Arma las opciones del menu segun el rol del usuario. Para agregar una opcion, alcanza con sumarla a la lista
    Precondiciones: juegos es la biblioteca cargada en memoria. usuario es la cuenta logueada
    Postcondiciones: Devuelve una lista de (descripcion, accion), en orden. La accion de cerrar sesion es None
    """
    if usuario["rol"] == ROL_ADMIN:
        return [
            ("Listado de juegos", lambda: listar_juegos(juegos, usuario)),
            ("Buscar juego", lambda: buscar_en_biblioteca(juegos, usuario)),
            ("Agregar juego", lambda: agregar_juego(juegos)),
            ("Eliminar juego", lambda: eliminar_juego(juegos)),
            ("Consultar juegos instalados", consultar_instalados),
            ("Instalar juego en una PC", lambda: instalar_en_pc(juegos)),
            ("Desinstalar juego de una PC", desinstalar_de_pc),
            ("Juegos sin instalar", lambda: listar_sin_instalar(juegos, usuario)),
            ("Agregar PC-Usuario", agregar_pc),
            ("Eliminar PC-Usuario", eliminar_pc),
            ("Bloquear/desbloquear PC-Usuario", bloquear_desbloquear_pc),
            ("Otorgar permiso de administrador", otorgar_admin),
            ("Quitar permiso de administrador", lambda: quitar_admin(usuario)),
            (CERRAR_SESION, None),
        ]

    return [
        ("Listado de juegos instalados", lambda: listar_juegos(juegos, usuario)),
        ("Buscar juego", lambda: buscar_en_biblioteca(juegos, usuario)),
        (CERRAR_SESION, None),
    ]


def menu_sesion(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Muestra el menu del usuario logueado y ejecuta la opcion elegida hasta que cierra sesion
    Precondiciones: juegos es la biblioteca cargada en memoria. usuario es la cuenta logueada
    Postcondiciones: Termina cuando el usuario elige cerrar sesion. Si una accion falla por un problema con los datos, muestra el error y sigue en el menu
    """
    opciones = opciones_de_usuario(juegos, usuario)
    descripciones = {}
    acciones = {}

    for numero, (descripcion, accion) in enumerate(opciones, start=1):
        descripciones[str(numero)] = descripcion
        acciones[str(numero)] = accion

    while True:
        mostrar_menu(TITULO, descripciones)
        accion = acciones[pedir_opcion(descripciones)]

        if accion is None:
            print("Sesión Cerrada")
            return

        try:
            accion()
        except ErrorDeDatos as error:
            print(f"Error: {error}")


def menu_inicial(juegos: list[dict]) -> None:
    """
    Contrato: Muestra el menu inicial (Login / Salir) y si el login es correcto abre el menu del usuario
    Precondiciones: juegos es la biblioteca cargada en memoria
    Postcondiciones: Termina cuando el usuario elige "Salir"
    """
    opciones = {"1": "Login", "2": "Salir"}

    while True:
        mostrar_menu(TITULO, opciones)

        if pedir_opcion(opciones) == "2":
            print("Hasta luego")
            return

        try:
            cuenta = iniciar_sesion(cargar_cuentas())
        except ErrorDeDatos as error:
            print(f"Error al cargar las cuentas: {error}")
            continue

        if cuenta is not None:
            print(f"Bienvenido {cuenta['usuario']}")
            menu_sesion(juegos, cuenta)
