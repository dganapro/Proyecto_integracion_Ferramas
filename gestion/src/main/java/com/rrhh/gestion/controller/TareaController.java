package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Tarea;
import com.rrhh.gestion.repository.TareaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/tareas")
@CrossOrigin(origins = "*")
public class TareaController {
    
    @Autowired
    private TareaRepository tareaRepository;
    
    @GetMapping
    public List<Tarea> obtenerTodasLasTareas() {
        return tareaRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Tarea> obtenerTareaPorId(@PathVariable Long id) {
        Optional<Tarea> tarea = tareaRepository.findById(id);
        return tarea.map(t -> ResponseEntity.ok().body(t))
                   .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Tarea> crearTarea(@RequestBody Tarea tarea) {
        Tarea nuevaTarea = tareaRepository.save(tarea);
        return new ResponseEntity<>(nuevaTarea, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Tarea> actualizarTarea(@PathVariable Long id, @RequestBody Tarea tareaActualizada) {
        Optional<Tarea> tareaExistente = tareaRepository.findById(id);
        if (tareaExistente.isPresent()) {
            tareaActualizada.setId(id);
            return ResponseEntity.ok(tareaRepository.save(tareaActualizada));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarTarea(@PathVariable Long id) {
        if (tareaRepository.existsById(id)) {
            tareaRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
