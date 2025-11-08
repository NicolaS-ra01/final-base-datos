Descripción del Proyecto

Este repositorio contiene la solución completa de Base de Datos y su aplicación cliente (GUI) para la gestión operativa de una cafetería.

El sistema se compone de:

    Base de Datos (CafeteriaDB_MS): Implementada en SQL Server. Incluye tablas, datos, procedimientos almacenados (CRUD), vistas, consultas avanzadas, y Triggers de auditoría y lógica de negocio.

    Aplicación Cliente (app_cafeteria.py): Interfaz gráfica desarrollada en Python (Tkinter) que consume directamente la lógica de negocio a través de Procedimientos Almacenados usando la librería pyodbc.

 Requisitos del Sistema

Para desplegar y probar el proyecto se necesitan los siguientes componentes:
Componente	Requisito	Notas
Servidor DB	SQL Server (versión 2017+ recomendada)	Se puede usar localmente o en un contenedor Docker.
Driver ODBC	ODBC Driver 18 for SQL Server	Necesario para que Python se conecte a SQL Server.
Python	Python 3.8 o superior	Entorno de ejecución para la interfaz gráfica.
Librerías Python	pyodbc	Se instala vía pip install pyodbc.


Paso 1: Configurar e Inicializar la Base de Datos

    Abre SQL Server Management Studio (SSMS) o Azure Data Studio.

    Crea una nueva base de datos con el nombre CafeteriaDB_MS (opcional si usas el script completo, ya que puedes ejecutar todo el contenido de SQLQuery_6.sql en modo "SQLCMD" si la primera línea lo requiere).

    Ejecuta el archivo SQLQuery_6.sql en la base de datos CafeteriaDB_MS.

        Este script se encarga de:

            Crear todas las tablas (DDL).

            Insertar los datos de prueba (DML).

            Crear todos los Procedimientos Almacenados.

            Crear todas las Vistas.

            Crear todos los Triggers (TR_Auditoria_Productos_Precio y TR_ActualizarTotalPedido).

    Importante: Asegúrate de tener un usuario SQL con credenciales (sa y TuContraseña123!) o ajusta las credenciales en el script SQL y en el archivo Python (app_cafeteria.py).

Paso 2: Configurar el Entorno Python

    Asegúrate de tener Python instalado.

    Instala la librería de conexión pyodbc:
    Bash

pip install pyodbc

Verifica y ajusta la conexión en la primera sección del archivo app_cafeteria.py:
Python

    DRIVER = "ODBC Driver 18 for SQL Server"
    SERVER = "localhost,1433"   
    DATABASE = "CafeteriaDB_MS"
    UID = "sa"                  
    PWD = "TuContraseña123!"    
    # ...

Paso 3: Ejecutar la Aplicación

    Abre una terminal o símbolo del sistema.

    Navega hasta la carpeta donde se encuentra el archivo app_cafeteria.py.

    Ejecuta la aplicación:
    Bash

    python app_cafeteria.py

Si la conexión es exitosa, la interfaz gráfica se abrirá, permitiendo probar las operaciones CRUD y el flujo de ventas que consumen los SPs y Triggers.

