package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Carrito;
import com.rrhh.gestion.repository.CarritoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/carritos")
@CrossOrigin(origins = "*")
public class CarritoController {
    
    @Autowired
    private CarritoRepository carritoRepository;
    
    @GetMapping
    public List<Carrito> obtenerTodosLosCarritos() {
        return carritoRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Carrito> obtenerCarritoPorId(@PathVariable Long id) {
        Optional<Carrito> carrito = carritoRepository.findById(id);
        return carrito.map(c -> ResponseEntity.ok().body(c))
                     .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Carrito> crearCarrito(@RequestBody Carrito carrito) {
        Carrito nuevoCarrito = carritoRepository.save(carrito);
        return new ResponseEntity<>(nuevoCarrito, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Carrito> actualizarCarrito(@PathVariable Long id, @RequestBody Carrito carritoActualizado) {
        Optional<Carrito> carritoExistente = carritoRepository.findById(id);
        if (carritoExistente.isPresent()) {
            carritoActualizado.setId(id);
            return ResponseEntity.ok(carritoRepository.save(carritoActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarCarrito(@PathVariable Long id) {
        if (carritoRepository.existsById(id)) {
            carritoRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
