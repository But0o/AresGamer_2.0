import json

CAMPOS_INSTALACION = ["juego", "pc"]


def cargar_instalaciones() -> list[dict]:
    """
    Carga el registro de instalaciones (que juego esta en que pc).

    Precondicion: existe el archivo data/instalaciones.json con formato JSON valido,
        una lista de diccionarios con las claves "juego" y "pc".
    Postcondicion: devuelve una lista de diccionarios tal cual estan en el archivo.
        Puede devolver una lista vacia si no hay ninguna instalacion registrada.
    """
    try:
        with open("data/instalaciones.json", "r", encoding="utf-8") as archivo:
            instalaciones = json.load(archivo)
    except FileNotFoundError:
        raise FileNotFoundError("No se encontro el archivo data/instalaciones.json")
    except json.JSONDecodeError:
        raise ValueError("instalaciones.json tiene un formato inválido")
    if not isinstance(instalaciones, list):
        raise ValueError("instalaciones.json debe contener una lista de instalaciones")

    for instalacion in instalaciones:
        if not isinstance(instalacion, dict):
            raise ValueError(
                "instalaciones.json: hay un elemento que no es una instalación válida"
            )
        for campo in CAMPOS_INSTALACION:
            if campo not in instalacion:
                raise ValueError(
                    f"instalaciones.json: a una instalación le falta el campo {campo}"
                )
    return instalaciones


def pcs_de_juego(nombre_juego: str, instalaciones: list[dict]) -> list[str]:
    """
    Busca en que pcs esta instalado un juego especifico.

    Precondicion: nombre_juego es un string; instalaciones es la lista
        devuelta por cargar_instalaciones().
    Postcondicion: devuelve una lista con los nombres de pc donde el juego
        esta instalado. Si no esta instalado en ninguna, devuelve lista vacia.
        No modifica instalaciones.
    """
    pcs = []
    for instalado in instalaciones:
        if instalado["juego"] == nombre_juego:
            pcs.append(instalado["pc"])
    return pcs


def guardar_instalaciones(instalaciones: list[dict]) -> None:
    """
    Contrato: Guarda el registro de instalaciones en data/instalaciones.json
    Precondiciones: instalaciones es una lista de diccionarios con las claves "juego" y "pc"
    Postcondiciones: El archivo queda con el contenido de instalaciones
    """
    filas = []
    for instalacion in instalaciones:
        juego = json.dumps(instalacion["juego"], ensure_ascii=False)
        pc = json.dumps(instalacion["pc"], ensure_ascii=False)
        filas.append("  { " + f'"juego": {juego}, "pc": {pc}' + " }")

    if len(filas) == 0:
        contenido = "[]"
    else:
        contenido = "[\n" + ",\n".join(filas) + "\n]"

    try:
        with open("data/instalaciones.json" "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
    except FileNotFoundError:
        raise FileNotFoundError("No se encontro la carpeta data/.")
    except PermissionError:
        raise PermissionError("No hay permiso para escribir data/instalaciones.json")
    except OSError as error:
        raise OSError(f"No se pudo guardar data/instalaciones.json ({error})")


def quitar_instalaciones_de_juego(instalaciones: list[dict], nombre_juego: str) -> list[dict]:
    """
    Contrato: Devuelve las instalaciones sin las que corresponden a un juego
    Precondiciones: instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Devuelve una lista nueva con todas las instalaciones cuyo juego es distinto a nombre_juego
    """
    restantes = []

    for instalacion in instalaciones:
        if instalacion["juego"] != nombre_juego:
            restantes.append(instalacion)

    return restantes
