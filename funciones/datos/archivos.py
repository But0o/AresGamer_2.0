"""Lectura y guardado seguro de los archivos JSON de la carpeta data/."""

import json
import os
from pathlib import Path

CARPETA_DATOS = Path(__file__).resolve().parents[2] / "data"


class ErrorDeDatos(Exception):
    """Un archivo de datos no se pudo leer, no tiene formato valido o no se pudo guardar."""


def leer_lista(nombre_archivo: str) -> list:
    """
    Contrato: Lee un archivo JSON de data/ que debe contener una lista
    Precondiciones: nombre_archivo es el nombre de un archivo dentro de data/
    Postcondiciones: Devuelve la lista. Lanza ErrorDeDatos si el archivo no existe, no se puede leer o no contiene una lista en formato JSON
    """
    ruta = CARPETA_DATOS / nombre_archivo

    try:
        # utf-8-sig acepta tambien los archivos con BOM que guardan algunos editores de Windows
        with open(ruta, "r", encoding="utf-8-sig") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise ErrorDeDatos(f"No se encontró el archivo data/{nombre_archivo}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ErrorDeDatos(f"{nombre_archivo} tiene un formato inválido")
    except OSError as error:
        raise ErrorDeDatos(f"No se pudo leer data/{nombre_archivo} ({error})")

    if not isinstance(datos, list):
        raise ErrorDeDatos(f"{nombre_archivo} debe contener una lista")

    return datos


def validar_registros(registros: list, nombre_archivo: str, campos: list[str]) -> None:
    """
    Contrato: Valida que cada registro sea un diccionario con todos los campos y que sean textos
    Precondiciones: registros es la lista leida del archivo. campos son los nombres de los campos obligatorios
    Postcondiciones: No devuelve nada si todo es correcto. Lanza ErrorDeDatos en el primer problema que encuentra
    """
    for registro in registros:
        if not isinstance(registro, dict):
            raise ErrorDeDatos(f"{nombre_archivo}: hay un elemento que no es válido")
        for campo in campos:
            if campo not in registro:
                raise ErrorDeDatos(f"{nombre_archivo}: a un elemento le falta el campo {campo}")
            if not isinstance(registro[campo], str):
                raise ErrorDeDatos(f"{nombre_archivo}: el campo {campo} debe ser un texto")


def guardar_archivos(contenidos: dict[str, str]) -> None:
    """
    Contrato: Guarda uno o mas archivos de data/ de forma conjunta
    Precondiciones: contenidos es un diccionario {nombre de archivo: texto a guardar}
    Postcondiciones: Todos los archivos quedan con su contenido nuevo. Si algo falla, lanza ErrorDeDatos y los archivos quedan como estaban
    """
    temporales = {}

    try:
        # Primero se escribe todo en temporales: si el disco falla, los originales ni se tocan
        for nombre, contenido in contenidos.items():
            temporales[nombre] = _escribir_temporal(nombre, contenido)

        anteriores = {nombre: _leer_si_existe(nombre) for nombre in contenidos}
        _reemplazar_originales(temporales, anteriores)
    except OSError as error:
        raise ErrorDeDatos(f"No se pudieron guardar los datos, no hubo cambios ({error})")
    finally:
        for temporal in temporales.values():
            temporal.unlink(missing_ok=True)


def _escribir_temporal(nombre: str, contenido: str) -> Path:
    """
    Contrato: Escribe el contenido en un archivo temporal al lado del original
    Precondiciones: nombre es el nombre de un archivo dentro de data/
    Postcondiciones: Devuelve la ruta del temporal. Lanza OSError si no se pudo escribir
    """
    temporal = CARPETA_DATOS / f"{nombre}.tmp"

    with open(temporal, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    return temporal


def _leer_si_existe(nombre: str) -> bytes | None:
    """
    Contrato: Lee el contenido actual de un archivo de data/
    Precondiciones: nombre es el nombre de un archivo dentro de data/
    Postcondiciones: Devuelve sus bytes, o None si el archivo no existe. Lanza OSError si no se pudo leer
    """
    try:
        return (CARPETA_DATOS / nombre).read_bytes()
    except FileNotFoundError:
        return None


def _reemplazar_originales(
    temporales: dict[str, Path], anteriores: dict[str, bytes | None]
) -> None:
    """
    Contrato: Reemplaza cada original por su temporal, y si uno falla vuelve atras los ya reemplazados
    Precondiciones: temporales y anteriores tienen los mismos nombres de archivo
    Postcondiciones: Los originales quedan todos con el contenido nuevo. Si falla, vuelve atras y lanza OSError
    """
    reemplazados = []

    try:
        for nombre, temporal in temporales.items():
            os.replace(temporal, CARPETA_DATOS / nombre)
            reemplazados.append(nombre)
    except OSError:
        for nombre in reemplazados:
            ruta = CARPETA_DATOS / nombre
            if anteriores[nombre] is None:
                ruta.unlink(missing_ok=True)
            else:
                ruta.write_bytes(anteriores[nombre])
        raise
