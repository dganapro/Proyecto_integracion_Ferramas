package com.rrhh.gestion.dto;

public class EmpleadoDTO {
    private String rut;
    private String nombre;
    private String telefono;
    private String correo;
    private String comuna;

    public EmpleadoDTO() {
    }

    public EmpleadoDTO(String rut, String nombre, String telefono, String correo, String comuna) {
        this.rut = rut;
        this.nombre = nombre;
        this.telefono = telefono;
        this.correo = correo;
        this.comuna = comuna;
    }

    public String getRut() {
        return rut;
    }

    public void setRut(String rut) {
        this.rut = rut;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getTelefono() {
        return telefono;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    public String getCorreo() {
        return correo;
    }

    public void setCorreo(String correo) {
        this.correo = correo;
    }

    public String getComuna() {
        return comuna;
    }

    public void setComuna(String comuna) {
        this.comuna = comuna;
    }
}