package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;

@Entity
@Table(name = "movimientos_inventario")
public class MovimientoInventario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "producto_id", nullable = false)
    @NotNull
    private Producto producto;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TipoMovimiento tipoMovimiento;
    
    @Column(nullable = false)
    @NotNull
    private Integer cantidad;
    
    @Column(nullable = false)
    private Integer stockAnterior;
    
    @Column(nullable = false)
    private Integer stockNuevo;
    
    @Column(length = 500)
    private String motivo;
    
    @Column(length = 100)
    private String usuario;
    
    @Column(nullable = false)
    private LocalDateTime fechaMovimiento = LocalDateTime.now();
    
    public enum TipoMovimiento {
        ENTRADA, SALIDA, AJUSTE, VENTA, DEVOLUCION, TRANSFERENCIA
    }
    
    // Constructores
    public MovimientoInventario() {}
    
    public MovimientoInventario(Producto producto, TipoMovimiento tipoMovimiento, 
                               Integer cantidad, Integer stockAnterior, String motivo) {
        this.producto = producto;
        this.tipoMovimiento = tipoMovimiento;
        this.cantidad = cantidad;
        this.stockAnterior = stockAnterior;
        this.stockNuevo = stockAnterior + (tipoMovimiento == TipoMovimiento.ENTRADA ? cantidad : -cantidad);
        this.motivo = motivo;
        this.fechaMovimiento = LocalDateTime.now();
    }
    
    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Producto getProducto() { return producto; }
    public void setProducto(Producto producto) { this.producto = producto; }
    
    public TipoMovimiento getTipoMovimiento() { return tipoMovimiento; }
    public void setTipoMovimiento(TipoMovimiento tipoMovimiento) { this.tipoMovimiento = tipoMovimiento; }
    
    public Integer getCantidad() { return cantidad; }
    public void setCantidad(Integer cantidad) { this.cantidad = cantidad; }
    
    public Integer getStockAnterior() { return stockAnterior; }
    public void setStockAnterior(Integer stockAnterior) { this.stockAnterior = stockAnterior; }
    
    public Integer getStockNuevo() { return stockNuevo; }
    public void setStockNuevo(Integer stockNuevo) { this.stockNuevo = stockNuevo; }
    
    public String getMotivo() { return motivo; }
    public void setMotivo(String motivo) { this.motivo = motivo; }
    
    public String getUsuario() { return usuario; }
    public void setUsuario(String usuario) { this.usuario = usuario; }
    
    public LocalDateTime getFechaMovimiento() { return fechaMovimiento; }
    public void setFechaMovimiento(LocalDateTime fechaMovimiento) { this.fechaMovimiento = fechaMovimiento; }
}
