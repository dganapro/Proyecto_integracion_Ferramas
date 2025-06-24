package com.rrhh.gestion.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "envios")
public class Envio {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne
    @JoinColumn(name = "venta_id")
    private Venta venta;
    
    @Column(name = "fecha_envio")
    private LocalDate fechaEnvio;
    
    @Column(name = "fecha_entrega")
    private LocalDate fechaEntrega;
    
    private String estado;

    // Constructores
    public Envio() {}

    public Envio(Venta venta, LocalDate fechaEnvio, LocalDate fechaEntrega, String estado) {
        this.venta = venta;
        this.fechaEnvio = fechaEnvio;
        this.fechaEntrega = fechaEntrega;
        this.estado = estado;
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Venta getVenta() { return venta; }
    public void setVenta(Venta venta) { this.venta = venta; }
    
    public LocalDate getFechaEnvio() { return fechaEnvio; }
    public void setFechaEnvio(LocalDate fechaEnvio) { this.fechaEnvio = fechaEnvio; }
    
    public LocalDate getFechaEntrega() { return fechaEntrega; }
    public void setFechaEntrega(LocalDate fechaEntrega) { this.fechaEntrega = fechaEntrega; }
    
    public String getEstado() { return estado; }
    public void setEstado(String estado) { this.estado = estado; }
}
