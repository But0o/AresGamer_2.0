import json
from tabulate import tabulate

def mostrar_juegos(juegos):
    filas = []
    for juego in juegos:
        filas.append([juego["nombre"],juego["categoria"],juego["fecha_lanzamiento"],juego["peso"]])  
                      
    print(tabulate(filas, headers=["Nombre","Categoria/s","Fecha de Lanzamiento","Peso"], tablefmt="grid"))


def cargar_juegos():
    with open("data/juegos.json", "r", encoding="utf-8") as archivo:
        juegos = json.load(archivo)
    return juegos

