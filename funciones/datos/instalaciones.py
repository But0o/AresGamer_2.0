"""Registro de instalaciones: que juego esta instalado en que PC."""

import json

from funciones.datos.archivos import guardar_archivos, leer_lista, validar_registros

ARCHIVO_INSTALACIONES = "instalaciones.json"
CAMPOS_INSTALACION = ["juego", "pc"]


def cargar_instalaciones() -> list[dict]:
    """
    Contrato: Carga y valida el registro de instalaciones
    Precondiciones: -
    Postcondiciones: Devuelve la lista de instalaciones (puede estar vacia). Lanza ErrorDeDatos si el archivo falta o es incorrecto
    """
    instalaciones = leer_lista(ARCHIVO_INSTALACIONES)
    validar_registros(instalaciones, ARCHIVO_INSTALACIONES, CAMPOS_INSTALACION)
    return instalaciones


def texto_instalaciones(instalaciones: list[dict]) -> str:
    """
    Contrato: Arma el texto del archivo: una instalacion por linea y una linea en blanco al cambiar de PC
    Precondiciones: instalaciones es una lista de diccionarios con las claves "juego" y "pc"
    Postcondiciones: Devuelve el texto en formato JSON, listo para guardar
    """
    if len(instalaciones) == 0:
        return "[]"

    lineas = []
    pc_anterior = instalaciones[0]["pc"]

    for instalacion in instalaciones:
        if instalacion["pc"] != pc_anterior:
            lineas.append("")
            pc_anterior = instalacion["pc"]

        juego = json.dumps(instalacion["juego"], ensure_ascii=False)
        pc = json.dumps(instalacion["pc"], ensure_ascii=False)
        lineas.append("  { " + f'"juego": {juego}, "pc": {pc}' + " },")

    # La ultima instalacion no lleva coma para que el JSON sea valido
    lineas[-1] = lineas[-1].removesuffix(",")

    return "[\n" + "\n".join(lineas) + "\n]"


def guardar_instalaciones(instalaciones: list[dict]) -> None:
    """
    Contrato: Guarda el registro de instalaciones en data/instalaciones.json
    Precondiciones: instalaciones es una lista de diccionarios con las claves "juego" y "pc"
    Postcondiciones: El archivo queda con el contenido de instalaciones. Lanza ErrorDeDatos si no se pudo guardar
    """
    guardar_archivos({ARCHIVO_INSTALACIONES: texto_instalaciones(instalaciones)})


def pcs_de_juego(nombre_juego: str, instalaciones: list[dict]) -> list[str]:
    """
    Contrato: Busca en que PCs esta instalado un juego
    Precondiciones: instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Devuelve una lista nueva con los nombres de las PCs (vacia si no esta en ninguna)
    """
    pcs = []

    for instalacion in instalaciones:
        if instalacion["juego"] == nombre_juego:
            pcs.append(instalacion["pc"])

    return pcs


def juegos_instalados_en(instalaciones: list[dict], pc: str) -> list[str]:
    """
    Contrato: Devuelve los nombres de los juegos instalados en una PC
    Precondiciones: instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Devuelve una lista nueva con los nombres, en el orden del archivo (vacia si no tiene ninguno)
    """
    nombres = []

    for instalacion in instalaciones:
        if instalacion["pc"] == pc:
            nombres.append(instalacion["juego"])

    return nombres


def instalar_juego(instalaciones: list[dict], nombre_juego: str, pc: str) -> bool:
    """
    Contrato: Agrega una instalacion a la lista, sin permitir duplicados
    Precondiciones: instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Si el juego no estaba en esa PC, lo agrega al final y devuelve True. Si ya estaba, no cambia nada y devuelve False
    """
    if nombre_juego in juegos_instalados_en(instalaciones, pc):
        return False

    instalaciones.append({"juego": nombre_juego, "pc": pc})

    return True


def desinstalar_juego(instalaciones: list[dict], nombre_juego: str, pc: str) -> bool:
    """
    Contrato: Saca de la lista la instalacion de un juego en una PC
    Precondiciones: instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Si el juego estaba en esa PC, lo saca y devuelve True. Si no estaba, no cambia nada y devuelve False
    """
    for instalacion in instalaciones:
        if instalacion["juego"] == nombre_juego and instalacion["pc"] == pc:
            instalaciones.remove(instalacion)
            return True

    return False


def quitar_instalaciones_de_juego(
    instalaciones: list[dict], nombre_juego: str
) -> list[dict]:
    """
    Contrato: Devuelve las instalaciones sin las que corresponden a un juego
    Precondiciones: instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Devuelve una lista nueva. No modifica la recibida
    """
    restantes = []

    for instalacion in instalaciones:
        if instalacion["juego"] != nombre_juego:
            restantes.append(instalacion)

    return restantes


def quitar_instalaciones_de_pc(instalaciones: list[dict], pc: str) -> list[dict]:
    """
    Contrato: Devuelve las instalaciones sin las que corresponden a una PC
    Precondiciones: instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Devuelve una lista nueva. No modifica la recibida
    """
    restantes = []

    for instalacion in instalaciones:
        if instalacion["pc"] != pc:
            restantes.append(instalacion)

    return restantes
