# daWaitress

Aplicación de gestión de pedidos para restaurante, desarrollada en Python usando Flet como framework de interfaz gráfica y SQLite como base de datos local.

La aplicación permite manejar usuarios, mesas, productos y pedidos desde una interfaz de escritorio/web a pantalla completa.

## Características

- Sistema de usuarios (tabla `USERS`).
- Gestión de mesas por área (tabla `TABLES`).
- Gestión de productos con categoría, precio, información y ruta de imagen (tabla `PRODUCTS`).
- Registro de pedidos en curso por mesa y área (tabla `WORKING`).
- Interfaz gráfica en Flet con diferentes pantallas:
  - Pantalla de login (`LOGIN`).
  - Pantalla principal (`HOME`).
  - Pantalla de edición de productos/mesas (`EDITOR`).
- Selector de archivos para cargar imágenes de productos (`FilePicker`).
- Modo oscuro por defecto, con opción de cambiar el tema.

## Tecnologías utilizadas

- Python 3.x
- [Flet](https://flet.dev/)
- SQLite3 (base de datos embebida)
- Módulo estándar `os` para manejo de directorios e imágenes

## Estructura del proyecto

```text
daWaitress/
├─ main.py
├─ db.db              # Base de datos SQLite (se crea automáticamente)
├─ images/            # Carpeta de imágenes (se crea si no existe)
└─ pages/
   ├─ LOGIN.py
   ├─ HOME.py
   └─ EDITOR.py
