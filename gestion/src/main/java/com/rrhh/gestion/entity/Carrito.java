package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.util.List;

@Entity
@Table(name = "carritos")
public class Carrito {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "cliente_id")
    private Cliente cliente;
    
    @Column(name = "fecha_creacion")
    private LocalDate fechaCreacion;

    @OneToMany(mappedBy = "carrito", cascade = CascadeType.ALL)
    private List<ItemCarrito> itemsCarrito;

    // Constructores
    public Carrito() {
        this.fechaCreacion = LocalDate.now();
    }

    public Carrito(Cliente cliente) {
        this.cliente = cliente;
        this.fechaCreacion = LocalDate.now();
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Cliente getCliente() { return cliente; }
    public void setCliente(Cliente cliente) { this.cliente = cliente; }
    
    public LocalDate getFechaCreacion() { return fechaCreacion; }
    public void setFechaCreacion(LocalDate fechaCreacion) { this.fechaCreacion = fechaCreacion; }
    
    public List<ItemCarrito> getItemsCarrito() { return itemsCarrito; }
    public void setItemsCarrito(List<ItemCarrito> itemsCarrito) { this.itemsCarrito = itemsCarrito; }
}
