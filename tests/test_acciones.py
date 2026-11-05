"""Tests de cada accion de los menus, con los archivos de datos temporales."""

import copy

import pytest

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
from funciones.datos.archivos import ErrorDeDatos
from tests.conftest import CUENTAS, JUEGOS

ADMIN = {"usuario": "admin", "rol": "admin"}
PC01 = {"usuario": "PC01", "rol": "pc"}


def rol_de(datos, usuario):
    for cuenta in datos.leer("cuentas.json"):
        if cuenta["usuario"] == usuario:
            return cuenta["rol"]
    return None


def hacer_admin(datos, usuario):
    cuentas = copy.deepcopy(CUENTAS)
    for cuenta in cuentas:
        if cuenta["usuario"] == usuario:
            cuenta["rol"] = "admin"
    datos.escribir("cuentas.json", cuentas)


@pytest.fixture
def juegos():
    return copy.deepcopy(JUEGOS)


# ---------- Biblioteca ----------


def test_listar_juegos_segun_rol(juegos, capsys):
    listar_juegos(juegos, PC01)
    assert "Tetris" not in capsys.readouterr().out
    listar_juegos(juegos, ADMIN)
    assert "Tetris" in capsys.readouterr().out


def test_buscar_vacio_no_busca(juegos, teclado, capsys):
    teclado("   ")
    buscar_en_biblioteca(juegos, ADMIN)
    assert "Hay que escribir algo" in capsys.readouterr().out


def test_admin_busca_en_toda_la_biblioteca(juegos, teclado, capsys):
    teclado("TETRIS")
    buscar_en_biblioteca(juegos, ADMIN)
    assert "10 MB" in capsys.readouterr().out


def test_pc_no_encuentra_juegos_que_no_tiene(juegos, teclado, capsys):
    teclado("Tetris")
    buscar_en_biblioteca(juegos, PC01)
    assert "No se encontraron juegos para Tetris" in capsys.readouterr().out


def test_pc_encuentra_sus_juegos(juegos, teclado, capsys):
    teclado("indie")
    buscar_en_biblioteca(juegos, PC01)
    salida = capsys.readouterr().out
    assert "SOMA" in salida
    assert "Tetris" not in salida


def test_agregar_juego_guarda_y_valida(juegos, teclado, datos, capsys):
    teclado("soma", " Nuevo ", "", "Puzzle", "ayer", "Feb 30, 2020", "Mar 1, 2020", "10", "1.5 gb", "s")
    agregar_juego(juegos)
    nuevo = {"nombre": "Nuevo", "categoria": "Puzzle", "fecha_lanzamiento": "Mar 1, 2020", "peso": "1.5 GB"}
    assert juegos[-1] == nuevo
    assert datos.leer("juegos.json")[-1] == nuevo
    salida = capsys.readouterr().out
    assert "Ya existe un juego llamado 'soma'" in salida
    assert salida.count("Fecha inválida") == 2
    assert "Formato inválido" in salida


@pytest.mark.parametrize("respuestas", [("",), ("Nuevo", "Puzzle", "Coming soon", "1 GB", "n")])
def test_cancelar_agregar_juego_no_cambia_nada(juegos, teclado, datos, respuestas):
    antes = datos.foto()
    teclado(*respuestas)
    agregar_juego(juegos)
    assert juegos == JUEGOS
    assert datos.foto() == antes


def test_agregar_juego_con_guardado_fallido_no_cambia_nada(juegos, teclado, datos, falla_guardado):
    antes = datos.foto()
    falla_guardado()
    teclado("Nuevo", "Puzzle", "Coming soon", "1 GB", "s")
    with pytest.raises(ErrorDeDatos):
        agregar_juego(juegos)
    assert juegos == JUEGOS
    assert datos.foto() == antes


def test_eliminar_juego_lo_quita_de_la_biblioteca_y_de_las_pcs(juegos, teclado, datos, capsys):
    teclado("soma", "s")
    eliminar_juego(juegos)
    assert [juego["nombre"] for juego in juegos] == ["Portal", "Tetris"]
    assert [juego["nombre"] for juego in datos.leer("juegos.json")] == ["Portal", "Tetris"]
    assert datos.leer("instalaciones.json") == [{"juego": "Portal", "pc": "PC01"}]
    assert "PC01, PC02" in capsys.readouterr().out


@pytest.mark.parametrize("respuestas", [("",), ("no existe",), ("SOMA", "n")])
def test_cancelar_eliminar_juego_no_cambia_nada(juegos, teclado, datos, respuestas):
    antes = datos.foto()
    teclado(*respuestas)
    eliminar_juego(juegos)
    assert juegos == JUEGOS
    assert datos.foto() == antes


