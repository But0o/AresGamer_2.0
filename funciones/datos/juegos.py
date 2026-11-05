"""Biblioteca de juegos: carga, guardado, busquedas y validacion de datos."""

import json
import re
from datetime import date

from funciones.datos.archivos import guardar_archivos, leer_lista, validar_registros
from funciones.datos.instalaciones import pcs_de_juego

ARCHIVO_JUEGOS = "juegos.json"
CAMPOS_JUEGO = ["nombre", "categoria", "fecha_lanzamiento", "peso"]
UNIDADES_PESO = ["MB", "GB"]
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
FECHA_SIN_DEFINIR = "Coming soon"


def cargar_juegos() -> list[dict]:
    """
    Contrato: Carga y valida la biblioteca completa de juegos
    Precondiciones: -
    Postcondiciones: Devuelve la lista de juegos. Lanza ErrorDeDatos si el archivo falta o es incorrecto
    """
    juegos = leer_lista(ARCHIVO_JUEGOS)
    validar_registros(juegos, ARCHIVO_JUEGOS, CAMPOS_JUEGO)
    return juegos


def texto_juegos(juegos: list[dict]) -> str:
    """
    Contrato: Arma el texto del archivo de juegos
    Precondiciones: juegos es una lista de diccionarios con los campos de CAMPOS_JUEGO
    Postcondiciones: Devuelve el texto en formato JSON, listo para guardar
    """
    return json.dumps(juegos, indent=4, ensure_ascii=False)


def guardar_juegos(juegos: list[dict]) -> None:
    """
    Contrato: Guarda la biblioteca completa de juegos en data/juegos.json
    Precondiciones: juegos es una lista de diccionarios con los campos de CAMPOS_JUEGO
    Postcondiciones: El archivo queda con el contenido de juegos. Lanza ErrorDeDatos si no se pudo guardar
    """
    guardar_archivos({ARCHIVO_JUEGOS: texto_juegos(juegos)})


def buscar_juego(juegos: list[dict], nombre: str) -> dict | None:
    """
    Contrato: Busca un juego por su nombre completo, sin distinguir mayusculas
    Precondiciones: juegos es la lista devuelta por cargar_juegos
    Postcondiciones: Devuelve el diccionario del juego o None si no existe
    """
    for juego in juegos:
        if juego["nombre"].lower() == nombre.lower():
            return juego

    return None


def buscar_juegos(juegos: list[dict], texto: str) -> list[dict]:
    """
    Contrato: Busca los juegos cuyo nombre o categoria contiene el texto, sin distinguir mayusculas
    Precondiciones: juegos es la lista devuelta por cargar_juegos. texto es un string no vacio
    Postcondiciones: Devuelve una lista nueva con los juegos que coinciden (puede estar vacia)
    """
    texto = texto.lower()
    resultados = []

    for juego in juegos:
        if texto in juego["nombre"].lower() or texto in juego["categoria"].lower():
            resultados.append(juego)

    return resultados


def juegos_de_pc(juegos: list[dict], instalaciones: list[dict], pc: str) -> list[dict]:
    """
    Contrato: Devuelve los juegos de la biblioteca que estan instalados en una PC
    Precondiciones: juegos es la lista devuelta por cargar_juegos. instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Devuelve una lista nueva, en el orden de las instalaciones. Ignora los juegos que no estan en juegos
    """
    resultado = []

    for instalacion in instalaciones:
        if instalacion["pc"] == pc:
            juego = buscar_juego(juegos, instalacion["juego"])
            if juego is not None:
                resultado.append(juego)

    return resultado


def juegos_sin_instalar(juegos: list[dict], instalaciones: list[dict]) -> list[dict]:
    """
    Contrato: Devuelve los juegos de la biblioteca que no estan instalados en ninguna PC
    Precondiciones: juegos es la lista devuelta por cargar_juegos. instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Devuelve una lista nueva (vacia si estan todos instalados)
    """
    resultado = []

    for juego in juegos:
        if len(pcs_de_juego(juego["nombre"], instalaciones)) == 0:
            resultado.append(juego)

    return resultado


def normalizar_peso(texto: str) -> str | None:
    """
    Contrato: Valida un peso con el formato "numero unidad", como "10 MB" o "1.5 gb"
    Precondiciones: texto es un string
    Postcondiciones: Devuelve el peso con la unidad en mayusculas, o None si el formato es invalido o el numero no es mayor a cero
    """
    partes = texto.split()

    if len(partes) != 2 or partes[1].upper() not in UNIDADES_PESO:
        return None

    if re.fullmatch(r"[0-9]+(\.[0-9]+)?", partes[0]) is None or float(partes[0]) <= 0:
        return None

    return partes[0] + " " + partes[1].upper()


def fecha_valida(texto: str) -> bool:
    """
    Contrato: Indica si una fecha de lanzamiento tiene el formato de la biblioteca, como "Jun 6, 2016", o es "Coming soon"
    Precondiciones: texto es un string
    Postcondiciones: Devuelve True si tiene el formato y es una fecha que existe, False si no
    """
    if texto == FECHA_SIN_DEFINIR:
        return True

    partes = re.fullmatch(r"([A-Z][a-z]{2}) ([0-9]{1,2}), ([0-9]{4})", texto)

    if partes is None or partes[1] not in MESES:
        return False

    try:
        date(int(partes[3]), MESES.index(partes[1]) + 1, int(partes[2]))
    except ValueError:
        return False

    return True
