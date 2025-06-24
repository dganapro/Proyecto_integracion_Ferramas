package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Asignacion;
import com.rrhh.gestion.repository.AsignacionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/asignaciones")
@CrossOrigin(origins = "*")
public class AsignacionController {
    
    @Autowired
    private AsignacionRepository asignacionRepository;
    
    @GetMapping
    public List<Asignacion> obtenerTodasLasAsignaciones() {
        return asignacionRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Asignacion> obtenerAsignacionPorId(@PathVariable Long id) {
        Optional<Asignacion> asignacion = asignacionRepository.findById(id);
        return asignacion.map(a -> ResponseEntity.ok().body(a))
                        .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Asignacion> crearAsignacion(@RequestBody Asignacion asignacion) {
        Asignacion nuevaAsignacion = asignacionRepository.save(asignacion);
        return new ResponseEntity<>(nuevaAsignacion, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Asignacion> actualizarAsignacion(@PathVariable Long id, @RequestBody Asignacion asignacionActualizada) {
        Optional<Asignacion> asignacionExistente = asignacionRepository.findById(id);
        if (asignacionExistente.isPresent()) {
            asignacionActualizada.setId(id);
            return ResponseEntity.ok(asignacionRepository.save(asignacionActualizada));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarAsignacion(@PathVariable Long id) {
        if (asignacionRepository.existsById(id)) {
            asignacionRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
