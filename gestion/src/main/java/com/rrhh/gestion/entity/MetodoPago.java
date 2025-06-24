package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "metodos_pago")
public class MetodoPago {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String nombre;

    @OneToMany(mappedBy = "metodoPago", cascade = CascadeType.ALL)
    private List<Venta> ventas;

    // Constructores
    public MetodoPago() {}

    public MetodoPago(String nombre) {
        this.nombre = nombre;
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
    public List<Venta> getVentas() { return ventas; }
    public void setVentas(List<Venta> ventas) { this.ventas = ventas; }
}
