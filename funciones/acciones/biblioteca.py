"""Acciones sobre la biblioteca: listar, buscar, agregar y eliminar juegos."""

from funciones.consola.entrada import confirmar, pedir_nombre_nuevo, pedir_texto
from funciones.consola.tablas import mostrar_juegos
from funciones.datos.archivos import guardar_archivos
from funciones.datos.cuentas import ROL_PC
from funciones.datos.instalaciones import (
    ARCHIVO_INSTALACIONES,
    cargar_instalaciones,
    pcs_de_juego,
    quitar_instalaciones_de_juego,
    texto_instalaciones,
)
from funciones.datos.juegos import (
    ARCHIVO_JUEGOS,
    buscar_juego,
    buscar_juegos,
    fecha_valida,
    guardar_juegos,
    juegos_de_pc,
    juegos_sin_instalar,
    normalizar_peso,
    texto_juegos,
)


def listar_juegos(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Muestra la biblioteca segun el rol del usuario (el admin ve todos los juegos, la PC solo los suyos)
    Precondiciones: juegos es la biblioteca cargada en memoria. usuario es la cuenta logueada
    Postcondiciones: Imprime la tabla de juegos
    """
    mostrar_juegos(juegos, cargar_instalaciones(), usuario)


def buscar_en_biblioteca(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Pide un texto y muestra los juegos que coinciden. Una PC busca solo entre sus juegos instalados
    Precondiciones: juegos es la biblioteca cargada en memoria. usuario es la cuenta logueada
    Postcondiciones: Imprime la tabla de resultados, o un aviso si el texto esta vacio o no hay coincidencias
    """
    texto = input("Ingresa un nombre o categoría a buscar: ").strip()

    if texto == "":
        print("Hay que escribir algo para buscar")
        return

    instalaciones = cargar_instalaciones()
    biblioteca = juegos

    if usuario["rol"] == ROL_PC:
        biblioteca = juegos_de_pc(juegos, instalaciones, usuario["usuario"])

    resultados = buscar_juegos(biblioteca, texto)

    if len(resultados) == 0:
        print(f"No se encontraron juegos para {texto}")
        return

    mostrar_juegos(resultados, instalaciones, usuario)


def _pedir_peso() -> str:
    """
    Contrato: Pide el peso de un juego hasta que tenga un formato valido
    Precondiciones: -
    Postcondiciones: Devuelve el peso, con la unidad en mayusculas
    """
    while True:
        peso = normalizar_peso(input("Peso (ej: 10 MB, 1.5 GB): "))
        if peso is not None:
            return peso
        print("Formato inválido. Escribí un número y la unidad (ej: 10 MB, 1.5 GB)")


def _pedir_fecha() -> str:
    """
    Contrato: Pide la fecha de lanzamiento de un juego hasta que tenga un formato valido
    Precondiciones: -
    Postcondiciones: Devuelve una fecha como "Jun 6, 2016", o "Coming soon"
    """
    while True:
        fecha = pedir_texto("Fecha de lanzamiento (ej: Jun 6, 2016 o Coming soon): ")
        if fecha_valida(fecha):
            return fecha
        print("Fecha inválida. Usá el mes en inglés (ej: Jun 6, 2016) o Coming soon")


def _pedir_datos_juego(juegos: list[dict]) -> dict | None:
    """
    Contrato: Pide y valida los datos de un juego nuevo
    Precondiciones: juegos es la biblioteca cargada en memoria (para evitar nombres repetidos)
    Postcondiciones: Devuelve el diccionario del juego nuevo. Devuelve None si el nombre se deja vacio
    """
    nombre = pedir_nombre_nuevo(
        "Nombre del juego (vacío para cancelar): ",
        lambda texto: buscar_juego(juegos, texto) is not None,
        "Ya existe un juego llamado '{}'",
    )

    if nombre is None:
        return None

    return {
        "nombre": nombre,
        "categoria": pedir_texto("Categoria/s (ej: Action, Indie): "),
        "fecha_lanzamiento": _pedir_fecha(),
        "peso": _pedir_peso(),
    }


def agregar_juego(juegos: list[dict]) -> None:
    """
    Contrato: Pide los datos de un juego nuevo, lo agrega a la biblioteca y guarda los cambios
    Precondiciones: juegos es la biblioteca cargada en memoria
    Postcondiciones: Si el admin confirma y se pudo guardar, juegos y el archivo quedan con el juego nuevo al final. Si cancela, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    nuevo = _pedir_datos_juego(juegos)

    if nuevo is None:
        print("Operación cancelada")
        return

    print(
        f"Juego nuevo: {nuevo['nombre']} | {nuevo['categoria']} | {nuevo['fecha_lanzamiento']} | {nuevo['peso']}"
    )

    if not confirmar("¿Agregarlo a la biblioteca? (s/n): "):
        print("Operación cancelada")
        return

    guardar_juegos(juegos + [nuevo])
    juegos.append(nuevo)

    print(f"Juego '{nuevo['nombre']}' agregado correctamente")


def eliminar_juego(juegos: list[dict]) -> None:
    """
    Contrato: Elimina un juego de la biblioteca y de las PCs donde esta instalado, y guarda los cambios
    Precondiciones: juegos es la biblioteca cargada en memoria
    Postcondiciones: Si el admin confirma y se pudo guardar, el juego se quita de juegos y de los dos archivos. Si cancela, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    nombre = input("Nombre del juego a eliminar (vacío para cancelar): ").strip()

    if nombre == "":
        print("Operación cancelada")
        return

    juego = buscar_juego(juegos, nombre)

    if juego is None:
        print(f"No existe ningún juego llamado '{nombre}'")
        return

    instalaciones = cargar_instalaciones()
    pcs = pcs_de_juego(juego["nombre"], instalaciones)

    print(f"Juego a eliminar: {juego['nombre']}")
    if len(pcs) > 0:
        print(f"Está instalado en: {', '.join(pcs)}. También se quitará de esas PCs")

    if not confirmar("¿Eliminarlo definitivamente? (s/n): "):
        print("Operación cancelada")
        return

    restantes = []
    for otro in juegos:
        if otro is not juego:
            restantes.append(otro)

    guardar_archivos(
        {
            ARCHIVO_JUEGOS: texto_juegos(restantes),
            ARCHIVO_INSTALACIONES: texto_instalaciones(
                quitar_instalaciones_de_juego(instalaciones, juego["nombre"])
            ),
        }
    )
    juegos.remove(juego)

    print(f"Juego '{juego['nombre']}' eliminado correctamente")


def listar_sin_instalar(juegos: list[dict], usuario: dict) -> None:
    """
    Contrato: Muestra los juegos de la biblioteca que no estan instalados en ninguna PC
    Precondiciones: juegos es la biblioteca cargada en memoria. usuario es la cuenta logueada
    Postcondiciones: Imprime la tabla de juegos sin instalar, o un aviso si estan todos instalados
    """
    instalaciones = cargar_instalaciones()
    sin_instalar = juegos_sin_instalar(juegos, instalaciones)

    if len(sin_instalar) == 0:
        print("Todos los juegos están instalados en al menos una PC")
        return

    print(f"Juegos que no están instalados en ninguna PC ({len(sin_instalar)}):")
    mostrar_juegos(sin_instalar, instalaciones, usuario)
