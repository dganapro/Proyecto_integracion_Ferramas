package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.DetalleVenta;
import com.rrhh.gestion.repository.DetalleVentaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/detalles-venta")
@CrossOrigin(origins = "*")
public class DetalleVentaController {
    
    @Autowired
    private DetalleVentaRepository detalleVentaRepository;
    
    @GetMapping
    public List<DetalleVenta> obtenerTodosLosDetallesVenta() {
        return detalleVentaRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<DetalleVenta> obtenerDetalleVentaPorId(@PathVariable Long id) {
        Optional<DetalleVenta> detalleVenta = detalleVentaRepository.findById(id);
        return detalleVenta.map(d -> ResponseEntity.ok().body(d))
                          .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<DetalleVenta> crearDetalleVenta(@RequestBody DetalleVenta detalleVenta) {
        DetalleVenta nuevoDetalleVenta = detalleVentaRepository.save(detalleVenta);
        return new ResponseEntity<>(nuevoDetalleVenta, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<DetalleVenta> actualizarDetalleVenta(@PathVariable Long id, @RequestBody DetalleVenta detalleVentaActualizado) {
        Optional<DetalleVenta> detalleVentaExistente = detalleVentaRepository.findById(id);
        if (detalleVentaExistente.isPresent()) {
            detalleVentaActualizado.setId(id);
            return ResponseEntity.ok(detalleVentaRepository.save(detalleVentaActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarDetalleVenta(@PathVariable Long id) {
        if (detalleVentaRepository.existsById(id)) {
            detalleVentaRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
