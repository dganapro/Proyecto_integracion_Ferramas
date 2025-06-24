package com.rrhh.gestion.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Controlador para manejar las rutas de las páginas web
 */
@Controller
public class WebController {

    /**
     * Página principal - redirige al login
     */
    @GetMapping("/")
    public String index() {
        return "redirect:/login";
    }

    /**
     * Página de login
     */
    @GetMapping("/login")
    public String login() {
        return "login";
    }

    /**
     * Página de registro
     */
    @GetMapping("/registro")
    public String registro() {
        return "registro";
    }

    /**
     * Dashboard de administrador
     */
    @GetMapping("/admin/dashboard")
    public String adminDashboard() {
        return "admin-dashboard";
    }

    /**
     * Dashboard de usuario
     */
    @GetMapping("/usuario/dashboard")
    public String usuarioDashboard() {
        return "usuario-dashboard";
    }
}
