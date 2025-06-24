package com.rrhh.gestion.controller;

import com.rrhh.gestion.entity.Empleado;
import com.rrhh.gestion.repository.EmpleadoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import com.rrhh.gestion.dto.EmpleadoDTO;
@RestController
@RequestMapping("/api/empleados/")
public class EmpleadoController {
    @Autowired
    private EmpleadoRepository empleadoRepository;
    @GetMapping
    public List<Empleado> leerEmpleados() {
        return empleadoRepository.findAll();
    }

    @GetMapping("/comuna/")
    public List<EmpleadoDTO> leerEmpleadosDTO() {
        List<Empleado> empleados=empleadoRepository.findAll();
        List<EmpleadoDTO> empleadosDTO = new ArrayList<>();
        for (Empleado emp : empleados) {
            empleadosDTO.add(new EmpleadoDTO(emp.getRut(), emp.getNombre(), emp.getTelefono(), emp.getCorreo(),
                    emp.getComuna().getNombre()));
        }
        return empleadosDTO;
    }

    @PostMapping
    public ResponseEntity<Empleado> crearEmpleado(@RequestBody Empleado empleado) {
        Empleado nuevo=empleadoRepository.save(empleado);
        return new ResponseEntity<>(nuevo, HttpStatus.CREATED);
    }

}
