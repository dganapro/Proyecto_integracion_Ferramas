package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.MetodoPago;
import com.rrhh.gestion.repository.MetodoPagoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/metodos-pago")
@CrossOrigin(origins = "*")
public class MetodoPagoController {
    
    @Autowired
    private MetodoPagoRepository metodoPagoRepository;
    
    @GetMapping
    public List<MetodoPago> obtenerTodosLosMetodosPago() {
        return metodoPagoRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<MetodoPago> obtenerMetodoPagoPorId(@PathVariable Long id) {
        Optional<MetodoPago> metodoPago = metodoPagoRepository.findById(id);
        return metodoPago.map(m -> ResponseEntity.ok().body(m))
                        .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<MetodoPago> crearMetodoPago(@RequestBody MetodoPago metodoPago) {
        MetodoPago nuevoMetodoPago = metodoPagoRepository.save(metodoPago);
        return new ResponseEntity<>(nuevoMetodoPago, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<MetodoPago> actualizarMetodoPago(@PathVariable Long id, @RequestBody MetodoPago metodoPagoActualizado) {
        Optional<MetodoPago> metodoPagoExistente = metodoPagoRepository.findById(id);
        if (metodoPagoExistente.isPresent()) {
            metodoPagoActualizado.setId(id);
            return ResponseEntity.ok(metodoPagoRepository.save(metodoPagoActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarMetodoPago(@PathVariable Long id) {
        if (metodoPagoRepository.existsById(id)) {
            metodoPagoRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
