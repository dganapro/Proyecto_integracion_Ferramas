package com.rrhh.gestion.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name="comuna")
public class Comuna {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    
    @Column(nullable = false, length = 100)
    @NotBlank(message = "El nombre de la comuna es obligatorio")
    private String nombre;
    
    @Column(length = 100)
    private String region;
    
    @Column(length = 10)
    private String codigoPostal;

    @OneToMany(mappedBy="comuna", cascade=CascadeType.ALL, orphanRemoval = true)
    @JsonIgnore
    private List<Empleado> empleados;

    // Constructores
    public Comuna() {
        this.empleados = new ArrayList<>();
    }

    public Comuna(int id, String nombre) {
        this.id = id;
        this.nombre = nombre;
        this.empleados = new ArrayList<>();
    }
    
    public Comuna(String nombre, String region) {
        this.nombre = nombre;
        this.region = region;
        this.empleados = new ArrayList<>();
    }

    // Métodos de utilidad
    public void addEmpleado(Empleado empleado) {
        empleados.add(empleado);
        empleado.setComuna(this);
    }
    
    public void removeEmpleado(Empleado empleado) {
        empleados.remove(empleado);
        empleado.setComuna(null);
    }
    
    public int getCantidadEmpleados() {
        return empleados != null ? empleados.size() : 0;
    }

    // Getters y Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    
    public String getRegion() {
        return region;
    }
    
    public void setRegion(String region) {
        this.region = region;
    }
    
    public String getCodigoPostal() {
        return codigoPostal;
    }
    
    public void setCodigoPostal(String codigoPostal) {
        this.codigoPostal = codigoPostal;
    }

    public List<Empleado> getEmpleados() {
        return empleados;
    }

    public void setEmpleados(List<Empleado> empleados) {
        this.empleados = empleados;
    }
    
    @Override
    public String toString() {
        return "Comuna{" +
                "id=" + id +
                ", nombre='" + nombre + '\'' +
                ", region='" + region + '\'' +
                ", codigoPostal='" + codigoPostal + '\'' +
                ", cantidadEmpleados=" + getCantidadEmpleados() +
                '}';
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Comuna comuna = (Comuna) o;
        return id == comuna.id;
    }
    
    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }
}
