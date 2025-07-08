package com.rrhh.gestion.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;           
import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name="comuna")
public class Comuna {
    @Id
    private int id;
    private String nombre;

    @OneToMany(mappedBy="comuna", cascade=CascadeType.ALL, orphanRemoval = true)
    @JsonIgnore
    private List<Empleado> empleados;

    public Comuna() {
        this.empleados = new ArrayList<>();
    }

    public Comuna(int id, String nombre) {
        this.id = id;
        this.nombre = nombre;
    }

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

    public List<Empleado> getEmpleados() {
        return empleados;
    }

    public void setEmpleados(List<Empleado> empleados) {
        this.empleados = empleados;
    }
}
