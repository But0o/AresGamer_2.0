"""Tests de las reglas de juegos, instalaciones y cuentas, y de los datos reales del proyecto."""

import json
from pathlib import Path

import pytest

from funciones.datos import archivos
from funciones.datos.archivos import ErrorDeDatos
from funciones.datos.cuentas import (
    admins_que_se_pueden_quitar,
    buscar_cuenta,
    cargar_cuentas,
    cuenta_activa,
    nombres_de_pcs,
    quitar_cuenta,
    texto_cuentas,
    verificar_credenciales,
)
from funciones.datos.instalaciones import (
    cargar_instalaciones,
    desinstalar_juego,
    instalar_juego,
    juegos_instalados_en,
    pcs_de_juego,
    quitar_instalaciones_de_juego,
    quitar_instalaciones_de_pc,
    texto_instalaciones,
)
from funciones.datos.juegos import (
    buscar_juego,
    buscar_juegos,
    cargar_juegos,
    fecha_valida,
    juegos_de_pc,
    juegos_sin_instalar,
    normalizar_peso,
    texto_juegos,
)
from tests.conftest import CUENTAS, INSTALACIONES, JUEGOS

CARPETA_REAL = Path(__file__).resolve().parents[1] / "data"


def test_buscar_juego_no_distingue_mayusculas():
    assert buscar_juego(JUEGOS, "sOmA")["nombre"] == "SOMA"
    assert buscar_juego(JUEGOS, "SOM") is None


@pytest.mark.parametrize(
    "texto, esperados",
    [
        ("por", ["Portal"]),
        ("INDIE", ["SOMA", "Tetris"]),
        ("puzzle", ["Portal", "Tetris"]),
        ("zzz", []),
    ],
)
def test_buscar_juegos_por_nombre_o_categoria(texto, esperados):
    assert [juego["nombre"] for juego in buscar_juegos(JUEGOS, texto)] == esperados


def test_juegos_de_pc_ignora_instalaciones_de_juegos_que_no_existen():
    instalaciones = INSTALACIONES + [{"juego": "Borrado", "pc": "PC01"}]
    nombres = [juego["nombre"] for juego in juegos_de_pc(JUEGOS, instalaciones, "PC01")]
    assert nombres == ["SOMA", "Portal"]


def test_juegos_sin_instalar():
    assert [juego["nombre"] for juego in juegos_sin_instalar(JUEGOS, INSTALACIONES)] == ["Tetris"]


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("10 mb", "10 MB"),
        ("  2   Gb ", "2 GB"),
        ("1.5 GB", "1.5 GB"),
        ("0 GB", None),
        ("0.0 GB", None),
        ("-1 GB", None),
        ("10", None),
        ("10MB", None),
        ("10 TB", None),
        ("nan GB", None),
        ("1e3 GB", None),
        (".5 GB", None),
        ("", None),
        ("1 2 GB", None),
    ],
)
def test_normalizar_peso(texto, esperado):
    assert normalizar_peso(texto) == esperado


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("Jun 6, 2016", True),
        ("Feb 29, 2016", True),
        ("Coming soon", True),
        ("Feb 29, 2015", False),
        ("Jun 31, 2016", False),
        ("Foo 6, 2016", False),
        ("jun 6, 2016", False),
        ("Jun 6 2016", False),
        ("06/06/2016", False),
        ("Jun 6, 0000", False),
        ("", False),
    ],
)
def test_fecha_valida(texto, esperado):
    assert fecha_valida(texto) is esperado


def test_pcs_y_juegos_instalados():
    assert pcs_de_juego("SOMA", INSTALACIONES) == ["PC01", "PC02"]
    assert pcs_de_juego("Tetris", INSTALACIONES) == []
    assert juegos_instalados_en(INSTALACIONES, "PC01") == ["SOMA", "Portal"]
    assert juegos_instalados_en(INSTALACIONES, "PC03") == []


def test_instalar_juego_no_permite_duplicados():
    instalaciones = [dict(i) for i in INSTALACIONES]
    assert instalar_juego(instalaciones, "SOMA", "PC01") is False
    assert len(instalaciones) == 3
    assert instalar_juego(instalaciones, "SOMA", "PC03") is True
    assert instalaciones[-1] == {"juego": "SOMA", "pc": "PC03"}


def test_desinstalar_juego():
    instalaciones = [dict(i) for i in INSTALACIONES]
    assert desinstalar_juego(instalaciones, "Tetris", "PC01") is False
    assert len(instalaciones) == 3
    assert desinstalar_juego(instalaciones, "SOMA", "PC01") is True
    assert instalaciones == [{"juego": "Portal", "pc": "PC01"}, {"juego": "SOMA", "pc": "PC02"}]


def test_quitar_instalaciones_devuelve_lista_nueva():
    assert quitar_instalaciones_de_juego(INSTALACIONES, "SOMA") == [{"juego": "Portal", "pc": "PC01"}]
    assert quitar_instalaciones_de_pc(INSTALACIONES, "PC01") == [{"juego": "SOMA", "pc": "PC02"}]
    assert len(INSTALACIONES) == 3


