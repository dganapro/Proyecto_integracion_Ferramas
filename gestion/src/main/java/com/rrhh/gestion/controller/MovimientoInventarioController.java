package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.MovimientoInventario;
import com.rrhh.gestion.repository.MovimientoInventarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/movimientos-inventario")
@CrossOrigin(origins = "*")
public class MovimientoInventarioController {
    
    @Autowired
    private MovimientoInventarioRepository movimientoInventarioRepository;
    
    @GetMapping
    public List<MovimientoInventario> obtenerTodosLosMovimientosInventario() {
        return movimientoInventarioRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<MovimientoInventario> obtenerMovimientoInventarioPorId(@PathVariable Long id) {
        Optional<MovimientoInventario> movimientoInventario = movimientoInventarioRepository.findById(id);
        return movimientoInventario.map(m -> ResponseEntity.ok().body(m))
                                  .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<MovimientoInventario> crearMovimientoInventario(@RequestBody MovimientoInventario movimientoInventario) {
        MovimientoInventario nuevoMovimientoInventario = movimientoInventarioRepository.save(movimientoInventario);
        return new ResponseEntity<>(nuevoMovimientoInventario, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<MovimientoInventario> actualizarMovimientoInventario(@PathVariable Long id, @RequestBody MovimientoInventario movimientoInventarioActualizado) {
        Optional<MovimientoInventario> movimientoInventarioExistente = movimientoInventarioRepository.findById(id);
        if (movimientoInventarioExistente.isPresent()) {
            movimientoInventarioActualizado.setId(id);
            return ResponseEntity.ok(movimientoInventarioRepository.save(movimientoInventarioActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarMovimientoInventario(@PathVariable Long id) {
        if (movimientoInventarioRepository.existsById(id)) {
            movimientoInventarioRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
