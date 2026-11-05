"""Tests de punta a punta: login, menus y programa completo."""

import os
from pathlib import Path

import pytest

import main as programa
from funciones.datos import archivos
from funciones.sesion import iniciar_sesion
from tests.conftest import CUENTAS

MENU_LOGIN = "1"
SALIR = "2"
ADMIN_LOGIN = (MENU_LOGIN, "admin", "admin123")
PC01_LOGIN = (MENU_LOGIN, "PC01", "1234")
ADMIN_CERRAR = "14"
PC_CERRAR = "3"


def test_login_correcto(teclado):
    teclado("pc01", "1234")
    assert iniciar_sesion(CUENTAS)["usuario"] == "PC01"


def test_login_se_agota_a_los_tres_intentos(teclado, capsys):
    teclado("PC01", "mala", "", "", "nadie", "1234")
    assert iniciar_sesion(CUENTAS) is None
    salida = capsys.readouterr().out
    assert "Intentos restantes: 2" in salida
    assert "Intentos restantes: 1" in salida
    assert "Demasiados intentos" in salida


def test_login_con_cuenta_bloqueada(teclado, capsys):
    cuentas = [dict(CUENTAS[1], activa=False)]
    teclado("PC01", "1234", "PC01", "1234", "PC01", "1234")
    assert iniciar_sesion(cuentas) is None
    assert capsys.readouterr().out.count("bloqueada") == 3


def test_clave_incorrecta_no_revela_que_la_cuenta_esta_bloqueada(teclado, capsys):
    cuentas = [dict(CUENTAS[1], activa=False)]
    teclado("PC01", "mala", "PC01", "mala", "PC01", "mala")
    assert iniciar_sesion(cuentas) is None
    assert "bloqueada" not in capsys.readouterr().out


def test_menu_de_admin_tiene_todas_las_opciones_numeradas(teclado, capsys):
    teclado(*ADMIN_LOGIN, ADMIN_CERRAR, SALIR)
    programa.main()
    salida = capsys.readouterr().out
    assert "Bienvenido admin" in salida
    for texto in [
        "Listado de juegos",
        "Eliminar juego",
        "Juegos sin instalar",
        "Bloquear/desbloquear PC-Usuario",
        "Quitar permiso de administrador",
    ]:
        assert texto in salida
    assert "Sesión Cerrada" in salida
    assert "Hasta luego" in salida


def test_menu_de_pc_no_tiene_opciones_de_administrador(teclado, capsys):
    teclado(*PC01_LOGIN, PC_CERRAR, SALIR)
    programa.main()
    salida = capsys.readouterr().out
    assert "Listado de juegos instalados" in salida
    assert "Agregar juego" not in salida
    assert "Otorgar permiso" not in salida


def test_pc_no_puede_usar_numeros_del_menu_de_admin(teclado, datos, capsys):
    antes = datos.foto()
    teclado(*PC01_LOGIN, "4", "13", PC_CERRAR, SALIR)
    programa.main()
    assert capsys.readouterr().out.count("Opcion invalida") == 2
    assert datos.foto() == antes


def test_recorrido_completo_de_una_pc_bloqueada_y_desbloqueada(teclado, capsys):
    teclado(
        *ADMIN_LOGIN,
        "11", "PC01", "s",
        ADMIN_CERRAR,
        *PC01_LOGIN, "PC01", "1234", "PC01", "1234",
        *ADMIN_LOGIN,
        "11", "PC01", "s",
        ADMIN_CERRAR,
        *PC01_LOGIN,
        PC_CERRAR,
        SALIR,
    )
    programa.main()
    salida = capsys.readouterr().out
    assert "Esta cuenta está bloqueada" in salida
    assert "Bienvenido PC01" in salida


def test_recorrido_de_admin_otorgado_y_revertido(teclado, capsys, datos):
    teclado(
        *ADMIN_LOGIN,
        "12", "PC01", "s",
        ADMIN_CERRAR,
        *PC01_LOGIN,
        "13",
        ADMIN_CERRAR,
        *ADMIN_LOGIN,
        "13", "PC01", "s",
        ADMIN_CERRAR,
        *PC01_LOGIN,
        PC_CERRAR,
        SALIR,
    )
    programa.main()
    assert datos.leer("cuentas.json")[1]["rol"] == "pc"
    assert "No hay administradores" in capsys.readouterr().out


def test_juego_agregado_queda_disponible_en_la_misma_sesion(teclado, capsys):
    teclado(
        *ADMIN_LOGIN,
        "3", "Nuevo", "Puzzle", "Coming soon", "1 GB", "s",
        "2", "nuevo",
        ADMIN_CERRAR,
        SALIR,
    )
    programa.main()
    assert capsys.readouterr().out.count("Coming soon") >= 2


def test_juego_eliminado_deja_de_estar_en_la_misma_sesion(teclado, capsys):
    teclado(*ADMIN_LOGIN, "4", "Tetris", "s", "2", "tetris", ADMIN_CERRAR, SALIR)
    programa.main()
    assert "No se encontraron juegos para tetris" in capsys.readouterr().out


def test_error_de_datos_en_una_accion_no_corta_el_programa(teclado, datos, capsys):
    teclado(*ADMIN_LOGIN, "1", ADMIN_CERRAR, SALIR)
    datos.escribir("instalaciones.json", "{mal")
    programa.main()
    salida = capsys.readouterr().out
    assert "Error: instalaciones.json tiene un formato inválido" in salida
    assert "Hasta luego" in salida


def test_guardado_fallido_avisa_y_sigue_en_el_menu(teclado, datos, falla_guardado, capsys):
    antes = datos.foto()
    falla_guardado()
    teclado(*ADMIN_LOGIN, "10", "PC01", "s", ADMIN_CERRAR, SALIR)
    programa.main()
    salida = capsys.readouterr().out
    assert "Error: No se pudieron guardar los datos, no hubo cambios" in salida
    assert "Hasta luego" in salida
    assert datos.foto() == antes


def test_cuentas_invalidas_avisan_al_hacer_login(teclado, datos, capsys):
    datos.escribir("cuentas.json", [{"usuario": 123, "clave": "x", "rol": "pc"}])
    teclado(MENU_LOGIN, SALIR)
    programa.main()
    assert "Error al cargar las cuentas" in capsys.readouterr().out


def test_biblioteca_invalida_avisa_y_termina(teclado, datos, capsys):
    datos.escribir("juegos.json", "{mal")
    teclado()
    programa.main()
    assert "Error al cargar la biblioteca de juegos" in capsys.readouterr().out


@pytest.mark.parametrize("corte", [KeyboardInterrupt(), EOFError()])
def test_ctrl_c_y_ctrl_d_terminan_sin_error(teclado, capsys, corte):
    teclado(*ADMIN_LOGIN, "3", "Nuevo", corte)
    programa.main()
    assert "Hasta luego" in capsys.readouterr().out


def test_ctrl_c_a_mitad_de_una_accion_no_guarda_nada(teclado, datos):
    antes = datos.foto()
    teclado(*ADMIN_LOGIN, "4", "SOMA", KeyboardInterrupt())
    programa.main()
    assert datos.foto() == antes


def test_la_carpeta_de_datos_no_depende_de_donde_se_ejecuta(monkeypatch, tmp_path):
    """La ruta se calcula desde el codigo, asi funciona desde cualquier carpeta."""
    monkeypatch.undo()
    monkeypatch.chdir(tmp_path)
    raiz = Path(__file__).resolve().parents[1]
    assert archivos.CARPETA_DATOS == raiz / "data"
    assert os.path.isabs(archivos.CARPETA_DATOS)
