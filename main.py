"""AresGamer 2.0"""

from funciones.datos.archivos import ErrorDeDatos
from funciones.datos.juegos import cargar_juegos
from funciones.sesion import menu_inicial


def main() -> None:
    """
    Contrato: Punto de entrada al programa, carga la biblioteca de juegos y arranca el menu inicial
    Precondiciones: -
    Postcondiciones: Si no se puede cargar la biblioteca, muestra el motivo y termina. Si no, termina cuando el usuario sale del menu o corta la entrada (Ctrl+C o Ctrl+D)
    """
    try:
        juegos = cargar_juegos()
    except ErrorDeDatos as error:
        print(f"Error al cargar la biblioteca de juegos: {error}")
        return

    try:
        menu_inicial(juegos)
    except (KeyboardInterrupt, EOFError):
        print("\nHasta luego")


if __name__ == "__main__":
    main()
