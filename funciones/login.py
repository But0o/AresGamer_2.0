"""Inicio de sesion: valida credenciales con las cuentas del sistema"""

def login(usuario_ingresado: str, contraseña_ingresada: str, cuentas: list[dict]) -> dict | None:
    """
    Contrato:
        Valida la scredenciales ingresadas contra la lista de las cuentas

    Precondiciones:
        usuario_ingresado y contraseña_ingresada son strings
        lo ingresado por el usuario por consola. cuentas es la lista devuelta por cargar_cuentas()

    Postcondiciones: 
        Si existe una cuenta que "Usuario" y "Contraseña" coinciden con los parametros
        devuelve el diccionario completo de esa cuenta (con usuario, contraseña y tipo). 
        si no hay ninguna coincidencia devuelve None no modifica la lista cuentas
    """

    for cuenta in cuentas:
        if cuenta["usuario"] == usuario_ingresado and cuenta["contraseña"] == contraseña_ingresada:
            return cuenta
    return None
