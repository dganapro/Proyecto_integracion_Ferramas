package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.ItemCarrito;
import com.rrhh.gestion.repository.ItemCarritoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/items-carrito")
@CrossOrigin(origins = "*")
public class ItemCarritoController {
    
    @Autowired
    private ItemCarritoRepository itemCarritoRepository;
    
    @GetMapping
    public List<ItemCarrito> obtenerTodosLosItemsCarrito() {
        return itemCarritoRepository.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<ItemCarrito> obtenerItemCarritoPorId(@PathVariable Long id) {
        Optional<ItemCarrito> itemCarrito = itemCarritoRepository.findById(id);
        return itemCarrito.map(i -> ResponseEntity.ok().body(i))
                         .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<ItemCarrito> crearItemCarrito(@RequestBody ItemCarrito itemCarrito) {
        ItemCarrito nuevoItemCarrito = itemCarritoRepository.save(itemCarrito);
        return new ResponseEntity<>(nuevoItemCarrito, HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<ItemCarrito> actualizarItemCarrito(@PathVariable Long id, @RequestBody ItemCarrito itemCarritoActualizado) {
        Optional<ItemCarrito> itemCarritoExistente = itemCarritoRepository.findById(id);
        if (itemCarritoExistente.isPresent()) {
            itemCarritoActualizado.setId(id);
            return ResponseEntity.ok(itemCarritoRepository.save(itemCarritoActualizado));
        }
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarItemCarrito(@PathVariable Long id) {
        if (itemCarritoRepository.existsById(id)) {
            itemCarritoRepository.deleteById(id);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
}
