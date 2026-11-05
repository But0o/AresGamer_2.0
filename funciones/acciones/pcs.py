"""Acciones sobre las PC-Usuario: agregar, eliminar y bloquear."""

from funciones.consola.entrada import (
    confirmar,
    pedir_nombre_nuevo,
    pedir_pc,
    pedir_texto,
)
from funciones.consola.tablas import mostrar_estado_pcs
from funciones.datos.archivos import guardar_archivos
from funciones.datos.cuentas import (
    ARCHIVO_CUENTAS,
    ROL_PC,
    buscar_cuenta,
    cargar_cuentas,
    cuenta_activa,
    guardar_cuentas,
    quitar_cuenta,
    texto_cuentas,
)
from funciones.datos.instalaciones import (
    ARCHIVO_INSTALACIONES,
    cargar_instalaciones,
    juegos_instalados_en,
    quitar_instalaciones_de_pc,
    texto_instalaciones,
)


def agregar_pc() -> None:
    """
    Contrato: Pide los datos de una PC-Usuario nueva y la agrega a las cuentas
    Precondiciones: -
    Postcondiciones: Si el admin confirma, el archivo queda con la cuenta nueva (rol "pc") al final. Si cancela, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    cuentas = cargar_cuentas()

    nombre = pedir_nombre_nuevo(
        "Nombre de la PC nueva (vacío para cancelar): ",
        lambda texto: buscar_cuenta(cuentas, texto) is not None,
        "Ya existe una cuenta llamada '{}'",
    )

    if nombre is None:
        print("Operación cancelada")
        return

    clave = pedir_texto("Clave: ")

    print(f"PC-Usuario nueva: {nombre} | clave: {clave}")

    if not confirmar("¿Crear la cuenta? (s/n): "):
        print("Operación cancelada")
        return

    cuentas.append({"usuario": nombre, "clave": clave, "rol": ROL_PC})
    guardar_cuentas(cuentas)

    print(f"PC-Usuario '{nombre}' creada correctamente")


def eliminar_pc() -> None:
    """
    Contrato: Elimina una PC-Usuario junto con sus instalaciones
    Precondiciones: -
    Postcondiciones: Si el admin confirma, la cuenta y sus instalaciones se quitan de los dos archivos. Solo se ofrecen cuentas con rol "pc", nunca un admin. Si cancela, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    cuentas = cargar_cuentas()
    instalaciones = cargar_instalaciones()
    pc = pedir_pc(cuentas)

    if pc is None:
        return

    instalados = juegos_instalados_en(instalaciones, pc)

    print(f"PC-Usuario a eliminar: {pc}")
    if len(instalados) > 0:
        print(
            f"Tiene {len(instalados)} juego/s instalado/s: {', '.join(instalados)}. También se quitarán"
        )

    if not confirmar("¿Eliminarla definitivamente? (s/n): "):
        print("Operación cancelada")
        return

    guardar_archivos(
        {
            ARCHIVO_CUENTAS: texto_cuentas(quitar_cuenta(cuentas, pc)),
            ARCHIVO_INSTALACIONES: texto_instalaciones(
                quitar_instalaciones_de_pc(instalaciones, pc)
            ),
        }
    )

    print(f"PC-Usuario '{pc}' eliminada correctamente")


def bloquear_desbloquear_pc() -> None:
    """
    Contrato: Cambia el acceso de una PC-Usuario (activa a bloqueada o al reves)
    Precondiciones: -
    Postcondiciones: Si el admin confirma, la cuenta queda con el acceso contrario al que tenia. Solo se ofrecen cuentas con rol "pc", nunca un admin. Si cancela, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    cuentas = cargar_cuentas()

    mostrar_estado_pcs(cuentas)

    pc = pedir_pc(cuentas)

    if pc is None:
        return

    cuenta = buscar_cuenta(cuentas, pc)

    if cuenta_activa(cuenta):
        accion = "Bloquear"
        resultado = "bloqueada"
    else:
        accion = "Desbloquear"
        resultado = "desbloqueada"

    if not confirmar(f"¿{accion} {pc}? (s/n): "):
        print("Operación cancelada")
        return

    cuenta["activa"] = not cuenta_activa(cuenta)
    guardar_cuentas(cuentas)

    print(f"PC-Usuario '{pc}' {resultado} correctamente")
