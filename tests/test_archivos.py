"""Tests de la lectura y el guardado de archivos."""

import pytest

from funciones.datos import archivos
from funciones.datos.archivos import (
    ErrorDeDatos,
    guardar_archivos,
    leer_lista,
    validar_registros,
)


def test_leer_lista_devuelve_el_contenido(datos):
    datos.escribir("x.json", [1, 2])
    assert leer_lista("x.json") == [1, 2]


def test_leer_lista_acepta_archivos_con_bom(datos):
    (datos.carpeta / "x.json").write_bytes(b"\xef\xbb\xbf[1]")
    assert leer_lista("x.json") == [1]


@pytest.mark.parametrize(
    "contenido, mensaje",
    [("{mal", "formato inválido"), ('{"a": 1}', "debe contener una lista")],
)
def test_leer_lista_rechaza_contenido_incorrecto(datos, contenido, mensaje):
    datos.escribir("x.json", contenido)
    with pytest.raises(ErrorDeDatos, match=mensaje):
        leer_lista("x.json")


def test_leer_lista_rechaza_archivo_que_no_es_utf8(datos):
    (datos.carpeta / "x.json").write_bytes(b'["\xff"]')
    with pytest.raises(ErrorDeDatos, match="formato inválido"):
        leer_lista("x.json")


def test_leer_lista_avisa_si_falta_el_archivo():
    with pytest.raises(ErrorDeDatos, match="No se encontró"):
        leer_lista("no_existe.json")


def test_leer_lista_no_revienta_con_otros_errores_del_sistema(datos):
    (datos.carpeta / "carpeta.json").mkdir()
    with pytest.raises(ErrorDeDatos, match="No se pudo leer"):
        leer_lista("carpeta.json")


@pytest.mark.parametrize(
    "registros, mensaje",
    [
        ([1], "no es válido"),
        ([{"a": "x"}], "le falta el campo b"),
        ([{"a": "x", "b": 5}], "campo b debe ser un texto"),
    ],
)
def test_validar_registros_rechaza_errores(registros, mensaje):
    with pytest.raises(ErrorDeDatos, match=mensaje):
        validar_registros(registros, "x.json", ["a", "b"])


def test_guardar_archivos_escribe_todo_y_no_deja_temporales(datos):
    guardar_archivos({"a.json": "uno", "b.json": "dos"})
    assert (datos.carpeta / "a.json").read_text(encoding="utf-8") == "uno"
    assert (datos.carpeta / "b.json").read_text(encoding="utf-8") == "dos"
    assert list(datos.carpeta.glob("*.tmp")) == []


def test_guardar_archivos_conserva_acentos(datos):
    guardar_archivos({"a.json": "acción ™"})
    assert (datos.carpeta / "a.json").read_text(encoding="utf-8") == "acción ™"


@pytest.mark.parametrize("numero", [1, 2])
def test_guardado_fallido_deja_todo_como_estaba(datos, falla_guardado, numero):
    antes = datos.foto()
    falla_guardado(numero)

    with pytest.raises(ErrorDeDatos, match="no hubo cambios"):
        guardar_archivos({"juegos.json": "nuevo", "cuentas.json": "nuevo"})

    assert datos.foto() == antes


def test_guardado_fallido_borra_un_archivo_que_antes_no_existia(datos, falla_guardado):
    antes = datos.foto()
    falla_guardado(2)

    with pytest.raises(ErrorDeDatos):
        guardar_archivos({"nuevo.json": "x", "cuentas.json": "y"})

    assert datos.foto() == antes


def test_falla_al_escribir_temporal_no_toca_los_originales(datos, monkeypatch):
    antes = datos.foto()

    def falla(nombre, contenido):
        raise PermissionError("sin permiso")

    monkeypatch.setattr(archivos, "_escribir_temporal", falla)

    with pytest.raises(ErrorDeDatos):
        guardar_archivos({"juegos.json": "nuevo"})

    assert datos.foto() == antes
