package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "asignaciones")
public class Asignacion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "tarea_id")
    private Tarea tarea;
    
    @ManyToOne
    @JoinColumn(name = "empleado_id")
    private Empleado empleado;
    
    @Column(name = "fecha_asignacion")
    private LocalDate fechaAsignacion;

    // Constructores
    public Asignacion() {}

    public Asignacion(Tarea tarea, Empleado empleado, LocalDate fechaAsignacion) {
        this.tarea = tarea;
        this.empleado = empleado;
        this.fechaAsignacion = fechaAsignacion;
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Tarea getTarea() { return tarea; }
    public void setTarea(Tarea tarea) { this.tarea = tarea; }
    
    public Empleado getEmpleado() { return empleado; }
    public void setEmpleado(Empleado empleado) { this.empleado = empleado; }
    
    public LocalDate getFechaAsignacion() { return fechaAsignacion; }
    public void setFechaAsignacion(LocalDate fechaAsignacion) { this.fechaAsignacion = fechaAsignacion; }
}
