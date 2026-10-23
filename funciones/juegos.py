import json
from tabulate import tabulate


def mostrar_juegos(juegos):
    """
    Contrato: Muestra por consola una tabla con los juegos recibidos
    Precondiciones: juegos es una lista de diccionarios con nombre, categoria, fecha_lanzamiento y peso
    Postcondiciones: Imprime la tabla en pantalla. No modifica la lista recibida ni devuelve nada
    """
    filas = []
    for juego in juegos:
        filas.append(
            [
                juego["nombre"],
                juego["categoria"],
                juego["fecha_lanzamiento"],
                juego["peso"],
            ]
        )

    print(
        tabulate(
            filas,
            headers=["Nombre", "Categoria/s", "Fecha de Lanzamiento", "Peso"],
            tablefmt="grid",
        )
    )


def cargar_juegos():
    """
    Contrato: Carga la biblioteca de juegos desde data/juegos.json
    Precondiciones: Existe data/juegos.json con una lista de diccionarios
    Postcondiciones: Devuelve la lista de juegos
    """
    with open("data/juegos.json", "r", encoding="utf-8") as archivo:
        juegos = json.load(archivo)
    return juegos


def buscar_juegos(juegos: list[dict], texto: str) -> list[dict]:
    """
    Contrato: Busca los juegos juyo nombre o categoria contiene el texto
    Precondiciones: juegos es una lista de diccionarios con nombre y categoria. texto es un string no vacio
    Postcondiciones: Devuelve una lista nueva con los juegos que coinciden (puede estar vacia). No modifica la lista original
    """
    texto = texto.lower()
    resultados = []

    for juego in juegos:
        if texto in juego["nombre"].lower() or texto in juego["categoria"].lower():
            resultados.append(juego)
    return resultados
