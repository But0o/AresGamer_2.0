"""Cuentas del sistema: carga, guardado, busquedas y reglas de permisos."""

import json

from funciones.datos.archivos import (
    ErrorDeDatos,
    guardar_archivos,
    leer_lista,
    validar_registros,
)

ARCHIVO_CUENTAS = "cuentas.json"
CAMPOS_CUENTA = ["usuario", "clave", "rol"]
ROL_ADMIN = "admin"
ROL_PC = "pc"
ADMIN_ORIGINAL = "admin"


def cargar_cuentas() -> list[dict]:
    """
    Contrato: Carga las cuentas y valida la estructura de cada una
    Precondiciones: -
    Postcondiciones: Devuelve la lista de cuentas. Lanza ErrorDeDatos si el archivo falta, es incorrecto, hay un rol invalido o el campo opcional activa no es true o false
    """
    cuentas = leer_lista(ARCHIVO_CUENTAS)
    validar_registros(cuentas, ARCHIVO_CUENTAS, CAMPOS_CUENTA)

    for cuenta in cuentas:
        if cuenta["rol"] not in [ROL_ADMIN, ROL_PC]:
            raise ErrorDeDatos(f"{ARCHIVO_CUENTAS}: rol inválido")
        if not isinstance(cuenta.get("activa", True), bool):
            raise ErrorDeDatos(f"{ARCHIVO_CUENTAS}: el campo activa debe ser true o false")

    return cuentas


def texto_cuentas(cuentas: list[dict]) -> str:
    """
    Contrato: Arma el texto del archivo de cuentas
    Precondiciones: cuentas es una lista de diccionarios con los campos de CAMPOS_CUENTA
    Postcondiciones: Devuelve el texto en formato JSON, listo para guardar
    """
    return json.dumps(cuentas, indent=2, ensure_ascii=False) + "\n"


def guardar_cuentas(cuentas: list[dict]) -> None:
    """
    Contrato: Guarda todas las cuentas en data/cuentas.json
    Precondiciones: cuentas es una lista de diccionarios con los campos de CAMPOS_CUENTA
    Postcondiciones: El archivo queda con el contenido de cuentas. Lanza ErrorDeDatos si no se pudo guardar
    """
    guardar_archivos({ARCHIVO_CUENTAS: texto_cuentas(cuentas)})


def buscar_cuenta(cuentas: list[dict], usuario: str) -> dict | None:
    """
    Contrato: Busca una cuenta por su nombre de usuario, sin distinguir mayusculas
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Devuelve el diccionario de la cuenta (no una copia) o None si no existe
    """
    for cuenta in cuentas:
        if cuenta["usuario"].lower() == usuario.lower():
            return cuenta

    return None


def verificar_credenciales(cuentas: list[dict], usuario: str, clave: str) -> dict | None:
    """
    Contrato: Busca la cuenta que coincide con el usuario y la clave. El usuario no distingue mayusculas, la clave si
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Devuelve la cuenta si las credenciales son correctas, None si no
    """
    cuenta = buscar_cuenta(cuentas, usuario)

    if cuenta is not None and cuenta["clave"] == clave:
        return cuenta

    return None


def cuenta_activa(cuenta: dict) -> bool:
    """
    Contrato: Indica si una cuenta puede iniciar sesion
    Precondiciones: cuenta es un diccionario devuelto por cargar_cuentas
    Postcondiciones: Devuelve False si esta bloqueada. Una cuenta sin el campo activa se considera activa
    """
    return cuenta.get("activa", True)


def nombres_de_pcs(cuentas: list[dict]) -> list[str]:
    """
    Contrato: Devuelve los nombres de las cuentas con rol "pc"
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Devuelve una lista nueva con los nombres, en el orden del archivo
    """
    pcs = []

    for cuenta in cuentas:
        if cuenta["rol"] == ROL_PC:
            pcs.append(cuenta["usuario"])

    return pcs


def quitar_cuenta(cuentas: list[dict], usuario: str) -> list[dict]:
    """
    Contrato: Devuelve las cuentas sin la que corresponde a un usuario
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Devuelve una lista nueva. No modifica la recibida
    """
    restantes = []

    for cuenta in cuentas:
        if cuenta["usuario"] != usuario:
            restantes.append(cuenta)

    return restantes


def admins_que_se_pueden_quitar(cuentas: list[dict], usuario_actual: str) -> list[str]:
    """
    Contrato: Devuelve los administradores a los que el admin logueado les puede quitar el permiso
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas. usuario_actual es el nombre del admin logueado
    Postcondiciones: Devuelve una lista nueva sin el admin logueado (asi siempre queda al menos un administrador) y sin la cuenta ADMIN_ORIGINAL
    """
    admins = []

    for cuenta in cuentas:
        if (
            cuenta["rol"] == ROL_ADMIN
            and cuenta["usuario"] != usuario_actual
            and cuenta["usuario"].lower() != ADMIN_ORIGINAL
        ):
            admins.append(cuenta["usuario"])

    return admins
