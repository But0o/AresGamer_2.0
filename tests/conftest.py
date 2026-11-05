"""Preparacion comun de los tests: datos temporales y teclado simulado."""

import json

import pytest

from funciones.datos import archivos

JUEGOS = [
    {"nombre": "SOMA", "categoria": "Action, Indie", "fecha_lanzamiento": "Sep 21, 2015", "peso": "20 GB"},
    {"nombre": "Portal", "categoria": "Puzzle", "fecha_lanzamiento": "Oct 10, 2007", "peso": "4 GB"},
    {"nombre": "Tetris", "categoria": "Puzzle, Indie", "fecha_lanzamiento": "Jun 6, 1984", "peso": "10 MB"},
]
CUENTAS = [
    {"usuario": "admin", "clave": "admin123", "rol": "admin"},
    {"usuario": "PC01", "clave": "1234", "rol": "pc"},
    {"usuario": "PC02", "clave": "1234", "rol": "pc"},
    {"usuario": "PC03", "clave": "1234", "rol": "pc"},
]
INSTALACIONES = [
    {"juego": "SOMA", "pc": "PC01"},
    {"juego": "Portal", "pc": "PC01"},
    {"juego": "SOMA", "pc": "PC02"},
]


class Datos:
    """Acceso de los tests a los archivos de la carpeta de datos temporal."""

    def __init__(self, carpeta):
        self.carpeta = carpeta

    def leer(self, nombre):
        return json.loads((self.carpeta / nombre).read_text(encoding="utf-8"))

    def escribir(self, nombre, contenido):
        texto = contenido if isinstance(contenido, str) else json.dumps(contenido)
        (self.carpeta / nombre).write_text(texto, encoding="utf-8")

    def foto(self):
        """Devuelve el contenido exacto de todos los archivos, para comparar antes y despues."""
        return {ruta.name: ruta.read_bytes() for ruta in self.carpeta.iterdir()}


@pytest.fixture(autouse=True)
def datos(tmp_path, monkeypatch):
    """Es automatica: ningun test puede tocar la carpeta data/ real."""
    monkeypatch.setattr(archivos, "CARPETA_DATOS", tmp_path)
    prueba = Datos(tmp_path)
    prueba.escribir("juegos.json", JUEGOS)
    prueba.escribir("cuentas.json", CUENTAS)
    prueba.escribir("instalaciones.json", INSTALACIONES)
    return prueba


@pytest.fixture
def teclado(monkeypatch):
    """Simula lo que escribe el usuario. Falla si el programa pide mas datos de los previstos."""

    def preparar(*respuestas):
        pendientes = list(respuestas)

        def responder(mensaje=""):
            print(mensaje, end="")
            if len(pendientes) == 0:
                pytest.fail(f"El programa pidió un dato de más: {mensaje!r}")
            respuesta = pendientes.pop(0)
            if isinstance(respuesta, BaseException):
                raise respuesta
            print(respuesta)
            return respuesta

        monkeypatch.setattr("builtins.input", responder)
        return pendientes

    return preparar


@pytest.fixture
def falla_guardado(monkeypatch):
    """Hace que falle el reemplazo numero n de un archivo al guardar."""

    def preparar(numero=1):
        original = archivos.os.replace
        llamadas = []

        def reemplazar(origen, destino):
            llamadas.append(destino)
            if len(llamadas) == numero:
                raise OSError("disco lleno")
            original(origen, destino)

        monkeypatch.setattr(archivos.os, "replace", reemplazar)

    return preparar
