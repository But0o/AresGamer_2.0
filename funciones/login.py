"""Login: carga de cuentas e inicio de sesion"""

import json

MAX_INTENTOS = 3
CAMPOS_CUENTA = ["usuario", "clave", "rol"]
ROLES_VALIDOS = ["admin", "pc"]


def cargar_cuentas() -> list[dict]:
    """
    Contrato: Carga las cuentas desde data/cuentas.json y valida la estructura de cada una
    Precondiciones: Existe data/cuentas.json con una lista de diccionarios. Cada cuenta tiene los campos usuario, clave y rol. El rol es "admin" o "pc"
    Postcondiciones: Devuelve la lista de cuentas. Lanza FileNotFoundError si falta el archivo. Lanza ValueError si el json es inválido o alguna cuenta es incorrecta
    """
    try:
        with open("data/cuentas.json", "rt", encoding="utf-8-sig") as archivo:
            cuentas = json.load(archivo)
    except FileNotFoundError:
        raise FileNotFoundError("No se encontro el archivo data/cuentas.json")
    except json.JSONDecodeError:
        raise ValueError("cuentas.json tiene un formato invalido")

    if not isinstance(cuentas, list):
        raise ValueError("cuentas.json debe contener una lista de cuentas")

    for cuenta in cuentas:
        if not isinstance(cuenta, dict):
            raise ValueError(
                "cuentas.json: hay un elemento que no es una cuenta valida"
            )
        for campo in CAMPOS_CUENTA:
            if campo not in cuenta:
                raise ValueError(
                    "cuentas.json: una cuenta le falta el campo '" + campo + "'"
                )
        if cuenta["rol"] not in ROLES_VALIDOS:
            raise ValueError("cuentas.json: rol inválido")
    return cuentas


def buscar_cuenta(cuentas: list[dict], usuario: str, clave: str) -> dict | None:
    """
    Contrato: Busca la cuenta que coincide con el usuario y la clave
    Precondiciones: cuentas es una lista de diccionarios con los campos usuario, clave y rol. usuario y clave son strings
    Postcondiciones: Devuelve el diccionario de la cuenta si hay coincidencia. Devuelve Nobe si no exite ninguna cuenta con esas credenciales. No modifica la lista recibida
    """

    i = 0

    while i < len(cuentas):
        if (
            cuentas[i]["usuario"].lower() == usuario.lower()
            and cuentas[i]["clave"] == clave
        ):
            return cuentas[i]
        i += 1
    return None


def iniciar_sesion(cuentas: list[dict]) -> dict | None:
    """
    Contrato: Pide usuario y clave por consola hasta un maximo de MAX_INTENTOS intentos
    Precondiciones: cuentas es una lista de diccionarios con los campos usuario, clave y rol
    Postcondiciones: Devuelve la cuenta si las credenciales son correctas. Devuelve None si se agotan los intentos. Imprime mensaje de error o intentos restantes
    """
    intentos = 0
    while intentos < MAX_INTENTOS:
        usuario = input("\nUsuario: ").strip()
        clave = input("Clave: ").strip()

        if usuario == "" or clave == "":
            print("Hay que completar los campos usuario y clave")
        else:
            cuenta = buscar_cuenta(cuentas, usuario, clave)
            if cuenta != None:
                return cuenta
            print("Usuario o clave incorrectos")
        intentos += 1
        if intentos < MAX_INTENTOS:
            print("Intentos restantes:", MAX_INTENTOS - intentos)
    return None


def guardar_cuentas(cuentas: list[dict]) -> None:
    """
    Contrato: Guarda todas las cuentas en data/cuentas.json
    Precondiciones: cuentas es una lista de diccionarios con los campos usuario, clave y rol
    Postcondiciones: El archivo queda con el contenido de cuentas, con el mismo formato que ya tiene. Lanza OSError (o una subclase) si no se pudo escribir
    """
    contenido = json.dumps(cuentas, indent=2, ensure_ascii=False)

    try:
        with open("data/cuentas.json", "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
    except FileNotFoundError:
        raise FileNotFoundError("No se encontro la carpeta data/.")
    except PermissionError:
        raise PermissionError("No hay permiso para escribir data/cuentas.json")
    except OSError as error:
        raise OSError(f"No se pudo guardar data/cuentas.json ({error})")


def usuario_en_uso(cuentas: list[dict], usuario: str) -> bool:
    """
    Contrato: Indica si ya existe una cuenta con ese nombre de usuario, sin distinguir mayusculas (igual que el login)
    Precondiciones: cuentas es una lista de diccionarios con el campo usuario. usuario es un string
    Postcondiciones: Devuelve True si ya hay una cuenta con ese usuario, False si no
    """
    for cuenta in cuentas:
        if cuenta["usuario"].lower() == usuario.lower():
            return True
    return False
