"""Funciones para pedir datos por consola."""

from collections.abc import Callable

from funciones.datos.cuentas import nombres_de_pcs


def pedir_texto(mensaje: str) -> str:
    """
    Contrato: Pide un texto hasta que el usuario ingrese uno que no este vacio
    Precondiciones: mensaje es el texto que se muestra al pedir el dato
    Postcondiciones: Devuelve el texto ingresado, sin espacios al principio y al final
    """
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("El dato no puede quedar vacío")


def pedir_nombre_nuevo(
    mensaje: str, ya_existe: Callable[[str], bool], aviso: str
) -> str | None:
    """
    Contrato: Pide un nombre hasta que no este repetido
    Precondiciones: ya_existe recibe un nombre y devuelve True si esta en uso. aviso es el mensaje para un nombre repetido, con {} donde va el nombre
    Postcondiciones: Devuelve el nombre sin espacios al principio y al final. Devuelve None si se ingresa vacio
    """
    while True:
        nombre = input(mensaje).strip()

        if nombre == "":
            return None
        if not ya_existe(nombre):
            return nombre

        print(aviso.format(nombre))


def elegir_de_lista(mensaje: str, opciones: list[str], aviso: str) -> str | None:
    """
    Contrato: Pide un nombre hasta que coincida con una de las opciones, sin distinguir mayusculas
    Precondiciones: opciones es una lista de strings. aviso es el mensaje para un nombre invalido, con {} donde va el nombre
    Postcondiciones: Devuelve la opcion tal como esta escrita en la lista. Devuelve None si se ingresa vacio
    """
    while True:
        nombre = input(mensaje).strip()

        if nombre == "":
            return None

        for opcion in opciones:
            if opcion.lower() == nombre.lower():
                return opcion

        print(aviso.format(nombre))


def pedir_pc(cuentas: list[dict]) -> str | None:
    """
    Contrato: Muestra las PC-Usuario y pide el nombre de una hasta que exista
    Precondiciones: cuentas es la lista devuelta por cargar_cuentas
    Postcondiciones: Devuelve el nombre de la PC. Si no hay PCs o se ingresa vacio, avisa que se cancela y devuelve None
    """
    pcs = nombres_de_pcs(cuentas)

    if len(pcs) == 0:
        print("No hay PC-Usuarios registradas")
    else:
        print(f"PCs disponibles: {', '.join(pcs)}")
        pc = elegir_de_lista(
            "Nombre de la PC (vacío para cancelar): ", pcs, "No existe la PC '{}'"
        )
        if pc is not None:
            return pc

    print("Operación cancelada")
    return None


def confirmar(mensaje: str) -> bool:
    """
    Contrato: Hace una pregunta de si o no y repite hasta recibir una respuesta valida
    Precondiciones: mensaje es el texto de la pregunta
    Postcondiciones: Devuelve True si el usuario responde "s" o "si", False si responde "n" o "no"
    """
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta == "s" or respuesta == "si":
            return True
        if respuesta == "n" or respuesta == "no":
            return False
        print("Respuesta inválida, respondé s/si o n/no")
