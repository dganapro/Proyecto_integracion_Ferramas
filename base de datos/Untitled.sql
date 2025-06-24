create database rrhh;
create user "jefe"@"%" identified by "123";
grant all privileges on rrhh.* to "jefe"@"%";
flush privileges;

use rrhh;

CREATE TABLE `tareas` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `nombre` text NOT NULL,
  `descripcion` text,
  `fecha_inicio` date,
  `fecha_fin` date,
  `estado` text
);

CREATE TABLE `empleados` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `nombre` text NOT NULL,
  `apellido` text NOT NULL,
  `correo_electronico` text UNIQUE,
  `telefono` text
);

CREATE TABLE `asignaciones` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `tarea_id` bigint,
  `empleado_id` bigint,
  `fecha_asignacion` date
);

CREATE TABLE `productos` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `nombre` text NOT NULL,
  `descripcion` text,
  `precio` numeric(10,2) NOT NULL,
  `stock` int NOT NULL,
  `categoria` text
);

CREATE TABLE `sedes` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `nombre` text NOT NULL,
  `direccion` text NOT NULL,
  `telefono` text
);

CREATE TABLE `clientes` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `nombre` text NOT NULL,
  `apellido` text NOT NULL,
  `correo_electronico` text UNIQUE,
  `telefono` text,
  `direccion` text
);

CREATE TABLE `ventas` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `cliente_id` bigint,
  `sede_id` bigint,
  `fecha` date NOT NULL,
  `total` numeric(10,2) NOT NULL,
  `empleado_id` bigint,
  `metodo_pago_id` bigint
);

CREATE TABLE `detalles_venta` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `venta_id` bigint,
  `producto_id` bigint,
  `cantidad` int NOT NULL,
  `precio_unitario` numeric(10,2) NOT NULL
);

CREATE TABLE `envios` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `venta_id` bigint,
  `fecha_envio` date,
  `fecha_entrega` date,
  `estado` text
);

CREATE TABLE `metodos_pago` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `nombre` text NOT NULL
);

CREATE TABLE `carritos` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `cliente_id` bigint,
  `fecha_creacion` date DEFAULT (current_date)
);

CREATE TABLE `items_carrito` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `carrito_id` bigint,
  `producto_id` bigint,
  `cantidad` int NOT NULL
);

CREATE TABLE `historial_precios` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `producto_id` bigint,
  `precio` numeric(10,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date
);

CREATE TABLE `movimientos_inventario` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `producto_id` bigint,
  `cantidad` int NOT NULL,
  `tipo_movimiento` text NOT NULL,
  `fecha` date DEFAULT (current_date)
);

CREATE UNIQUE INDEX `unique_apellido` ON `empleados` (`apellido`);

ALTER TABLE `asignaciones` ADD FOREIGN KEY (`tarea_id`) REFERENCES `tareas` (`id`);

ALTER TABLE `asignaciones` ADD FOREIGN KEY (`empleado_id`) REFERENCES `empleados` (`id`);

ALTER TABLE `ventas` ADD FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`);

ALTER TABLE `ventas` ADD FOREIGN KEY (`sede_id`) REFERENCES `sedes` (`id`);

ALTER TABLE `ventas` ADD FOREIGN KEY (`empleado_id`) REFERENCES `empleados` (`id`);

ALTER TABLE `ventas` ADD FOREIGN KEY (`metodo_pago_id`) REFERENCES `metodos_pago` (`id`);

ALTER TABLE `detalles_venta` ADD FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`);

ALTER TABLE `detalles_venta` ADD FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

ALTER TABLE `envios` ADD FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`);

ALTER TABLE `carritos` ADD FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`);

ALTER TABLE `items_carrito` ADD FOREIGN KEY (`carrito_id`) REFERENCES `carritos` (`id`);

ALTER TABLE `items_carrito` ADD FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

ALTER TABLE `historial_precios` ADD FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

ALTER TABLE `movimientos_inventario` ADD FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);
