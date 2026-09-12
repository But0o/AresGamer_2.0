# 🎮 AresGamer 2.0

Sistema de gestión de juegos para cibers, locales de videojuegos y espacios de simuladores.

## 📌 Descripción

**AresGamer 2.0** es un sistema desarrollado en **Python** para administrar una biblioteca de videojuegos y controlar qué juegos se encuentran disponibles e instalados en las diferentes PC-Usuario de un establecimiento.

El sistema funciona completamente **offline**, utilizando archivos **JSON** para almacenar la información.

Cuenta con dos tipos de usuarios:

* 👑 **Administrador:** acceso completo a la gestión del sistema.
* 🖥️ **PC-Usuario:** acceso únicamente a los juegos asignados a su cuenta.

---

## 🎯 Objetivos

* Administrar una biblioteca de videojuegos.
* Gestionar las cuentas y permisos de las PC-Usuario.
* Controlar los juegos instalados en cada PC.
* Mantener la información almacenada localmente mediante archivos JSON.
* Desarrollar una interfaz de consola simple y organizada.

---

## ⚙️ Funcionalidades

### 👑 Administrador

* Listar y buscar juegos.
* Agregar y eliminar juegos.
* Crear y eliminar PC-Usuarios.
* Consultar cuentas y juegos instalados.
* Asignar o quitar juegos de las PC-Usuario.
* Gestionar permisos.

### 🖥️ PC-Usuario

* Iniciar sesión.
* Ver los juegos disponibles.
* Buscar juegos dentro de su biblioteca.
* Salir del sistema.

---

## 💾 Almacenamiento

El proyecto funcionará completamente **offline** mediante archivos JSON:

```text
data/
├── juegos.json
├── cuentas.json
└── instalaciones.json
```

* `juegos.json` → Biblioteca general de juegos.
* `cuentas.json` → Información de las cuentas.
* `instalaciones.json` → Juegos asignados a cada PC-Usuario.

---

## 🛠️ Tecnologías

* 🐍 **Python**
* 📄 **JSON**
* 📊 **Tabulate**
* 🐙 **Git / GitHub**

`Tabulate` será utilizada para mostrar la información del sistema mediante tablas en la consola.

---

## 📁 Estructura del proyecto

```text
AresGamer2.0/
│
├── main.py
├── funciones/
│   ├── menus.py
│   ├── login.py
│   ├── juegos.py
│   ├── usuarios.py
│   └── instalaciones.py
│
├── data/
│   ├── juegos.json
│   ├── cuentas.json
│   └── instalaciones.json
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 📅 Entregas

### Primera entrega — 18

La primera entrega tendrá como objetivo contar con la **idea y estructura principal del proyecto**, junto con la documentación y al menos **3 funcionalidades funcionando**.

**Funciones previstas:**

* [ ] Login y diferenciación de usuarios.
* [x] Listado de biblioteca.
* [ ] Búsqueda de juegos.
* [ ] Consulta de juegos instalados.

### Desarrollo restante

Luego de la primera entrega se completarán las funciones administrativas:

* [ ] Agregar / eliminar juegos.
* [ ] Agregar / eliminar PC-Usuarios.
* [ ] Modificar juegos instalados.
* [ ] Gestión de permisos.
* [ ] Listados administrativos.
* [ ] Pruebas y corrección de errores.

---

## 🚀 Ejecución

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el programa:

```bash
python main.py
```

---

## 👥 Integrantes

* [Sebastian Carini](https://github.com/Seuz1111)
* [Ignacio Sandes](https://github.com/Ignacio2710)
* [Mariano Quilindro](https://github.com/marianoquilindro)
* [Agustin Lamendola](https://github.com/But0o)

---

## 🎓 Proyecto académico

Trabajo práctico desarrollado para la materia **Programación 2**.

**AresGamer 2.0** — *Gestioná tus juegos. Organizá tus PCs.*
