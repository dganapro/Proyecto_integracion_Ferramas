package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "productos")
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true, length = 50)
    @NotBlank(message = "El código es obligatorio")
    private String codigo;
    
    @Column(nullable = false, length = 200)
    @NotBlank(message = "El nombre es obligatorio")
    private String nombre;
    
    @Column(length = 1000)
    private String descripcion;
    
    @Column(nullable = false, precision = 10, scale = 2)
    @NotNull(message = "El precio de venta es obligatorio")
    @DecimalMin(value = "0.01", message = "El precio debe ser mayor a 0")
    private BigDecimal precioVenta;
    
    @Column(precision = 10, scale = 2)
    @DecimalMin(value = "0.00", message = "El precio de compra no puede ser negativo")
    private BigDecimal precioCompra;
    
    @Column(nullable = false)
    @NotNull(message = "El stock es obligatorio")
    @Min(value = 0, message = "El stock no puede ser negativo")
    private Integer stockActual;
    
    @Column(nullable = false)
    @Min(value = 0, message = "El stock mínimo no puede ser negativo")
    private Integer stockMinimo = 5;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "categoria_id")
    private Categoria categoria;
    
    @Column(length = 100)
    private String marca;
    
    @Column(length = 100)
    private String modelo;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "proveedor_id")
    private Proveedor proveedor;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private EstadoProducto estado = EstadoProducto.ACTIVO;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UnidadMedida unidadMedida = UnidadMedida.UNIDAD;
    
    @Column
    private String imagen;
    
    @Column(precision = 8, scale = 3)
    private BigDecimal peso;
    
    @Column(nullable = false)
    private LocalDateTime fechaCreacion = LocalDateTime.now();
    
    @Column(nullable = false)
    private LocalDateTime fechaActualizacion = LocalDateTime.now();
    
    @Column(length = 50)
    private String usuarioCreacion;
    
    @Column(length = 50)
    private String usuarioActualizacion;

    // Relaciones
    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<DetalleVenta> detallesVenta;

    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ItemCarrito> itemsCarrito;

    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<HistorialPrecio> historialPrecios;

    @OneToMany(mappedBy = "producto", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<MovimientoInventario> movimientosInventario;

    // Enums
    public enum EstadoProducto {
        ACTIVO, INACTIVO, DESCONTINUADO
    }
    
    public enum UnidadMedida {
        UNIDAD, METRO, KILOGRAMO, LITRO, CAJA, PAQUETE, GRAMO, CENTIMETRO
    }

    // Constructores
    public Producto() {}

    public Producto(String codigo, String nombre, String descripcion, BigDecimal precioVenta, 
                   Integer stockActual, Categoria categoria) {
        this.codigo = codigo;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.precioVenta = precioVenta;
        this.stockActual = stockActual;
        this.categoria = categoria;
        this.fechaCreacion = LocalDateTime.now();
        this.fechaActualizacion = LocalDateTime.now();
    }

    // Métodos de negocio
    public boolean necesitaRestock() {
        return this.stockActual <= this.stockMinimo;
    }
    
    public BigDecimal calcularValorInventario() {
        if (precioCompra != null) {
            return precioCompra.multiply(BigDecimal.valueOf(stockActual));
        }
        return BigDecimal.ZERO;
    }
    
    public BigDecimal calcularMargenGanancia() {
        if (precioCompra != null && precioCompra.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal diferencia = precioVenta.subtract(precioCompra);
            return diferencia.divide(precioCompra, 4, BigDecimal.ROUND_HALF_UP)
                           .multiply(BigDecimal.valueOf(100));
        }
        return BigDecimal.ZERO;
    }
    
    public boolean estaDisponible() {
        return estado == EstadoProducto.ACTIVO && stockActual > 0;
    }
    
    public void reducirStock(int cantidad) {
        if (cantidad > stockActual) {
            throw new IllegalArgumentException("No hay suficiente stock disponible");
        }
        this.stockActual -= cantidad;
        this.fechaActualizacion = LocalDateTime.now();
    }
    
    public void aumentarStock(int cantidad) {
        this.stockActual += cantidad;
        this.fechaActualizacion = LocalDateTime.now();
    }
    
    @PreUpdate
    public void preUpdate() {
        this.fechaActualizacion = LocalDateTime.now();
    }

    // Getters y Setters básicos
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getCodigo() { return codigo; }
    public void setCodigo(String codigo) { this.codigo = codigo; }
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    
    public BigDecimal getPrecioVenta() { return precioVenta; }
    public void setPrecioVenta(BigDecimal precioVenta) { 
        this.precioVenta = precioVenta;
        this.fechaActualizacion = LocalDateTime.now();
    }
    
    public BigDecimal getPrecioCompra() { return precioCompra; }
    public void setPrecioCompra(BigDecimal precioCompra) { 
        this.precioCompra = precioCompra;
        this.fechaActualizacion = LocalDateTime.now();
    }
    
    public Integer getStockActual() { return stockActual; }
    public void setStockActual(Integer stockActual) { 
        this.stockActual = stockActual;
        this.fechaActualizacion = LocalDateTime.now();
    }
    
    public Integer getStockMinimo() { return stockMinimo; }
    public void setStockMinimo(Integer stockMinimo) { this.stockMinimo = stockMinimo; }
    
    public Categoria getCategoria() { return categoria; }
    public void setCategoria(Categoria categoria) { this.categoria = categoria; }
    
    public String getMarca() { return marca; }
    public void setMarca(String marca) { this.marca = marca; }
    
    public String getModelo() { return modelo; }
    public void setModelo(String modelo) { this.modelo = modelo; }
    
    public Proveedor getProveedor() { return proveedor; }
    public void setProveedor(Proveedor proveedor) { this.proveedor = proveedor; }
    
    public EstadoProducto getEstado() { return estado; }
    public void setEstado(EstadoProducto estado) { this.estado = estado; }
    
    public UnidadMedida getUnidadMedida() { return unidadMedida; }
    public void setUnidadMedida(UnidadMedida unidadMedida) { this.unidadMedida = unidadMedida; }
    
    public String getImagen() { return imagen; }
    public void setImagen(String imagen) { this.imagen = imagen; }
    
    public BigDecimal getPeso() { return peso; }
    public void setPeso(BigDecimal peso) { this.peso = peso; }
    
    public LocalDateTime getFechaCreacion() { return fechaCreacion; }
    public void setFechaCreacion(LocalDateTime fechaCreacion) { this.fechaCreacion = fechaCreacion; }
    
    public LocalDateTime getFechaActualizacion() { return fechaActualizacion; }
    public void setFechaActualizacion(LocalDateTime fechaActualizacion) { this.fechaActualizacion = fechaActualizacion; }
    
    public String getUsuarioCreacion() { return usuarioCreacion; }
    public void setUsuarioCreacion(String usuarioCreacion) { this.usuarioCreacion = usuarioCreacion; }
    
    public String getUsuarioActualizacion() { return usuarioActualizacion; }
    public void setUsuarioActualizacion(String usuarioActualizacion) { this.usuarioActualizacion = usuarioActualizacion; }
    
    // Getters y Setters para relaciones
    public List<DetalleVenta> getDetallesVenta() { return detallesVenta; }
    public void setDetallesVenta(List<DetalleVenta> detallesVenta) { this.detallesVenta = detallesVenta; }
    
    public List<ItemCarrito> getItemsCarrito() { return itemsCarrito; }
    public void setItemsCarrito(List<ItemCarrito> itemsCarrito) { this.itemsCarrito = itemsCarrito; }
    
    public List<HistorialPrecio> getHistorialPrecios() { return historialPrecios; }
    public void setHistorialPrecios(List<HistorialPrecio> historialPrecios) { this.historialPrecios = historialPrecios; }
    
    public List<MovimientoInventario> getMovimientosInventario() { return movimientosInventario; }
    public void setMovimientosInventario(List<MovimientoInventario> movimientosInventario) { this.movimientosInventario = movimientosInventario; }
    
    @Override
    public String toString() {
        return "Producto{" +
                "id=" + id +
                ", codigo='" + codigo + '\'' +
                ", nombre='" + nombre + '\'' +
                ", precioVenta=" + precioVenta +
                ", stockActual=" + stockActual +
                ", estado=" + estado +
                '}';
    }
}
