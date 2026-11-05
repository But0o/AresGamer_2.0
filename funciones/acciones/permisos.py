"""Acciones sobre los permisos: otorgar y quitar el permiso de administrador."""

from funciones.consola.entrada import confirmar, elegir_de_lista, pedir_pc
from funciones.datos.archivos import guardar_archivos
from funciones.datos.cuentas import (
    ADMIN_ORIGINAL,
    ARCHIVO_CUENTAS,
    ROL_ADMIN,
    ROL_PC,
    admins_que_se_pueden_quitar,
    buscar_cuenta,
    cargar_cuentas,
    cuenta_activa,
    guardar_cuentas,
    texto_cuentas,
)
from funciones.datos.instalaciones import (
    ARCHIVO_INSTALACIONES,
    cargar_instalaciones,
    juegos_instalados_en,
    quitar_instalaciones_de_pc,
    texto_instalaciones,
)


def otorgar_admin() -> None:
    """
    Contrato: Convierte una PC-Usuario en administrador
    Precondiciones: -
    Postcondiciones: Si el admin confirma, la cuenta queda con rol "admin" y sin instalaciones, porque deja de ser una PC-Usuario. Una PC bloqueada no se puede convertir hasta desbloquearla. Si cancela, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    cuentas = cargar_cuentas()
    instalaciones = cargar_instalaciones()
    pc = pedir_pc(cuentas)

    if pc is None:
        return

    cuenta = buscar_cuenta(cuentas, pc)

    if not cuenta_activa(cuenta):
        print(f"{pc} está bloqueada, primero hay que desbloquearla")
        return

    instalados = juegos_instalados_en(instalaciones, pc)

    print(f"{pc} va a tener acceso completo y dejará de ser una PC-Usuario")
    if len(instalados) > 0:
        print(
            f"Tiene {len(instalados)} juego/s instalado/s: {', '.join(instalados)}. Se quitarán de sus instalaciones"
        )

    if not confirmar("¿Otorgar permiso de administrador? (s/n): "):
        print("Operación cancelada")
        return

    cuenta["rol"] = ROL_ADMIN

    guardar_archivos(
        {
            ARCHIVO_CUENTAS: texto_cuentas(cuentas),
            ARCHIVO_INSTALACIONES: texto_instalaciones(
                quitar_instalaciones_de_pc(instalaciones, pc)
            ),
        }
    )

    print(f"'{pc}' ahora es administrador")


def quitar_admin(usuario: dict) -> None:
    """
    Contrato: Convierte otra cuenta de administrador en PC-Usuario
    Precondiciones: usuario es la cuenta del admin logueado
    Postcondiciones: Si el admin confirma, la cuenta elegida queda con rol "pc". No se puede elegir al admin logueado ni a la cuenta ADMIN_ORIGINAL. Si cancela, nada cambia. Si falla el guardado, nada cambia y se lanza ErrorDeDatos
    """
    cuentas = cargar_cuentas()
    admins = admins_que_se_pueden_quitar(cuentas, usuario["usuario"])

    if len(admins) == 0:
        print(
            "No hay administradores a los que se les pueda quitar el permiso "
            f"(ni a vos mismo ni a la cuenta '{ADMIN_ORIGINAL}')"
        )
        return

    print(f"Administradores disponibles: {', '.join(admins)}")

    elegida = elegir_de_lista(
        "Nombre de la cuenta (vacío para cancelar): ",
        admins,
        "'{}' no es una opción válida",
    )

    if elegida is None:
        print("Operación cancelada")
        return

    if not confirmar(f"¿Quitarle el permiso de administrador a {elegida}? (s/n): "):
        print("Operación cancelada")
        return

    buscar_cuenta(cuentas, elegida)["rol"] = ROL_PC
    guardar_cuentas(cuentas)

    print(f"'{elegida}' ahora es una PC-Usuario")