@pytest.mark.parametrize("numero", [1, 2])
def test_eliminar_juego_no_queda_a_medias_si_falla_el_guardado(juegos, teclado, datos, falla_guardado, numero):
    antes = datos.foto()
    falla_guardado(numero)
    teclado("SOMA", "s")
    with pytest.raises(ErrorDeDatos):
        eliminar_juego(juegos)
    assert juegos == JUEGOS
    assert datos.foto() == antes


def test_listar_sin_instalar(juegos, capsys):
    listar_sin_instalar(juegos, ADMIN)
    salida = capsys.readouterr().out
    assert "(1)" in salida and "Tetris" in salida
    assert "Portal" not in salida


def test_listar_sin_instalar_cuando_estan_todos(juegos, capsys):
    listar_sin_instalar(juegos[:2], ADMIN)
    assert "Todos los juegos están instalados" in capsys.readouterr().out


# ---------- Instalaciones ----------


def test_instalar_en_pc(juegos, teclado, datos):
    teclado("pc03", "no existe", "tetris", "s")
    instalar_en_pc(juegos)
    assert datos.leer("instalaciones.json")[-1] == {"juego": "Tetris", "pc": "PC03"}


def test_instalar_juego_repetido_no_cambia_nada(juegos, teclado, datos, capsys):
    antes = datos.foto()
    teclado("PC01", "SOMA")
    instalar_en_pc(juegos)
    assert "ya está instalado en PC01" in capsys.readouterr().out
    assert datos.foto() == antes


@pytest.mark.parametrize("respuestas", [("",), ("PC03", ""), ("PC03", "Tetris", "n")])
def test_cancelar_instalar_no_cambia_nada(juegos, teclado, datos, respuestas):
    antes = datos.foto()
    teclado(*respuestas)
    instalar_en_pc(juegos)
    assert datos.foto() == antes


def test_desinstalar_de_pc(teclado, datos, capsys):
    teclado("PC01", "tetris", "soma", "s")
    desinstalar_de_pc()
    assert {"juego": "SOMA", "pc": "PC01"} not in datos.leer("instalaciones.json")
    assert {"juego": "SOMA", "pc": "PC02"} in datos.leer("instalaciones.json")
    assert "'tetris' no está instalado en PC01" in capsys.readouterr().out


def test_desinstalar_de_pc_sin_juegos(teclado, capsys):
    teclado("PC03")
    desinstalar_de_pc()
    assert "PC03 no tiene juegos instalados" in capsys.readouterr().out


@pytest.mark.parametrize("respuestas", [("",), ("PC01", ""), ("PC01", "SOMA", "n")])
def test_cancelar_desinstalar_no_cambia_nada(teclado, datos, respuestas):
    antes = datos.foto()
    teclado(*respuestas)
    desinstalar_de_pc()
    assert datos.foto() == antes


def test_consultar_instalados(capsys):
    consultar_instalados()
    salida = capsys.readouterr().out
    assert "PC01" in salida and "PC03" in salida
    assert "admin" not in salida


def test_consultar_instalados_sin_pcs(datos, capsys):
    datos.escribir("cuentas.json", [CUENTAS[0]])
    consultar_instalados()
    assert "No hay PC-Usuarios" in capsys.readouterr().out


# ---------- PC-Usuarios ----------


def test_agregar_pc(teclado, datos, capsys):
    teclado("pc01", "ADMIN", " PC09 ", "", "clave", "s")
    agregar_pc()
    assert datos.leer("cuentas.json")[-1] == {"usuario": "PC09", "clave": "clave", "rol": "pc"}
    salida = capsys.readouterr().out
    assert "Ya existe una cuenta llamada 'pc01'" in salida
    assert "Ya existe una cuenta llamada 'ADMIN'" in salida


@pytest.mark.parametrize("respuestas", [("",), ("PC09", "clave", "n")])
def test_cancelar_agregar_pc_no_cambia_nada(teclado, datos, respuestas):
    antes = datos.foto()
    teclado(*respuestas)
    agregar_pc()
    assert datos.foto() == antes


def test_eliminar_pc_quita_la_cuenta_y_sus_instalaciones(teclado, datos):
    teclado("pc01", "s")
    eliminar_pc()
    assert rol_de(datos, "PC01") is None
    assert datos.leer("instalaciones.json") == [{"juego": "SOMA", "pc": "PC02"}]


def test_no_se_puede_eliminar_un_admin(teclado, datos, capsys):
    antes = datos.foto()
    teclado("admin", "")
    eliminar_pc()
    assert "No existe la PC 'admin'" in capsys.readouterr().out
    assert datos.foto() == antes


