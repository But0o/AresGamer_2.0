"""Tablas que se muestran por consola."""

from tabulate import tabulate

from funciones.datos.cuentas import ROL_ADMIN, ROL_PC, cuenta_activa
from funciones.datos.instalaciones import juegos_instalados_en, pcs_de_juego
from funciones.datos.juegos import juegos_de_pc


def mostrar_juegos(
    juegos: list[dict], instalaciones: list[dict], usuario: dict
) -> None:
    """
    Contrato: Muestra los juegos en una tabla, adaptada segun el rol del usuario
    Precondiciones: juegos es una lista de juegos. instalaciones es la lista devuelta por cargar_instalaciones. usuario tiene las claves "usuario" y "rol"
    Postcondiciones: El admin ve todos los juegos de la lista y en que PCs estan. La PC ve solo los juegos de la lista que tiene instalados. Si no hay ninguno para mostrar, imprime un aviso
    """
    filas = []
    headers = ["Nombre", "Categoria/s", "Fecha de Lanzamiento", "Peso"]

    if usuario["rol"] == ROL_ADMIN:
        headers.append("Instalado en")
        for juego in juegos:
            pcs = pcs_de_juego(juego["nombre"], instalaciones)
            filas.append(_fila_juego(juego) + [", ".join(pcs) or "-"])
    else:
        for juego in juegos_de_pc(juegos, instalaciones, usuario["usuario"]):
            filas.append(_fila_juego(juego))

    if len(filas) == 0:
        print("No hay juegos para mostrar")
        return

    print(tabulate(filas, headers=headers, tablefmt="grid"))


def _fila_juego(juego: dict) -> list[str]:
    """
    Contrato: Arma la fila de la tabla de un juego
    Precondiciones: juego es un diccionario devuelto por cargar_juegos
    Postcondiciones: Devuelve una lista con nombre, categoria, fecha y peso
    """
    return [
        juego["nombre"],
        juego["categoria"],
        juego["fecha_lanzamiento"],
        juego["peso"],
    ]


def mostrar_instalaciones_por_pc(pcs: list[str], instalaciones: list[dict]) -> None:
    """
    Contrato: Muestra una tabla con la cantidad y los nombres de los juegos instalados en cada PC
    Precondiciones: pcs es la lista de nombres de PC-Usuario. instalaciones es la lista devuelta por cargar_instalaciones
    Postcondiciones: Imprime una fila por cada PC, en el orden de pcs. Si una PC no tiene juegos, muestra "-"
    """
    filas = []

    for pc in pcs:
        nombres = juegos_instalados_en(instalaciones, pc)
        filas.append([pc, len(nombres), "\n".join(nombres) or "-"])

    print(tabulate(filas, headers=["PC", "Cantidad", "Juegos instalados"], tablefmt="grid"))


def mostrar_estado_pcs(cuentas: list[dict]) -> None:
    """
    Contrato: Muestra una tabla con las PC-Usuario y si estan activas o bloqueadas
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Imprime una fila por cada cuenta con rol "pc", en el orden del archivo
    """
    filas = []

    for cuenta in cuentas:
        if cuenta["rol"] == ROL_PC:
            if cuenta_activa(cuenta):
                filas.append([cuenta["usuario"], "activa"])
            else:
                filas.append([cuenta["usuario"], "bloqueada"])

    print(tabulate(filas, headers=["PC", "Acceso"], tablefmt="grid"))
