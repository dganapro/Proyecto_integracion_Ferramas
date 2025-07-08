package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Producto;
import com.rrhh.gestion.repository.ProductoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/productos")
@CrossOrigin(origins = "*")
public class ProductoController {
    
    @Autowired
    private ProductoRepository productoRepository;
    
    @GetMapping
    public List<Producto> obtenerTodosLosProductos() {
        return productoRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Producto> obtenerProductoPorId(@PathVariable Long id) {
        Optional<Producto> producto = productoRepository.findById(id);
        return producto.map(p -> ResponseEntity.ok().body(p))
                      .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Producto> crearProducto(@RequestBody Producto producto) {
        try {
            // Validar datos obligatorios
            if (producto.getCodigo() == null || producto.getNombre() == null) {
                return ResponseEntity.badRequest().build();
            }
            
            // Establecer valores por defecto si no están presentes
            if (producto.getEstado() == null) {
                producto.setEstado(Producto.EstadoProducto.ACTIVO);
            }
            if (producto.getStockMinimo() == null) {
                producto.setStockMinimo(5);
            }
            if (producto.getFechaCreacion() == null) {
                producto.setFechaCreacion(LocalDateTime.now());
            }
            if (producto.getFechaActualizacion() == null) {
                producto.setFechaActualizacion(LocalDateTime.now());
            }
            
            Producto nuevoProducto = productoRepository.save(producto);
            return new ResponseEntity<>(nuevoProducto, HttpStatus.CREATED);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Producto> actualizarProducto(@PathVariable Long id, @RequestBody Producto producto) {
        try {
            Optional<Producto> productoExistente = productoRepository.findById(id);
            if (productoExistente.isPresent()) {
                Producto p = productoExistente.get();
                
                // Actualizar campos
                if (producto.getCodigo() != null) p.setCodigo(producto.getCodigo());
                if (producto.getNombre() != null) p.setNombre(producto.getNombre());
                if (producto.getDescripcion() != null) p.setDescripcion(producto.getDescripcion());
                if (producto.getPrecioVenta() != null) p.setPrecioVenta(producto.getPrecioVenta());
                if (producto.getPrecioCompra() != null) p.setPrecioCompra(producto.getPrecioCompra());
                if (producto.getStockActual() != null) p.setStockActual(producto.getStockActual());
                if (producto.getStockMinimo() != null) p.setStockMinimo(producto.getStockMinimo());
                if (producto.getMarca() != null) p.setMarca(producto.getMarca());
                if (producto.getEstado() != null) p.setEstado(producto.getEstado());
                if (producto.getUnidadMedida() != null) p.setUnidadMedida(producto.getUnidadMedida());
                
                p.setFechaActualizacion(LocalDateTime.now());
                
                Producto productoActualizado = productoRepository.save(p);
                return ResponseEntity.ok(productoActualizado);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarProducto(@PathVariable Long id) {
        try {
            if (productoRepository.existsById(id)) {
                productoRepository.deleteById(id);
                return ResponseEntity.ok().build();
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }
    }
}
