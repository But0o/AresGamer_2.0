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