@pytest.mark.parametrize("numero", [1, 2])
def test_eliminar_pc_no_queda_a_medias_si_falla_el_guardado(teclado, datos, falla_guardado, numero):
    antes = datos.foto()
    falla_guardado(numero)
    teclado("PC01", "s")
    with pytest.raises(ErrorDeDatos):
        eliminar_pc()
    assert datos.foto() == antes


def test_bloquear_y_desbloquear_pc(teclado, datos, capsys):
    teclado("PC01", "s")
    bloquear_desbloquear_pc()
    assert datos.leer("cuentas.json")[1]["activa"] is False
    assert "bloqueada correctamente" in capsys.readouterr().out

    teclado("pc01", "s")
    bloquear_desbloquear_pc()
    assert datos.leer("cuentas.json")[1]["activa"] is True
    assert "desbloqueada correctamente" in capsys.readouterr().out


def test_no_se_puede_bloquear_un_admin(teclado, datos, capsys):
    antes = datos.foto()
    teclado("admin", "")
    bloquear_desbloquear_pc()
    assert "No existe la PC 'admin'" in capsys.readouterr().out
    assert datos.foto() == antes


def test_cancelar_bloqueo_no_cambia_nada(teclado, datos):
    antes = datos.foto()
    teclado("PC01", "n")
    bloquear_desbloquear_pc()
    assert datos.foto() == antes


# ---------- Permisos ----------


def test_otorgar_admin_quita_sus_instalaciones(teclado, datos):
    teclado("pc01", "s")
    otorgar_admin()
    assert rol_de(datos, "PC01") == "admin"
    assert datos.leer("instalaciones.json") == [{"juego": "SOMA", "pc": "PC02"}]


def test_no_se_puede_otorgar_admin_a_una_pc_bloqueada(teclado, datos, capsys):
    cuentas = copy.deepcopy(CUENTAS)
    cuentas[1]["activa"] = False
    datos.escribir("cuentas.json", cuentas)
    antes = datos.foto()
    teclado("PC01")
    otorgar_admin()
    assert "primero hay que desbloquearla" in capsys.readouterr().out
    assert datos.foto() == antes


@pytest.mark.parametrize("respuestas", [("",), ("PC01", "n")])
def test_cancelar_otorgar_admin_no_cambia_nada(teclado, datos, respuestas):
    antes = datos.foto()
    teclado(*respuestas)
    otorgar_admin()
    assert datos.foto() == antes


@pytest.mark.parametrize("numero", [1, 2])
def test_otorgar_admin_no_queda_a_medias_si_falla_el_guardado(teclado, datos, falla_guardado, numero):
    antes = datos.foto()
    falla_guardado(numero)
    teclado("PC01", "s")
    with pytest.raises(ErrorDeDatos):
        otorgar_admin()
    assert datos.foto() == antes


def test_quitar_admin(teclado, datos):
    hacer_admin(datos, "PC01")
    teclado("pc01", "s")
    quitar_admin(ADMIN)
    assert rol_de(datos, "PC01") == "pc"


def test_unico_admin_no_tiene_a_quien_quitarle_el_permiso(teclado, datos, capsys):
    antes = datos.foto()
    teclado()
    quitar_admin(ADMIN)
    assert "No hay administradores" in capsys.readouterr().out
    assert datos.foto() == antes


def test_el_admin_original_esta_protegido(teclado, datos, capsys):
    hacer_admin(datos, "PC01")
    antes = datos.foto()
    teclado()
    quitar_admin({"usuario": "PC01", "rol": "admin"})
    assert "No hay administradores" in capsys.readouterr().out
    assert datos.foto() == antes


def test_no_se_puede_elegir_al_original_ni_a_uno_mismo(teclado, datos, capsys):
    cuentas = copy.deepcopy(CUENTAS)
    cuentas[1]["rol"] = "admin"
    cuentas[2]["rol"] = "admin"
    datos.escribir("cuentas.json", cuentas)
    teclado("ADMIN", "PC01", "PC02", "s")
    quitar_admin({"usuario": "PC01", "rol": "admin"})
    salida = capsys.readouterr().out
    assert "'ADMIN' no es una opción válida" in salida
    assert "'PC01' no es una opción válida" in salida
    assert rol_de(datos, "admin") == "admin"
    assert rol_de(datos, "PC01") == "admin"
    assert rol_de(datos, "PC02") == "pc"


@pytest.mark.parametrize("respuestas", [("",), ("PC01", "n")])
def test_cancelar_quitar_admin_no_cambia_nada(teclado, datos, respuestas):
    hacer_admin(datos, "PC01")
    antes = datos.foto()
    teclado(*respuestas)
    quitar_admin(ADMIN)
    assert datos.foto() == antes
