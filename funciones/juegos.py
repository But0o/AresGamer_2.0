import json
from tabulate import tabulate
from funciones.instalaciones import pcs_de_juego

CAMPOS_JUEGO = ["nombre", "categoria", "fecha_lanzamiento", "peso"]
UNIDADES_PESO = ["MB", "GB"]


def mostrar_juegos(
    juegos: list[dict], instalaciones: list[dict], usuario: dict
) -> None:
    """
    Muestra la lista de juegos en una tabla, adaptada segun el tipo de usuario.

    Precondicion:
        - juegos es la lista devuelta por cargar_juegos().
        - instalaciones es la lista devuelta por cargar_instalaciones().
        - usuario es un diccionario con al menos las claves "usuario" y "rol",
          donde "rol" vale "admin" o "pc".

    Postcondicion:
        - Si usuario["rol"] == "admin": imprime TODOS los juegos de `juegos`,
          agregando una columna "Instalado en" con las pcs donde esta
          instalado cada uno, separadas por coma (o "-" si no esta instalado
          en ninguna).
        - Si usuario["rol"] == "pc": imprime SOLO los juegos que figuran en
          `instalaciones` con pc == usuario["usuario"].
        - No devuelve nada (return None). No modifica juegos ni instalaciones.
    """
    filas = []

    if usuario["rol"] == "admin":
        for juego in juegos:
            pcs = pcs_de_juego(juego["nombre"], instalaciones)
            if pcs:
                instalado_en = ", ".join(
                    pcs
                )  # unir la lista pcs en un string separado por coma
            else:
                instalado_en = "-"
            filas.append(
                [
                    juego["nombre"],
                    juego["categoria"],
                    juego["fecha_lanzamiento"],
                    juego["peso"],
                    instalado_en,
                ]
            )
        headers = [
            "Nombre",
            "Categoria/s",
            "Fecha de Lanzamiento",
            "Peso",
            "Instalado en",
        ]

    elif usuario["rol"] == "pc":
        for instalacion in instalaciones:
            if instalacion["pc"] == usuario["usuario"]:
                juego = buscar_juego(instalacion["juego"], juegos)
                if juego:
                    filas.append(
                        [
                            juego["nombre"],
                            juego["categoria"],
                            juego["fecha_lanzamiento"],
                            juego["peso"],
                        ]
                    )
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
    try:
        with open("data/juegos.json", "r", encoding="utf-8") as archivo:
            juegos = json.load(archivo)
    except FileNotFoundError:
        raise FileNotFoundError("No se econtro el archivo data/juegos.json")
    except json.JSONDecodeError:
        raise ValueError("juegos.json tiene un formato inválido")

    if not isinstance(juegos, list):
        raise ValueError("juegos.json debe contener una lista de juegos")

    for juego in juegos:
        if not isinstance(juego, dict):
            raise ValueError("juegos.json: hay un elemento que no es un juego válido")
        for campo in CAMPOS_JUEGO:
            if campo not in juego:
                raise ValueError(f"juegos.json: a un juego le falta el campo {campo}")
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


def buscar_juegos(juegos: list[dict], texto: str) -> list[dict]:
    """
    Contrato: Busca los juegos cuyo nombre o categoria contiene el texto
    Precondiciones: juegos es una lista de diccionarios con nombre y categoria. texto es un string no vacio
    Postcondiciones: Devuelve una lista nueva con los juegos que coinciden (puede estar vacia). No modifica la lista original
    """
    texto = texto.lower()
    resultados = []

    for juego in juegos:
        if texto in juego["nombre"].lower() or texto in juego["categoria"].lower():
            resultados.append(juego)
    return resultados


def buscar_juego_por_nombre(juegos: list[dict], nombre: str) -> dict | None:
    """
    Contrato: busca un juego por si nombre exacto
    Precondiciones: juegos es una lista de diccionarios con la clave "nombre", nombre es un string
    Postcondiciones: Devuelve el diccionario del juego o None si no existe
    """
    for juego in juegos:
        if juego["nombre"].lower() == nombre.lower():
            return juego

    return None


def guardar_juegos(juegos: list[dict]) -> None:
    """
    Contrato: Guarda la biblioteca completa de juegos en data/juegos.json
    Precondiciones: juegos es una lista de diccionarios con las claves "nombre", "categoria", "fecha_lanzamiento" y "peso"
    Postcondiciones: El archivo queda con el contenido de juegos, con el mismo formato que ya tiene
    """
    contenido = json.dumps(juegos, indent=4, ensure_ascii=False)

    try:
        with open("data/juegos.json", "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
    except FileNotFoundError:
        raise FileNotFoundError("No se encontro la carpeta data/.")
    except PermissionError:
        raise PermissionError("No hay permiso para escribir data/juegos.json")
    except OSError as error:
        raise OSError(f"No se pudo guardar data/juegos.json ({error})")


def nombre_en_uso(juegos: list[dict], nombre: str) -> bool:
    """
    Contrato: Indica si ya existe un juego con ese nombre
    Precondiciones: juegos es una lista de diccionarios con la clave "nombre", que es un string
    Postcondiciones: Devuelve True si ya hay un juego con ese nombre, False si no
    """
    for juego in juegos:
        if juego["nombre"].lower() == nombre.lower():
            return True
    return False


def pedir_texto(mensaje: str) -> str:
    """
    Contrato: Pide un texto hasta que el usuario ingrese un string vacío
    Precondiciones: mensaje es el texto que se muestra al pedir el dato
    Postcondiciones: Devuelve el texto ingresado, sin espacios al principio y al final
    """
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("El dato no puede quedar vacío")


def pedir_peso() -> str:
    """
    Contrato: Pide el peso de un juego hasta que tenga el formato " 'numero' MB " o " 'numero' GB "
    Precondiciones: -
    Postcondiciones: Devuelve el peso, con la unidad en mayusculas
    """
    while True:
        partes = input("Peso (ej: 10 MB, 2 GB): ").strip().split()

        if (
            len(partes) == 2
            and partes[0].isdecimal()
            and int(partes[0]) > 0
            and partes[1].upper() in UNIDADES_PESO
        ):
            return partes[0] + " " + partes[1].upper()
        print("Formato inválido. Escibi un número y la unidad (ej: 10 MB, 2 GB)")


def pedir_datos_juego(juegos: list[dict]) -> dict | None:
    """
    Contrato: Pideo los datos de un juego nuevo y los valida
    Precondiciones: juegos es la lista de juegos cargada (para evitar nombres repetidos)
    Postcondiciones: Devuelve un diccionario con las claves "nombre", "categoria", "fecha_lanzamiento" y "peso". Devuelve None si el nombre de seja vacio
    """
    nombre = input("Nombre del juego (vacío para cancelar): ").strip()

    while nombre != "" and nombre_en_uso(juegos, nombre):
        print("Ya existe un juego con ese nombre")
        nombre = input("Nombre del juego (vacío para cancelar): ").strip()

    if nombre == "":
        return None

    categoria = pedir_texto("Categoria/s (ej: Action, Indie): ")
    fecha = pedir_texto("Fecha de lanzamiento (ej: Jun 6, 2016): ")
    peso = pedir_peso()

    return {
        "nombre": nombre,
        "categoria": categoria,
        "fecha_lanzamiento": fecha,
        "peso": peso,
    }
