package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Envio;
import com.rrhh.gestion.repository.EnvioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/envios")
@CrossOrigin(origins = "*")
public class EnvioController {
    
    @Autowired
    private EnvioRepository envioRepository;
    
    @GetMapping
    public List<Envio> obtenerTodosLosEnvios() {
        return envioRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Envio> obtenerEnvioPorId(@PathVariable Long id) {
        Optional<Envio> envio = envioRepository.findById(id);
        return envio.map(e -> ResponseEntity.ok().body(e))
                   .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Envio> crearEnvio(@RequestBody Envio envio) {
        Envio nuevoEnvio = envioRepository.save(envio);
        return new ResponseEntity<>(nuevoEnvio, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Envio> actualizarEnvio(@PathVariable Long id, @RequestBody Envio envioActualizado) {
        Optional<Envio> envioExistente = envioRepository.findById(id);
        if (envioExistente.isPresent()) {
            envioActualizado.setId(id);
            return ResponseEntity.ok(envioRepository.save(envioActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarEnvio(@PathVariable Long id) {
        if (envioRepository.existsById(id)) {
            envioRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
