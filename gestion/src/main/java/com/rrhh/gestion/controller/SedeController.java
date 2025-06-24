package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Sede;
import com.rrhh.gestion.repository.SedeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/sedes")
@CrossOrigin(origins = "*")
public class SedeController {
    
    @Autowired
    private SedeRepository sedeRepository;
    
    @GetMapping
    public List<Sede> obtenerTodasLasSedes() {
        return sedeRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Sede> obtenerSedePorId(@PathVariable Long id) {
        Optional<Sede> sede = sedeRepository.findById(id);
        return sede.map(s -> ResponseEntity.ok().body(s))
                  .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Sede> crearSede(@RequestBody Sede sede) {
        Sede nuevaSede = sedeRepository.save(sede);
        return new ResponseEntity<>(nuevaSede, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Sede> actualizarSede(@PathVariable Long id, @RequestBody Sede sedeActualizada) {
        Optional<Sede> sedeExistente = sedeRepository.findById(id);
        if (sedeExistente.isPresent()) {
            sedeActualizada.setId(id);
            return ResponseEntity.ok(sedeRepository.save(sedeActualizada));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarSede(@PathVariable Long id) {
        if (sedeRepository.existsById(id)) {
            sedeRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
