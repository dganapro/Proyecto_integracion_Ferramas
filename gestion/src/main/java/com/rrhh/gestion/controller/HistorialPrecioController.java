package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.HistorialPrecio;
import com.rrhh.gestion.repository.HistorialPrecioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/historial-precios")
@CrossOrigin(origins = "*")
public class HistorialPrecioController {
    
    @Autowired
    private HistorialPrecioRepository historialPrecioRepository;
    
    @GetMapping
    public List<HistorialPrecio> obtenerTodoElHistorialPrecios() {
        return historialPrecioRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<HistorialPrecio> obtenerHistorialPrecioPorId(@PathVariable Long id) {
        Optional<HistorialPrecio> historialPrecio = historialPrecioRepository.findById(id);
        return historialPrecio.map(h -> ResponseEntity.ok().body(h))
                             .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<HistorialPrecio> crearHistorialPrecio(@RequestBody HistorialPrecio historialPrecio) {
        HistorialPrecio nuevoHistorialPrecio = historialPrecioRepository.save(historialPrecio);
        return new ResponseEntity<>(nuevoHistorialPrecio, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<HistorialPrecio> actualizarHistorialPrecio(@PathVariable Long id, @RequestBody HistorialPrecio historialPrecioActualizado) {
        Optional<HistorialPrecio> historialPrecioExistente = historialPrecioRepository.findById(id);
        if (historialPrecioExistente.isPresent()) {
            historialPrecioActualizado.setId(id);
            return ResponseEntity.ok(historialPrecioRepository.save(historialPrecioActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarHistorialPrecio(@PathVariable Long id) {
        if (historialPrecioRepository.existsById(id)) {
            historialPrecioRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
