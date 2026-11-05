# 🎮 AresGamer 2.0

**Gestioná tus juegos. Organizá tus PCs.**

AresGamer 2.0 es un programa de consola para cibers, locales de videojuegos y espacios de simuladores. Permite administrar la biblioteca de juegos y saber qué hay instalado en cada PC del local.

Funciona completamente **offline** y guarda toda la información en archivos **JSON**.

## 🚀 Cómo empezar

Necesitás [uv](https://docs.astral.sh/uv/), que se encarga de instalar Python 3.14 y las dependencias.

```bash
uv sync           # Prepara el entorno (solo la primera vez)
uv run main.py    # Abre el programa
```

Sin uv, con Python 3.14 instalado:

```bash
pip install -r requirements.txt
python main.py
```

### 🔑 Cuentas de prueba

| Usuario | Clave    | Rol           |
|---------|----------|---------------|
| admin   | admin123 | Administrador |
| PC01    | 1234     | PC-Usuario    |
| PC02    | 1234     | PC-Usuario    |
| PC03    | 1234     | PC-Usuario    |
| PC04    | 1234     | PC-Usuario    |

El usuario no distingue mayúsculas de minúsculas, pero la clave sí. Cada inicio de sesión permite hasta 3 intentos.

## ⚙️ Qué se puede hacer

### 👑 Administrador

Es el dueño o encargado del local.

| Área | Opciones |
|------|----------|
| **Biblioteca** | Listar, buscar, agregar y eliminar juegos |
| **Instalaciones** | Instalar y desinstalar juegos en una PC, ver qué tiene cada PC y qué juegos no están instalados en ninguna |
| **PC-Usuarios** | Crear, eliminar, bloquear y desbloquear cuentas de PC |
| **Permisos** | Otorgar y quitar el permiso de administrador |

### 🖥️ PC-Usuario

Es la cuenta de cada máquina del local. Solo puede listar y buscar los juegos instalados en esa PC.

### 📏 Reglas del sistema

* Una PC bloqueada no puede iniciar sesión.
* Al eliminar un juego, también se quita de las PCs donde estaba instalado.
* Al eliminar una PC o convertirla en administrador, se quitan sus instalaciones.
* Una PC bloqueada no puede pasar a ser administrador hasta que se la desbloquee.
* Un administrador no puede quitarse el permiso a sí mismo.
* La cuenta `admin` original no puede perder su permiso.
* Los cambios importantes piden confirmación antes de guardarse.
* Si falla un guardado, los archivos quedan como estaban.

## 💾 Datos

Los archivos están en la carpeta `data/`:

| Archivo | Contenido |
|---------|-----------|
| `juegos.json` | Biblioteca general: nombre, categorías, fecha de lanzamiento y peso |
| `cuentas.json` | Cuentas: usuario, clave, rol y si están bloqueadas |
| `instalaciones.json` | Qué juego está instalado en qué PC |

Formatos que pide el programa al agregar un juego:

* **Peso:** un número y `MB` o `GB`, como `10 MB` o `1.5 GB`.
* **Fecha de lanzamiento:** con el mes en inglés, como `Jun 6, 2016`, o `Coming soon`.

> ⚠️ Las claves se guardan sin cifrar en `cuentas.json`. El proyecto tiene fines académicos: no uses contraseñas reales.

## 📁 Estructura del proyecto

```text
AresGamer_2.0/
├── main.py                  # Punto de entrada
├── funciones/
│   ├── sesion.py            # Login y menús de cada rol
│   ├── acciones/            # Una función por cada opción de los menús
│   │   ├── biblioteca.py
│   │   ├── instalaciones.py
│   │   ├── pcs.py
│   │   └── permisos.py
│   ├── consola/             # Pedir datos y mostrar tablas y menús
│   │   ├── entrada.py
│   │   ├── menu.py
│   │   └── tablas.py
│   └── datos/               # Archivos JSON y reglas, sin print ni input
│       ├── archivos.py
│       ├── cuentas.py
│       ├── instalaciones.py
│       └── juegos.py
├── data/                    # Información del sistema
├── tests/                   # Pruebas automáticas
├── presentaciones/          # Presentación del proyecto
├── pyproject.toml           # Configuración del proyecto y dependencias
├── uv.lock                  # Versiones exactas para uv
└── requirements.txt         # Dependencias para pip
```

Cada capa usa solo las que están debajo: `sesion` → `acciones` → `consola` → `datos`.

### Agregar una opción al menú

1. Escribí la función en `funciones/acciones/`.
2. Sumala a la lista de `opciones_de_usuario` en `funciones/sesion.py`.

Los números del menú se generan solos.

## 🧪 Pruebas

```bash
uv run pytest
```

Las pruebas no modifican los archivos de `data/`: lo que guardan va a una carpeta temporal.

## 🛠️ Tecnologías

* 🐍 **Python 3.14**
* 📄 **JSON** para guardar los datos
* 📊 **Tabulate** para las tablas de la consola
* ✅ **pytest** para las pruebas
* 📦 **uv** para el entorno y las dependencias
* 🐙 **Git / GitHub** para el trabajo en equipo

## ✅ Estado del proyecto

* [x] Login y diferenciación de usuarios.
* [x] Listado y búsqueda de juegos.
* [x] Consulta de juegos instalados.
* [x] Agregar y eliminar juegos.
* [x] Agregar y eliminar PC-Usuarios.
* [x] Instalar y desinstalar juegos.
* [x] Gestión de permisos.
* [x] Listados administrativos.
* [x] Pruebas y corrección de errores.

## 👥 Integrantes

* [Sebastian Carini](https://github.com/Seuz1111)
* [Ignacio Sandes](https://github.com/Ignacio2710)
* [Mariano Quilindro](https://github.com/marianoquilindro)
* [Agustin Lamendola](https://github.com/But0o)

## 🎓 Proyecto académico

Trabajo práctico desarrollado para la materia **Programación 2**.
