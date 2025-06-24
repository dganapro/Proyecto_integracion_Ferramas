package com.rrhh.gestion.controller;

import com.rrhh.gestion.dto.UsuarioResponseDTO;
import com.rrhh.gestion.entity.Rol;
import com.rrhh.gestion.service.UsuarioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "*")
public class AdminController {

    @Autowired
    private UsuarioService usuarioService;

    @GetMapping("/dashboard")
    public ResponseEntity<?> obtenerDashboardAdmin() {
        try {
            long totalUsuarios = usuarioService.contarUsuariosPorRol(Rol.USUARIO);
            long totalAdministradores = usuarioService.contarUsuariosPorRol(Rol.ADMINISTRADOR);
            long totalActivos = usuarioService.obtenerUsuariosActivos().size();

            return ResponseEntity.ok(Map.of(
                "mensaje", "Bienvenido al Panel de Administrador",
                "estadisticas", Map.of(
                    "totalUsuarios", totalUsuarios,
                    "totalAdministradores", totalAdministradores,
                    "totalActivos", totalActivos,
                    "totalGeneral", totalUsuarios + totalAdministradores
                ),
                "permisos", new String[]{
                    "CREAR_USUARIOS",
                    "EDITAR_USUARIOS", 
                    "ELIMINAR_USUARIOS",
                    "VER_REPORTES",
                    "GESTIONAR_SISTEMA"
                }
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Error al cargar dashboard"));
        }
    }

    @GetMapping("/usuarios-sistema")
    public ResponseEntity<?> obtenerUsuariosParaAdmin() {
        try {
            return ResponseEntity.ok(Map.of(
                "usuarios", usuarioService.obtenerTodosLosUsuarios(),
                "mensaje", "Lista completa de usuarios del sistema"
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Error al obtener usuarios"));
        }
    }

    @PostMapping("/verificar-admin/{id}")
    public ResponseEntity<?> verificarPermisosAdmin(@PathVariable Long id) {
        try {
            UsuarioResponseDTO usuario = usuarioService.obtenerUsuarioPorId(id).orElse(null);
            
            if (usuario == null) {
                return ResponseEntity.badRequest().body(Map.of("error", "Usuario no encontrado"));
            }

            boolean esAdmin = usuario.getRol() == Rol.ADMINISTRADOR;
            
            return ResponseEntity.ok(Map.of(
                "esAdministrador", esAdmin,
                "usuario", usuario,
                "acceso", esAdmin ? "COMPLETO" : "DENEGADO"
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Error al verificar permisos"));
        }
    }

    @GetMapping("/configuracion")
    public ResponseEntity<?> obtenerConfiguracionSistema() {
        return ResponseEntity.ok(Map.of(
            "sistema", "Sistema de Gestión de Usuarios",
            "version", "1.0.0",
            "configuraciones", Map.of(
                "permitirRegistroLibre", true,
                "requiereAprobacionAdmin", false,
                "sesionExpirationTime", 3600
            )
        ));
    }
}
