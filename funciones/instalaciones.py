import json

def cargar_instalaciones() -> list[dict]:
    """
    Carga el registro de instalaciones (que juego esta en que pc).

    Precondicion: existe el archivo data/instalaciones.json con formato JSON valido,
        una lista de diccionarios con las claves "juego" y "pc".
    Postcondicion: devuelve una lista de diccionarios tal cual estan en el archivo.
        Puede devolver una lista vacia si no hay ninguna instalacion registrada.
    """
    with open("data/instalaciones.json", "r", encoding="utf-8") as archivo:
                instalados = json.load(archivo)
    return instalados

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