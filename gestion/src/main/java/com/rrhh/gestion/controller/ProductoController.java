package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Producto;
import com.rrhh.gestion.repository.ProductoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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
        Producto nuevoProducto = productoRepository.save(producto);
        return new ResponseEntity<>(nuevoProducto, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Producto> actualizarProducto(@PathVariable Long id, @RequestBody Producto productoActualizado) {
        Optional<Producto> productoExistente = productoRepository.findById(id);
        if (productoExistente.isPresent()) {
            productoActualizado.setId(id);
            return ResponseEntity.ok(productoRepository.save(productoActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarProducto(@PathVariable Long id) {
        if (productoRepository.existsById(id)) {
            productoRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
