package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Entity
@Table(name = "ventas")
public class Venta {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "cliente_id")
    private Cliente cliente;
    
    @ManyToOne
    @JoinColumn(name = "sede_id")
    private Sede sede;
    
    @Column(nullable = false)
    private LocalDate fecha;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal total;
    
    @ManyToOne
    @JoinColumn(name = "empleado_id")
    private Empleado empleado;
    
    @ManyToOne
    @JoinColumn(name = "metodo_pago_id")
    private MetodoPago metodoPago;

    @OneToMany(mappedBy = "venta", cascade = CascadeType.ALL)
    private List<DetalleVenta> detallesVenta;

    @OneToOne(mappedBy = "venta", cascade = CascadeType.ALL)
    private Envio envio;

    // Constructores
    public Venta() {}

    public Venta(Cliente cliente, Sede sede, LocalDate fecha, BigDecimal total, Empleado empleado, MetodoPago metodoPago) {
        this.cliente = cliente;
        this.sede = sede;
        this.fecha = fecha;
        this.total = total;
        this.empleado = empleado;
        this.metodoPago = metodoPago;
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Cliente getCliente() { return cliente; }
    public void setCliente(Cliente cliente) { this.cliente = cliente; }
    
    public Sede getSede() { return sede; }
    public void setSede(Sede sede) { this.sede = sede; }
    
    public LocalDate getFecha() { return fecha; }
    public void setFecha(LocalDate fecha) { this.fecha = fecha; }
    
    public BigDecimal getTotal() { return total; }
    public void setTotal(BigDecimal total) { this.total = total; }
    
    public Empleado getEmpleado() { return empleado; }
    public void setEmpleado(Empleado empleado) { this.empleado = empleado; }
    
    public MetodoPago getMetodoPago() { return metodoPago; }
    public void setMetodoPago(MetodoPago metodoPago) { this.metodoPago = metodoPago; }
    
    public List<DetalleVenta> getDetallesVenta() { return detallesVenta; }
    public void setDetallesVenta(List<DetalleVenta> detallesVenta) { this.detallesVenta = detallesVenta; }
    
    public Envio getEnvio() { return envio; }
    public void setEnvio(Envio envio) { this.envio = envio; }
}
