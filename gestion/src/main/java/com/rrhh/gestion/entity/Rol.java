package com.rrhh.gestion.entity;

public enum Rol {
    USUARIO("USUARIO"),
    ADMINISTRADOR("ADMINISTRADOR");

    private final String nombre;

    Rol(String nombre) {
        this.nombre = nombre;
    }

    public String getNombre() {
        return nombre;
    }
}
