package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Comuna;
import com.rrhh.gestion.repository.ComunaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
@RestController
@RequestMapping("/api/comunas/")
public class ComunaController {
    @Autowired
    private ComunaRepository comunaRepository;
    @GetMapping
    public List<Comuna> leerComunas() {
        return comunaRepository.findAll();
    }

    @PostMapping("/comuna")
    public Comuna crearComuna(@RequestBody Comuna comuna) {
        return comunaRepository.save(comuna);
    }

}
