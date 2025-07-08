package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "movimientos_inventario")
public class MovimientoInventario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "producto_id")
    private Producto producto;
    
    @Column(nullable = false)
    private Integer cantidad;
    
    @Column(name = "tipo_movimiento", nullable = false)
    private String tipoMovimiento;
    
    @Column(nullable = false)
    private LocalDate fecha;

    // Constructores
    public MovimientoInventario() {
        this.fecha = LocalDate.now();
    }

    public MovimientoInventario(Producto producto, Integer cantidad, String tipoMovimiento) {
        this.producto = producto;
        this.cantidad = cantidad;
        this.tipoMovimiento = tipoMovimiento;
        this.fecha = LocalDate.now();
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Producto getProducto() { return producto; }
    public void setProducto(Producto producto) { this.producto = producto; }
    
    public Integer getCantidad() { return cantidad; }
    public void setCantidad(Integer cantidad) { this.cantidad = cantidad; }
    
    public String getTipoMovimiento() { return tipoMovimiento; }
    public void setTipoMovimiento(String tipoMovimiento) { this.tipoMovimiento = tipoMovimiento; }
    
    public LocalDate getFecha() { return fecha; }
    public void setFecha(LocalDate fecha) { this.fecha = fecha; }
}
