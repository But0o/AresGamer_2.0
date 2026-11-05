"""Acciones sobre las instalaciones: instalar, desinstalar y consultar."""

from funciones.consola.entrada import confirmar, elegir_de_lista, pedir_pc
from funciones.consola.tablas import mostrar_instalaciones_por_pc
from funciones.datos.cuentas import cargar_cuentas, nombres_de_pcs
from funciones.datos.instalaciones import (
    cargar_instalaciones,
    desinstalar_juego,
    guardar_instalaciones,
    instalar_juego,
    juegos_instalados_en,
)
from funciones.datos.juegos import buscar_juego


def _pedir_juego(juegos: list[dict]) -> dict | None:
    """
    Contrato: Pide el nombre de un juego hasta que exista en la biblioteca
    Precondiciones: juegos es la biblioteca cargada en memoria
    Postcondiciones: Devuelve el diccionario del juego. Devuelve None si se deja el nombre vacio
    """
    while True:
        nombre = input("Nombre del juego (vacío para cancelar): ").strip()

        if nombre == "":
            return None

        juego = buscar_juego(juegos, nombre)

        if juego is not None:
            return juego

        print(f"No existe el juego llamado '{nombre}'")


def instalar_en_pc(juegos: list[dict]) -> None:
    """
    Contrato: Instala un juego de la biblioteca en una PC-Usuario y guarda el cambio
    Precondiciones: juegos es la biblioteca cargada en memoria
    Postcondiciones: Si el admin confirma, el archivo queda con la instalacion nueva. Si cancela o el juego ya estaba en esa PC, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    instalaciones = cargar_instalaciones()
    pc = pedir_pc(cargar_cuentas())

    if pc is None:
        return

    juego = _pedir_juego(juegos)

    if juego is None:
        print("Operación cancelada")
        return

    if juego["nombre"] in juegos_instalados_en(instalaciones, pc):
        print(f"'{juego['nombre']}' ya está instalado en {pc}")
        return

    if not confirmar(f"¿Instalar '{juego['nombre']}' en {pc}? (s/n): "):
        print("Operación cancelada")
        return

    instalar_juego(instalaciones, juego["nombre"], pc)
    guardar_instalaciones(instalaciones)

    print(f"Juego '{juego['nombre']}' instalado en {pc}")


def desinstalar_de_pc() -> None:
    """
    Contrato: Desinstala un juego de una PC-Usuario y guarda el cambio
    Precondiciones: -
    Postcondiciones: Si el admin confirma, el archivo queda sin esa instalacion. Si cancela o la PC no tiene juegos, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    instalaciones = cargar_instalaciones()
    pc = pedir_pc(cargar_cuentas())

    if pc is None:
        return

    instalados = juegos_instalados_en(instalaciones, pc)

    if len(instalados) == 0:
        print(f"{pc} no tiene juegos instalados")
        return

    print(f"Juegos instalados en {pc}: {', '.join(instalados)}")

    elegido = elegir_de_lista(
        "Nombre del juego a desinstalar (vacío para cancelar): ",
        instalados,
        f"'{{}}' no está instalado en {pc}",
    )

    if elegido is None:
        print("Operación cancelada")
        return

    if not confirmar(f"¿Desinstalar '{elegido}' de {pc}? (s/n): "):
        print("Operación cancelada")
        return

    desinstalar_juego(instalaciones, elegido, pc)
    guardar_instalaciones(instalaciones)

    print(f"Juego '{elegido}' desinstalado de {pc}")


def consultar_instalados() -> None:
    """
    Contrato: Muestra cuantos y cuales juegos tiene instalados cada PC-Usuario
    Precondiciones: -
    Postcondiciones: Imprime una tabla con una fila por PC, o un aviso si no hay PCs
    """
    pcs = nombres_de_pcs(cargar_cuentas())

    if len(pcs) == 0:
        print("No hay PC-Usuarios registradas")
        return

    mostrar_instalaciones_por_pc(pcs, cargar_instalaciones())