def test_texto_instalaciones_separa_las_pcs_y_es_json_valido():
    texto = texto_instalaciones(INSTALACIONES)
    assert texto == (
        "[\n"
        '  { "juego": "SOMA", "pc": "PC01" },\n'
        '  { "juego": "Portal", "pc": "PC01" },\n'
        "\n"
        '  { "juego": "SOMA", "pc": "PC02" }\n'
        "]"
    )
    assert json.loads(texto) == INSTALACIONES


def test_texto_instalaciones_vacio():
    assert texto_instalaciones([]) == "[]"


def test_buscar_cuenta_y_credenciales():
    assert buscar_cuenta(CUENTAS, "pc01")["usuario"] == "PC01"
    assert buscar_cuenta(CUENTAS, "PC99") is None
    assert verificar_credenciales(CUENTAS, "pc01", "1234")["usuario"] == "PC01"
    assert verificar_credenciales(CUENTAS, "PC01", "mala") is None
    assert verificar_credenciales(CUENTAS, "ADMIN", "ADMIN123") is None
    assert verificar_credenciales(CUENTAS, "nadie", "1234") is None


def test_cuenta_activa():
    assert cuenta_activa({}) is True
    assert cuenta_activa({"activa": True}) is True
    assert cuenta_activa({"activa": False}) is False


def test_nombres_de_pcs_y_quitar_cuenta():
    assert nombres_de_pcs(CUENTAS) == ["PC01", "PC02", "PC03"]
    assert [c["usuario"] for c in quitar_cuenta(CUENTAS, "PC02")] == ["admin", "PC01", "PC03"]
    assert len(CUENTAS) == 4


def test_admins_que_se_pueden_quitar_excluye_al_actual_y_al_original():
    cuentas = [
        {"usuario": "admin", "clave": "x", "rol": "admin"},
        {"usuario": "PC01", "clave": "x", "rol": "admin"},
        {"usuario": "PC02", "clave": "x", "rol": "admin"},
        {"usuario": "PC03", "clave": "x", "rol": "pc"},
    ]
    assert admins_que_se_pueden_quitar(cuentas, "admin") == ["PC01", "PC02"]
    assert admins_que_se_pueden_quitar(cuentas, "PC01") == ["PC02"]


@pytest.mark.parametrize(
    "cargar, archivo, contenido, mensaje",
    [
        (cargar_juegos, "juegos.json", [{"nombre": "x"}], "le falta el campo"),
        (cargar_juegos, "juegos.json", [dict(JUEGOS[0], nombre=5)], "debe ser un texto"),
        (cargar_instalaciones, "instalaciones.json", [{"juego": "x"}], "le falta el campo"),
        (cargar_cuentas, "cuentas.json", [{"usuario": "x", "clave": "y"}], "le falta el campo"),
        (cargar_cuentas, "cuentas.json", [{"usuario": 123, "clave": "y", "rol": "pc"}], "debe ser un texto"),
        (cargar_cuentas, "cuentas.json", [{"usuario": "x", "clave": "y", "rol": "otro"}], "rol inválido"),
        (cargar_cuentas, "cuentas.json", [{"usuario": "x", "clave": "y", "rol": "pc", "activa": "false"}], "true o false"),
    ],
)
def test_cargar_rechaza_datos_incorrectos(datos, cargar, archivo, contenido, mensaje):
    datos.escribir(archivo, contenido)
    with pytest.raises(ErrorDeDatos, match=mensaje):
        cargar()


@pytest.fixture
def carpeta_real(monkeypatch):
    """Solo para leer los datos reales. Estos tests no guardan nada."""
    monkeypatch.setattr(archivos, "CARPETA_DATOS", CARPETA_REAL)


def test_los_datos_reales_son_validos_y_coherentes(carpeta_real):
    juegos = cargar_juegos()
    cuentas = cargar_cuentas()
    instalaciones = cargar_instalaciones()
    pcs = nombres_de_pcs(cuentas)

    for juego in juegos:
        assert normalizar_peso(juego["peso"]) == juego["peso"]
        assert fecha_valida(juego["fecha_lanzamiento"]), juego["fecha_lanzamiento"]

    for instalacion in instalaciones:
        assert buscar_juego(juegos, instalacion["juego"]) is not None
        assert instalacion["pc"] in pcs

    nombres = [juego["nombre"].lower() for juego in juegos]
    usuarios = [cuenta["usuario"].lower() for cuenta in cuentas]
    assert len(nombres) == len(set(nombres))
    assert len(usuarios) == len(set(usuarios))


def test_guardar_los_datos_reales_no_cambiaria_su_formato(carpeta_real):
    """Evita que el primer guardado cambie todo el archivo en el diff de git."""
    pares = [
        ("juegos.json", texto_juegos(cargar_juegos())),
        ("cuentas.json", texto_cuentas(cargar_cuentas())),
        ("instalaciones.json", texto_instalaciones(cargar_instalaciones())),
    ]

    for nombre, texto in pares:
        original = (CARPETA_REAL / nombre).read_text(encoding="utf-8")
        assert texto.replace("\r\n", "\n") == original.replace("\r\n", "\n"), nombre
