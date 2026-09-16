import json

def cargar_cuentas() -> list[dict]:
    """
    Carga las cuentas del sistema (admin y pc-usuarios).

    Precondicion: existe el archivo data/cuentas.json con formato JSON valido,
        una lista de diccionarios con las claves "usuario", "contrasenia", "tipo".
    Postcondicion: devuelve una lista de diccionarios tal cual estan en el archivo.
        No valida ni filtra nada, solo carga.
    """
    with open("data/cuentas.json", "r", encoding="utf-8") as archivo:
            cuentas = json.load(archivo)
    return cuentas
