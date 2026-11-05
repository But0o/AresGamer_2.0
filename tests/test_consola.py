"""Tests de los pedidos de datos, el menu y las tablas."""

from funciones.consola.entrada import (
    confirmar,
    elegir_de_lista,
    pedir_nombre_nuevo,
    pedir_pc,
    pedir_texto,
)
from funciones.consola.menu import mostrar_menu, pedir_opcion
from funciones.consola.tablas import (
    mostrar_estado_pcs,
    mostrar_instalaciones_por_pc,
    mostrar_juegos,
)
from tests.conftest import CUENTAS, INSTALACIONES, JUEGOS

ADMIN = {"usuario": "admin", "rol": "admin"}
PC01 = {"usuario": "PC01", "rol": "pc"}


def test_pedir_texto_repite_si_esta_vacio_y_limpia_espacios(teclado, capsys):
    teclado("", "   ", "  hola ")
    assert pedir_texto("> ") == "hola"
    assert capsys.readouterr().out.count("no puede quedar vacío") == 2


def test_pedir_nombre_nuevo_rechaza_repetidos(teclado, capsys):
    teclado("usado", " libre ")
    assert pedir_nombre_nuevo("> ", lambda nombre: nombre == "usado", "Repetido: {}") == "libre"
    assert "Repetido: usado" in capsys.readouterr().out


def test_pedir_nombre_nuevo_cancela_con_vacio(teclado):
    teclado("")
    assert pedir_nombre_nuevo("> ", lambda nombre: False, "{}") is None


def test_elegir_de_lista_devuelve_la_opcion_como_esta_escrita(teclado, capsys):
    teclado("nada", "pc01")
    assert elegir_de_lista("> ", ["PC01"], "No existe {}") == "PC01"
    assert "No existe nada" in capsys.readouterr().out


def test_elegir_de_lista_acepta_llaves_en_lo_que_escribe_el_usuario(teclado, capsys):
    teclado("{0}{x}", "")
    assert elegir_de_lista("> ", ["PC01"], "No existe {}") is None
    assert "No existe {0}{x}" in capsys.readouterr().out


def test_pedir_pc_sin_pcs_avisa_y_no_pregunta(teclado, capsys):
    teclado()
    assert pedir_pc([CUENTAS[0]]) is None
    assert "No hay PC-Usuarios" in capsys.readouterr().out


def test_pedir_pc_no_ofrece_administradores(teclado, capsys):
    teclado("admin", "PC02")
    assert pedir_pc(CUENTAS) == "PC02"
    salida = capsys.readouterr().out
    assert "PCs disponibles: PC01, PC02, PC03" in salida
    assert "No existe la PC 'admin'" in salida


def test_confirmar_acepta_variantes_y_repite_si_no_entiende(teclado):
    teclado("quizas", " SI ")
    assert confirmar("> ") is True
    teclado("s")
    assert confirmar("> ") is True
    teclado("N")
    assert confirmar("> ") is False
    teclado("no")
    assert confirmar("> ") is False


def test_menu_muestra_y_valida_opciones(teclado, capsys):
    opciones = {"1": "Uno", "2": "Dos"}
    mostrar_menu("Titulo", opciones)
    teclado("9", "", " 2 ")
    assert pedir_opcion(opciones) == "2"
    salida = capsys.readouterr().out
    assert "Titulo" in salida and "Uno" in salida
    assert salida.count("Opcion invalida") == 2


def test_admin_ve_todos_los_juegos_y_donde_estan(capsys):
    mostrar_juegos(JUEGOS, INSTALACIONES, ADMIN)
    salida = capsys.readouterr().out
    assert "Instalado en" in salida
    assert "PC01, PC02" in salida
    assert "Tetris" in salida


def test_pc_ve_solo_sus_juegos(capsys):
    mostrar_juegos(JUEGOS, INSTALACIONES, PC01)
    salida = capsys.readouterr().out
    assert "SOMA" in salida and "Portal" in salida
    assert "Tetris" not in salida
    assert "Instalado en" not in salida


def test_tabla_de_juegos_vacia_muestra_un_aviso(capsys):
    mostrar_juegos(JUEGOS, [], PC01)
    assert "No hay juegos para mostrar" in capsys.readouterr().out


def test_tabla_de_instalaciones_por_pc(capsys):
    mostrar_instalaciones_por_pc(["PC01", "PC03"], INSTALACIONES)
    salida = capsys.readouterr().out
    assert "SOMA" in salida and "Portal" in salida
    assert "| PC03 " in salida and "| -" in salida


def test_tabla_de_estado_de_pcs(capsys):
    mostrar_estado_pcs(
        [
            {"usuario": "admin", "clave": "x", "rol": "admin"},
            {"usuario": "PC01", "clave": "x", "rol": "pc"},
            {"usuario": "PC02", "clave": "x", "rol": "pc", "activa": False},
        ]
    )
    salida = capsys.readouterr().out
    assert "activa" in salida and "bloqueada" in salida
    assert "admin" not in salida
