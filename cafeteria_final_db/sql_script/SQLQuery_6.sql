-- Verificar y crear la base de datos (Opcional, si tienes permisos)
-- USE master;
-- GO
-- IF DB_ID('CafeteriaDB_MS') IS NOT NULL DROP DATABASE CafeteriaDB_MS;
-- GO
-- CREATE DATABASE CafeteriaDB_MS;
-- GO
-- USE CafeteriaDB_MS;
-- GO

-- 1. CREACIÓN DE TABLAS (USANDO IDENTITY(1,1))
-------------------------------------------------------------------------------------------------

CREATE TABLE Empleados (
    empleado_id INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    salario DECIMAL(10, 2)
);

CREATE TABLE Productos (
    producto_id INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion NVARCHAR(MAX),
    precio DECIMAL(10, 2) NOT NULL,
    tipo_producto VARCHAR(50) NOT NULL
);

CREATE TABLE Ingredientes (
    ingrediente_id INT PRIMARY KEY IDENTITY(1,1),
    nombre_ingrediente VARCHAR(100) NOT NULL UNIQUE,
    unidad_medida VARCHAR(20) NOT NULL,
    stock_actual DECIMAL(10, 2) NOT NULL,
    stock_minimo DECIMAL(10, 2) NOT NULL DEFAULT 10
);

CREATE TABLE Pedidos (
    pedido_id INT PRIMARY KEY IDENTITY(1,1),
    fecha_hora DATETIME NOT NULL,
    empleado_id INT,
    estado VARCHAR(50) NOT NULL,
    total_pedido DECIMAL(10, 2),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
);

