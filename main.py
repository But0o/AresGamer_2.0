"""AresGamer 2.0"""

from funciones.menu import mostrar_menu, pedir_opcion, confirmar
from funciones.juegos import (
    mostrar_juegos,
    cargar_juegos,
    buscar_juegos,
    guardar_juegos,
    pedir_datos_juego,
    buscar_juego_por_nombre,
)
from funciones.instalaciones import (
    cargar_instalaciones,
    guardar_instalaciones,
    quitar_instalaciones_de_juego,
    pcs_de_juego,
    juegos_instalados_en,
    instalar_juego,
    desinstalar_juego,
)
from funciones.login import cargar_cuentas, iniciar_sesion

TITULO = "===== AresGamer 2.0 ====="

opciones_no_logueado = {"1": "Login", "2": "Salir"}

opciones_admin = {
    "1": "Listado de juegos",
    "2": "Buscar juego",
    "3": "Agregar juego",
    "4": "Eliminar juego",
    "5": "Consultar juegos instalados",
    "6": "Instalar juego en una PC",
    "7": "Desinstalar juego de una PC",
    "8": "Cerrar sesion",
}

opciones_pc = {
    "1": "Listado de juegos instalados",
    "2": "Buscar juego",
    "3": "Cerrar sesion",
}


def listar_juegos(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Muestra los juegos recibidos segun el rol del usuario (el admin ve todos con sus instalaciones, la PC solo los suyos)
    Precondiciones: juegos es una lista de juegos válidos. usuario es un diccionario con las claves "usuario" y "rol"
    Postcondiciones: Imprime la tabla de juegos, o un mensaje de error si no se pudieron cargar las instalaciones
    """
    try:
        instalaciones = cargar_instalaciones()
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al cargar las instalaciones: {error}")
        return

    mostrar_juegos(juegos, instalaciones, usuario)


def buscar_en_biblioteca(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Pide un texto por consola y muestra los juegos que coinciden con el, según el rol del usuario
    Precondiciones: juegos es una lista de juegos válidos. usuario es un diccionario con las claves "usuario" y "rol"
    Postcondiciones: Imprime la tabla de resultados o un aviso si el texto esta vacío o no hay coincidencias
    """
    texto = input("Ingresa un nombre o categoría a buscar: ").strip().lower()

    if texto == "":
        print("Hay que escribir algo para buscar")
        return

    resultados = buscar_juegos(juegos, texto)

    if len(resultados) == 0:
        print(f"No se encontraron juegos para {texto}")
        return

    listar_juegos(resultados, usuario)


def agregar_juego(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Pide los datos de un juego nuevo, lo agrega a la biblioteca y guarda los cambios es data/juegos.json
    Precondiciones: juegos es la lista de juegos cargada en memoria. usuario es el diccionario del administrador logueado
    Postcondiciones: Si el administrador confirma y el guardado funciona, juegos queda con el juego nuevo al final (se modifica la lista). Si cancela o el guardado falla, juegos queda sin cambios
    """
    nuevo = pedir_datos_juego(juegos)

    if nuevo is None:
        print("Operación cancelada")
        return

    print(
        f"Juego nuevo: {nuevo['nombre']} | {nuevo['categoria']} | {nuevo['fecha_lanzamiento']} | {nuevo['peso']}"
    )

    if not confirmar("¿Agregarlo a la biblioteca? (s/n): "):
        print("Operación cancelada")
        return

    juegos.append(nuevo)

    try:
        guardar_juegos(juegos)
    except OSError as error:
        juegos.pop()
        print(f"No se agregó el juego: {error}")
        return

    print(f"Juego '{nuevo['nombre']}' agregado correctamente")


def eliminar_juego(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Elimina un juego de la biblioteca y de las PC donde esta instalado y guarda los cambios en data/juegos.json y data/instalaciones.json
    Precondiciones: juegos es la lista de juegos cargada en memoria, usuario es el diccionario del admin logueado
    Postcondiciones: Si el admin confirma y el guardado funciona el juego se quita de juegos y de instalaciones.json
    """
    nombre = input("Nombre del juego a eliminar (vacío para cancelar): ").strip()

    if nombre == "":
        print("Operación cancelada")
        return

    juego = buscar_juego_por_nombre(juegos, nombre)

    if juego is None:
        print(f"No existe ningún juego llamado '{nombre}'")
        return

    try:
        instalaciones = cargar_instalaciones()
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al cargar las instalaciones: {error}")
        return

    pcs = pcs_de_juego(juego["nombre"], instalaciones)

    print(f"Juego a eliminar: {juego['nombre']}")
    if len(pcs) > 0:
        print(f"Esta instalado en: {', '.join(pcs)}. También se quitará de esas PCs")

    if not confirmar("¿Eliminarlo definitivamente? (s/n): "):
        print("Operación cancelada")
        return

    posicion = juegos.index(juego)
    juegos.remove(juego)

    try:
        guardar_juegos(juegos)
    except OSError as error:
        juegos.insert(
            posicion, juego
        )  # para que coincida lo que hay en memoria y lo que hay en archivo
        print(f"No se elimino el juego: {error}")
        return

    if len(pcs) > 0:
        try:
            guardar_instalaciones(
                quitar_instalaciones_de_juego(instalaciones, juego["nombre"])
            )
        except OSError as error:
            print(
                f"Juego eliminado, pero no se pudieron actualizar las instalaciones: {error}"
            )
            return

    print(f"Juego '{juego['nombre']}' eliminado correctamente")


def pedir_pc(cuentas: list[dict]) -> str | None:
    """
    Contrato: Pide el nombre de una PC-Usuario hasta que sea una cuenta existente con rol "pc"
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Devuelve el nombre de la PC (ej: "PC01"). Devuelve Nibe si no hay PC-Usuario o si se ingresa vacío en el nombre
    """
    pcs = []

    for cuenta in cuentas:
        if cuenta["rol"] == "pc":
            pcs.append(cuenta["usuario"])

    if len(pcs) == 0:
        print("No hay PC-Usuarios registradas")
        return None

    print(f"PCs disponibles: {', '.join(pcs)}")

    while True:
        nombre = input("Nombre de la PC (vacío para cancelar): ").strip()

        if nombre == "":
            return None

        for pc in pcs:
            if pc.lower() == nombre.lower():
                return pc

        print(f"No existe la PC '{nombre}'")


def pedir_juego(juegos: list[dict]) -> dict | None:
    """
    Contrato: Pide el nombre de un juego hasta que exista en la biblioteca
    Precondiciones: juegos es la lista de juegos cargada en memoria
    Postcondiciones: Devuelve el diccionario del juego. Devuelve None si se deja el nombre vacío
    """
    while True:
        nombre = input("Nombre del juego (vacío para cancelar): ").strip()

        if nombre == "":
            return None

        juego = buscar_juego_por_nombre(juegos, nombre)

        if juego is not None:
            return juego

        print(f"No existe el juego llamado '{nombre}'")


def elegir_pc() -> tuple[str, list[dict]] | None:
    """
    Contrato: Carga las cuentas y las instalaciones, y le pide al admin que elija una PC-Usuario
    Precondiciones: Existe data/cuentas.json y data/instalaciones.json con formato válido
    Postcondiciones: Devuelve una tupla (pc, instalaciones) con la PC elegida y la lista de instalaciones cargada. Devuelve None si no se pudieron cargar los archivos o si el admin cancela
    """
    try:
        cuentas = cargar_cuentas()
        instalaciones = cargar_instalaciones()
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al cargar los datos: {error}")
        return None

    pc = pedir_pc(cuentas)

    if pc is None:
        print("Operación cancelada")
        return None

    return pc, instalaciones


def instalar_en_pc(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Instala un juego de la biblioteca en una PC-Usuario y guarda el cambio en data/instalaciones.json
    Precondiciones: juegos es la lista de juegos cargada en memoria. usuario es el diccionario del admin logueado
    Postcondiciones: Si el admin confirma y el guardado funciona, instalaciones.json queda con la instalación nueva, si cancela, el guardado falla o el juego ya estaba instalado en esa PC, el archivo queda sin cambios
    """
    eleccion = elegir_pc()

    if eleccion is None:
        return

    pc, instalaciones = eleccion

    juego = pedir_juego(juegos)

    if juego is None:
        print("Operación cancelada")
        return

    if juego["nombre"] in juegos_instalados_en(instalaciones, pc):
        print(f"'{juego['nombre']}' ya está instalado en {pc}")
        return

    if not confirmar(f"¿Instalar '{juego['nombre']}' en {pc}? (s/n): "):
        print("Operación cancelada")
        return

    instalar_juego(instalaciones, juego["nombre"], pc)

    try:
        guardar_instalaciones(instalaciones)
    except OSError as error:
        print(f"No se instalo el juego: {error}")
        return

    print(f"Juego: '{juego['nombre']}' instalado en {pc}")


def desinstalar_de_pc(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Desinstala un juego de una Pc-Usuario y guarda el cambio en data/instalaciones.json
    Precondiciones: juegos es la lista de juegos cargada en memoria. usuario es el diccionario del admin logueado
    Postcondiciones: Si el admin confirma y el guardado funciona, instalaciones.json queda sin esa instalación. Si cancela, el guardado falla o la PC no tiene ese juego, el archivo queda sin cambios
    """
    eleccion = elegir_pc ()

    if eleccion is None:
        return

    pc, instalaciones = eleccion

    instalados = juegos_instalados_en(instalaciones, pc)

    if len(instalados) == 0:
        print(f"{pc} no tiene juegos instalados")
        return

    print(f"Juegos instalados en {pc}: {', '.join(instalados)}")

    nombre = input("Nombre del juego a desinstalar (vacío para cancelar): ").strip()

    if nombre == "":
        print("Operación cancelada")
        return

    elegido = None

    for instalado in instalados:
        if instalado.lower() == nombre.lower():
            elegido = instalado

    if elegido is None:
        print(f"'{nombre}' no esta instalado en {pc}")
        return

    if not confirmar(f"¿Desinstalar '{elegido}' de {pc}? (s/n): "):
        print("Operación cancelada")
        return

    desinstalar_juego(instalaciones, elegido, pc)

    try:
        guardar_instalaciones(instalaciones)
    except OSError as error:
        print(f"No se desinstalí el juego: {error}")
        return

    print(f"Juego '{elegido}' desinstalado de {pc}")


def hacer_login() -> dict | None:
    """
    Conrtato: Carga las cuentas e inicia el proceso de login por consola
    Precondiciones: Existe data/cuentas.json con cuentas válidas
    Postcondiciones: Devuelva la cuenta si el login es correcto, None si no lo es
    """
    try:
        cuentas = cargar_cuentas()
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al cargar las cuentas: {error}")
        return None

    cuenta = iniciar_sesion(cuentas)

    if cuenta is None:
        print("Demasiados intentos fallidos, volviendo al menu")

    return cuenta


def menu_sesion(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Muestra el menu del usuario logueado (admin o pc) y ejecula la opción elegida hasta que ceirra sesión
    Precondiciones: juegos es una lista de juegos válidos. usuario es un diccionario con las claves "usuario" y "rol", donde "rol" vale "admin" o "pc"
    Postcondiciones: Termina cuando el usuario elige "Cerrar sesión"
    """
    if usuario["rol"] == "admin":
        opciones_menu = opciones_admin
    else:
        opciones_menu = opciones_pc

    while True:
        mostrar_menu(TITULO, opciones_menu)
        opcion = pedir_opcion(opciones_menu)
        descripcion = opciones_menu[opcion]

        if descripcion == "Cerrar sesion":
            print("Sesión Cerrada")
            break
        elif (
            descripcion == "Listado de juegos"
            or descripcion == "Listado de juegos instalados"
        ):
            listar_juegos(juegos, usuario)
        elif descripcion == "Buscar juego":
            buscar_en_biblioteca(juegos, usuario)
        elif descripcion == "Agregar juego":
            agregar_juego(juegos, usuario)
        elif descripcion == "Eliminar juego":
            eliminar_juego(juegos, usuario)
        elif descripcion == "Consultar juegos instalados":
            print("[Pendiente] Consultar juegos instalados")
        elif descripcion == "Instalar juego en una PC":
            instalar_en_pc(juegos, usuario)
        elif descripcion == "Desinstalar juego de una PC":
            desinstalar_de_pc(juegos, usuario)


def menu_inicial(juegos: list[dict]):
    """
    Contrato: Muestra el menu inicial (Login / Salir) y si el login es correcto abre el menú del usuario
    Precondiciones: juegos es una lista de juegos válidos
    Postcondiciones: Termina cuando el usuario elige "Salir"
    """

    while True:
        mostrar_menu(TITULO, opciones_no_logueado)
        opcion = pedir_opcion(opciones_no_logueado)

        if opcion == "1":
            cuenta = hacer_login()
            if cuenta is not None:
                print(f"Bienvenido {cuenta['usuario']}")
                menu_sesion(juegos, cuenta)
        elif opcion == "2":
            print("Hasta luego")
            break


def main() -> None:
    """
    Contrato: Punto de entrada al programa, carga la bibloteca de juegos y arranca el menu inicial
    Precondiciones: Se ejecuta desde la carpeta raiz del proyecto y existe data/juegos.json
    Postcondiciones: Si no se puede cargar la biblioteca, muestra el motivo y sale, si no, termina cuando el usuario sale del menu inicial
    """

    try:
        juegos = cargar_juegos()
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al cargar la biblioteca de juegos: {error}")
        return

    menu_inicial(juegos)


if __name__ == "__main__":
    main()
