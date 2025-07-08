package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.util.List;

@Entity
@Table(name = "productos")
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String nombre;
    
    private String descripcion;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal precio;
    
    @Column(nullable = false)
    private Integer stock;
    
    private String categoria;

    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL)
    private List<DetalleVenta> detallesVenta;

    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL)
    private List<ItemCarrito> itemsCarrito;

    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL)
    private List<HistorialPrecio> historialPrecios;

    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL)
    private List<MovimientoInventario> movimientosInventario;

    // Constructores
    public Producto() {}

    public Producto(String nombre, String descripcion, BigDecimal precio, Integer stock, String categoria) {
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.precio = precio;
        this.stock = stock;
        this.categoria = categoria;
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    
    public BigDecimal getPrecio() { return precio; }
    public void setPrecio(BigDecimal precio) { this.precio = precio; }
    
    public Integer getStock() { return stock; }
    public void setStock(Integer stock) { this.stock = stock; }
    
    public String getCategoria() { return categoria; }
    public void setCategoria(String categoria) { this.categoria = categoria; }
    
    public List<DetalleVenta> getDetallesVenta() { return detallesVenta; }
    public void setDetallesVenta(List<DetalleVenta> detallesVenta) { this.detallesVenta = detallesVenta; }
    
    public List<ItemCarrito> getItemsCarrito() { return itemsCarrito; }
    public void setItemsCarrito(List<ItemCarrito> itemsCarrito) { this.itemsCarrito = itemsCarrito; }
    
    public List<HistorialPrecio> getHistorialPrecios() { return historialPrecios; }
    public void setHistorialPrecios(List<HistorialPrecio> historialPrecios) { this.historialPrecios = historialPrecios; }
    
    public List<MovimientoInventario> getMovimientosInventario() { return movimientosInventario; }
    public void setMovimientosInventario(List<MovimientoInventario> movimientosInventario) { this.movimientosInventario = movimientosInventario; }
}