CREATE TABLE Detalle_Pedido (
    detalle_id INT PRIMARY KEY IDENTITY(1,1),
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    -- Campo calculado en SQL Server
    subtotal AS (cantidad * precio_unitario) PERSISTED, 
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

CREATE TABLE Recetas (
    receta_id INT PRIMARY KEY IDENTITY(1,1),
    producto_id INT NOT NULL UNIQUE,
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

CREATE TABLE Detalle_Receta (
    receta_detalle_id INT PRIMARY KEY IDENTITY(1,1),
    receta_id INT NOT NULL,
    ingrediente_id INT NOT NULL,
    cantidad_requerida DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (receta_id) REFERENCES Recetas(receta_id),
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(ingrediente_id)
);

CREATE TABLE LOG_AUDITORIA (
    log_id INT PRIMARY KEY IDENTITY(1,1),
    tabla_afectada VARCHAR(50) NOT NULL,
    operacion VARCHAR(20) NOT NULL,
    usuario VARCHAR(50) DEFAULT SUSER_SNAME(), -- Función de usuario en MS SQL
    fecha_hora DATETIME DEFAULT GETDATE(),
    descripcion NVARCHAR(MAX)
);

-- 2. INSERCIÓN DE DATOS DE MUESTRA
-------------------------------------------------------------------------------------------------

SET IDENTITY_INSERT Empleados OFF; -- Se asume que no necesitas insertar IDs específicos
INSERT INTO Empleados (nombre, apellido, cargo, fecha_contratacion, salario) VALUES
('Ana', 'Gomez', 'Barista Senior', '2023-01-15', 2500.00), ('Carlos', 'Diaz', 'Cajero', '2023-03-20', 2000.00),
('Elena', 'Ruiz', 'Gerente', '2022-10-01', 3500.00), ('Beto', 'Lopez', 'Barista Junior', '2024-05-10', 1800.00),
('Marta', 'Perez', 'Ayudante', '2023-08-01', 1900.00), ('Jorge', 'Soto', 'Cajero', '2024-01-10', 2100.00),
('Luisa', 'Mora', 'Barista Senior', '2022-11-20', 2600.00), ('David', 'Vargas', 'Ayudante', '2024-03-01', 1850.00),
('Sofia', 'Castro', 'Barista Junior', '2024-06-15', 1750.00), ('Raul', 'Nuñez', 'Cajero', '2023-04-05', 2050.00);

SET IDENTITY_INSERT Productos OFF;
INSERT INTO Productos (nombre, descripcion, precio, tipo_producto) VALUES
('Espresso', 'Shot de café concentrado.', 2.50, 'Bebida'), ('Latte Vainilla', 'Espresso con leche y sirope de vainilla.', 4.00, 'Bebida'),
('Muffin Choco', 'Muffin de chocolate casero.', 3.50, 'Comida'), ('Croissant', 'Croissant de mantequilla.', 2.00, 'Comida'),
('Capuchino', 'Café con leche espumada.', 3.80, 'Bebida'), ('Jugo Naranja', 'Jugo de naranja natural.', 3.00, 'Bebida'),
('Brownie', 'Brownie de nueces.', 4.50, 'Comida'), ('Té Verde', 'Té verde premium.', 2.80, 'Bebida'),
('Sándwich Pavo', 'Sándwich de pavo y queso.', 6.00, 'Comida'), ('Donut Glaseado', 'Donut con glaseado de azúcar.', 2.50, 'Comida');

SET IDENTITY_INSERT Ingredientes OFF;
INSERT INTO Ingredientes (nombre_ingrediente, unidad_medida, stock_actual, stock_minimo) VALUES
('Grano Café', 'gramos', 50000.00, 10000.00), ('Leche Entera', 'ml', 30000.00, 5000.00),
('Sirope Vainilla', 'ml', 5000.00, 1000.00), ('Harina', 'gramos', 20000.00, 5000.00),
('Huevos', 'unidad', 300.00, 50.00), ('Azúcar', 'gramos', 10000.00, 2000.00),
('Naranja', 'unidad', 150.00, 30.00), ('Chocolate', 'gramos', 8000.00, 1500.00),
('Pavo Lonchas', 'gramos', 4000.00, 500.00), ('Queso', 'gramos', 5000.00, 800.00);

SET IDENTITY_INSERT Pedidos OFF;
INSERT INTO Pedidos (fecha_hora, empleado_id, estado, total_pedido) VALUES
('2025-10-25 10:00:00', 1, 'Entregado', 8.00), ('2025-10-25 10:05:00', 2, 'Entregado', 10.50),
('2025-10-25 10:15:00', 1, 'Entregado', 12.00), ('2025-10-26 11:30:00', 1, 'Entregado', 6.00),
('2025-10-26 11:45:00', 3, 'Entregado', 7.30), ('2025-10-27 12:00:00', 2, 'Entregado', 15.00),
('2025-10-27 12:30:00', 4, 'Preparando', 9.50), ('2025-10-27 12:45:00', 1, 'Entregado', 8.30),
('2025-10-28 09:10:00', 5, 'Entregado', 11.00), ('2025-10-28 09:20:00', 6, 'Entregado', 4.50),
('2025-10-28 09:40:00', 7, 'Entregado', 18.00), ('2025-10-29 13:00:00', 8, 'Entregado', 7.50),
('2025-10-29 13:15:00', 9, 'Pendiente', 4.00), ('2025-10-29 13:30:00', 10, 'Entregado', 10.00),
('2025-10-30 14:00:00', 1, 'Entregado', 8.00), ('2025-10-30 14:15:00', 2, 'Entregado', 12.00);

SET IDENTITY_INSERT Detalle_Pedido OFF;
INSERT INTO Detalle_Pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 2, 2.50), (1, 4, 1, 2.00), (2, 2, 2, 4.00), (2, 6, 1, 2.50), (3, 3, 2, 3.50), (3, 5, 1, 4.00),
(4, 1, 1, 2.50), (4, 9, 1, 6.00), (5, 7, 1, 4.50), (5, 8, 1, 2.80), (6, 10, 3, 2.50), (6, 4, 2, 2.00),
(6, 5, 1, 3.50), (7, 2, 1, 4.00), (7, 3, 1, 3.50), (7, 10, 1, 2.00), (8, 1, 2, 2.50), (8, 6, 1, 3.30),
(9, 3, 2, 3.50), (9, 7, 1, 4.00), (10, 1, 1, 2.50), (10, 4, 1, 2.00), (11, 2, 3, 4.00), (11, 3, 2, 3.00),
(12, 5, 2, 3.75), (13, 2, 1, 4.00), (14, 1, 4, 2.50), (15, 7, 1, 4.00), (15, 8, 1, 4.00), (16, 9, 2, 6.00);

-- 3. PROCEDIMIENTOS ALMACENADOS (T-SQL)
-------------------------------------------------------------------------------------------------

GO
-- INSERT (C)
CREATE PROCEDURE SP_InsertarProducto (
    @p_nombre VARCHAR(100),
    @p_descripcion NVARCHAR(MAX),
    @p_precio DECIMAL(10, 2),
    @p_tipo_producto VARCHAR(50)
)
AS
BEGIN
    INSERT INTO Productos (nombre, descripcion, precio, tipo_producto)
    VALUES (@p_nombre, @p_descripcion, @p_precio, @p_tipo_producto);
END;
GO

-- SELECT (R)
CREATE PROCEDURE SP_ObtenerProductosPorTipo (
    @p_tipo VARCHAR(50)
)
AS
BEGIN
    SELECT producto_id, nombre, precio
    FROM Productos
    WHERE tipo_producto = @p_tipo;
END;
GO

-- UPDATE (U)
CREATE PROCEDURE SP_ActualizarPrecioProducto (
    @p_id INT,
    @p_nuevo_precio DECIMAL(10, 2)
)
AS
BEGIN
    UPDATE Productos
    SET precio = @p_nuevo_precio
    WHERE producto_id = @p_id;
END;
GO

-- DELETE (D)
CREATE PROCEDURE SP_EliminarProducto (
    @p_id INT
)
AS
BEGIN
    DELETE FROM Productos
    WHERE producto_id = @p_id;
END;
GO

-- PROCEDIMIENTO COMPUESTO (Maestra y Detalle)
CREATE PROCEDURE SP_ObtenerDetallesPedido (
    @p_pedido_id INT
)
AS
BEGIN
    -- Resultado 1: Datos del Pedido (Maestra)
    SELECT
        p.pedido_id,
        p.fecha_hora,
        e.nombre,
        p.estado,
        p.total_pedido
    FROM Pedidos p
    INNER JOIN Empleados e ON p.empleado_id = e.empleado_id
    WHERE p.pedido_id = @p_pedido_id;

    -- Resultado 2: Detalles de los productos en el pedido (Detalle)
    SELECT
        dp.cantidad,
        pr.nombre AS producto_nombre,
        dp.precio_unitario,
        dp.subtotal
    FROM Detalle_Pedido dp
    INNER JOIN Productos pr ON dp.producto_id = pr.producto_id
    WHERE dp.pedido_id = @p_pedido_id;
END;
GO

-- 4. VISTAS (T-SQL)
-------------------------------------------------------------------------------------------------

CREATE VIEW Vista_StockMinimo AS
SELECT nombre_ingrediente, stock_actual, stock_minimo FROM Ingredientes WHERE stock_actual <= stock_minimo;
GO

CREATE VIEW Vista_VentasPorEmpleado AS
SELECT e.nombre AS empleado_nombre, e.apellido AS empleado_apellido, e.cargo, COUNT(p.pedido_id) AS total_pedidos, SUM(p.total_pedido) AS total_vendido
FROM Empleados e JOIN Pedidos p ON e.empleado_id = p.empleado_id WHERE p.estado = 'Entregado'
GROUP BY e.empleado_id, e.nombre, e.apellido, e.cargo;
GO

CREATE VIEW Vista_DetalleVentasProductos AS
SELECT pr.nombre AS producto, pr.tipo_producto, SUM(dp.cantidad) AS unidades_vendidas, SUM(dp.subtotal) AS ingresos_totales
FROM Detalle_Pedido dp JOIN Productos pr ON dp.producto_id = pr.producto_id
GROUP BY pr.producto_id, pr.nombre, pr.tipo_producto;
GO

CREATE VIEW Vista_RecetaCompleta AS
SELECT p.nombre AS producto, i.nombre_ingrediente, dr.cantidad_requerida, i.unidad_medida
FROM Productos p JOIN Recetas r ON p.producto_id = r.producto_id
JOIN Detalle_Receta dr ON r.receta_id = dr.receta_id JOIN Ingredientes i ON dr.ingrediente_id = i.ingrediente_id;
GO

CREATE VIEW Vista_RankingPedidosDiarios AS
SELECT CAST(fecha_hora AS DATE) AS dia, pedido_id, total_pedido, RANK() OVER (PARTITION BY CAST(fecha_hora AS DATE) ORDER BY total_pedido DESC) AS rank_venta
FROM Pedidos WHERE estado = 'Entregado';
GO

-- 5. CONSULTAS AVANZADAS (T-SQL)
-------------------------------------------------------------------------------------------------

-- Consulta Avanzada 1: Uso de CTE y Función de Ventana (Acumulados)
WITH VentasDiarias AS (
    SELECT CAST(fecha_hora AS DATE) AS dia, SUM(total_pedido) AS venta_diaria
    FROM Pedidos WHERE estado = 'Entregado' GROUP BY CAST(fecha_hora AS DATE)
)
SELECT dia, venta_diaria, SUM(venta_diaria) OVER (ORDER BY dia) AS total_acumulado FROM VentasDiarias
ORDER BY dia;
GO

-- Consulta Avanzada 2: Subconsulta Correlacionada en WHERE y Escalar en HAVING
SELECT p1.nombre, p1.tipo_producto, p1.precio
FROM Productos p1
WHERE p1.precio > (
    -- Subconsulta Correlacionada en WHERE
    SELECT AVG(p2.precio) FROM Productos p2 WHERE p2.tipo_producto = p1.tipo_producto
)
GROUP BY p1.nombre, p1.tipo_producto, p1.precio
HAVING p1.precio > (
    -- Subconsulta Escalar en HAVING
    SELECT AVG(precio) FROM Productos
)
ORDER BY p1.precio DESC;
GO

-- 6. TRIGGERS (T-SQL)
-------------------------------------------------------------------------------------------------

-- TRIGGER 1: Auditoría (AFTER UPDATE)
CREATE TRIGGER TR_Auditoria_Productos_Precio
ON Productos
AFTER UPDATE
AS
BEGIN
    IF UPDATE(precio)
    BEGIN
        INSERT INTO LOG_AUDITORIA (tabla_afectada, operacion, usuario, descripcion)
        SELECT 
            'Productos', 
            'UPDATE', 
            SUSER_SNAME(), 
            'Precio actualizado de ' + CAST(d.precio AS VARCHAR) + ' a ' + CAST(i.precio AS VARCHAR) + ' para producto_id ' + CAST(i.producto_id AS VARCHAR)
        FROM deleted d JOIN inserted i ON d.producto_id = i.producto_id
        WHERE d.precio <> i.precio;
    END
END;
GO

-- TRIGGER 2: Lógica de Negocio (AFTER INSERT) - Actualiza el total del pedido
CREATE TRIGGER TR_ActualizarTotalPedido
ON Detalle_Pedido
AFTER INSERT
AS
BEGIN
    UPDATE P
    SET P.total_pedido = (
        SELECT SUM(subtotal)
        FROM Detalle_Pedido dp
        WHERE dp.pedido_id = I.pedido_id
    )
    FROM Pedidos P
    INNER JOIN inserted I ON P.pedido_id = I.pedido_id;
END;
GO