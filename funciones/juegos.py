import json
from tabulate import tabulate
from funciones.instalaciones import pcs_de_juego

def mostrar_juegos(juegos: list[dict], instalaciones: list[dict], usuario: dict) -> None:
    """
    Muestra la lista de juegos en una tabla, adaptada segun el tipo de usuario.

    Precondicion:
        - juegos es la lista devuelta por cargar_juegos().
        - instalaciones es la lista devuelta por cargar_instalaciones().
        - usuario es un diccionario con al menos las claves "usuario" y "tipo",
          donde "tipo" vale "admin" o "pc".

    Postcondicion:
        - Si usuario["tipo"] == "admin": imprime TODOS los juegos de `juegos`,
          agregando una columna "Instalado en" con las pcs donde esta
          instalado cada uno, separadas por coma (o "-" si no esta instalado
          en ninguna).
        - Si usuario["tipo"] == "pc": imprime SOLO los juegos que figuran en
          `instalaciones` con pc == usuario["usuario"].
        - No devuelve nada (return None). No modifica juegos ni instalaciones.
    """
    filas = []

    if usuario["tipo"] == "admin":
        for juego in juegos:
            pcs = pcs_de_juego(juego["nombre"], instalaciones)
            if pcs:
                instalado_en = ", ".join(pcs)   # unir la lista pcs en un string separado por coma
            else:
                instalado_en = "-"
            filas.append([juego["nombre"], juego["categoria"], juego["fecha_lanzamiento"], juego["peso"], instalado_en])
        headers = ["Nombre", "Categoria/s", "Fecha de Lanzamiento", "Peso", "Instalado en"]

    elif usuario["tipo"] == "pc":
        for instalacion in instalaciones:
            if instalacion["pc"] == usuario["usuario"]:
                juego = buscar_juego(instalacion["juego"], juegos)
                if juego:
                    filas.append([juego["nombre"], juego["categoria"], juego["fecha_lanzamiento"], juego["peso"]])
        headers = ["Nombre", "Categoria/s", "Fecha de Lanzamiento", "Peso"]

    print(tabulate(filas, headers=headers, tablefmt="grid"))

def cargar_juegos() -> list[dict]:
    """
    Carga la biblioteca completa de juegos.

    Precondicion: existe el archivo data/juegos.json con formato JSON valido,
        una lista de diccionarios con las claves "nombre", "categoria",
        "fecha_lanzamiento" y "peso".
    Postcondicion: devuelve una lista de diccionarios tal cual estan en el
        archivo. No valida ni filtra nada, solo carga.
    """
    with open("data/juegos.json", "r", encoding="utf-8") as archivo:
        juegos = json.load(archivo)
    return juegos

def buscar_juego(nombre: str, juegos: list[dict]) -> dict | None:
    """
    Busca el diccionario completo de un juego a partir de su nombre.

    Precondicion: nombre es un string; juegos es la lista devuelta por
        cargar_juegos().
    Postcondicion: devuelve el diccionario del juego cuyo campo "nombre"
        coincide exactamente con el parametro nombre. Si no lo encuentra,
        devuelve None. No modifica juegos.
    """
    for juego in juegos:
        if juego["nombre"] == nombre:
            return juego
    return None
