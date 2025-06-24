package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Venta;
import com.rrhh.gestion.repository.VentaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/ventas")
@CrossOrigin(origins = "*")
public class VentaController {
    
    @Autowired
    private VentaRepository ventaRepository;
    
    @GetMapping
    public List<Venta> obtenerTodasLasVentas() {
        return ventaRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Venta> obtenerVentaPorId(@PathVariable Long id) {
        Optional<Venta> venta = ventaRepository.findById(id);
        return venta.map(v -> ResponseEntity.ok().body(v))
                   .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Venta> crearVenta(@RequestBody Venta venta) {
        Venta nuevaVenta = ventaRepository.save(venta);
        return new ResponseEntity<>(nuevaVenta, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Venta> actualizarVenta(@PathVariable Long id, @RequestBody Venta ventaActualizada) {
        Optional<Venta> ventaExistente = ventaRepository.findById(id);
        if (ventaExistente.isPresent()) {
            ventaActualizada.setId(id);
            return ResponseEntity.ok(ventaRepository.save(ventaActualizada));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarVenta(@PathVariable Long id) {
        if (ventaRepository.existsById(id)) {
            ventaRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
