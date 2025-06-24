package com.rrhh.gestion.controller;

import com.rrhh.gestion.dto.UsuarioResponseDTO;
import com.rrhh.gestion.entity.Rol;
import com.rrhh.gestion.service.UsuarioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/usuario")
@CrossOrigin(origins = "*")
public class UsuarioViewController {

    @Autowired
    private UsuarioService usuarioService;

    @GetMapping("/dashboard")
    public ResponseEntity<?> obtenerDashboardUsuario() {
        return ResponseEntity.ok(Map.of(
            "mensaje", "Bienvenido al Panel de Usuario",
            "permisos", new String[]{
                "VER_PERFIL",
                "EDITAR_PERFIL",
                "CAMBIAR_CONTRASEÑA"
            },
            "funcionalidades", new String[]{
                "Consultar productos",
                "Realizar compras",
                "Ver historial de compras",
                "Gestionar perfil personal"
            }
        ));
    }

    @GetMapping("/perfil/{id}")
    public ResponseEntity<?> obtenerPerfilUsuario(@PathVariable Long id) {
        try {
            UsuarioResponseDTO usuario = usuarioService.obtenerUsuarioPorId(id).orElse(null);
            
            if (usuario == null) {
                return ResponseEntity.badRequest().body(Map.of("error", "Usuario no encontrado"));
            }

            // Solo permitir ver el perfil si es usuario regular
            if (usuario.getRol() != Rol.USUARIO) {
                return ResponseEntity.badRequest().body(Map.of("error", "Acceso denegado"));
            }

            return ResponseEntity.ok(Map.of(
                "perfil", usuario,
                "configuracion", Map.of(
                    "puedeEditarPerfil", true,
                    "puedeEliminarCuenta", false,
                    "notificacionesActivas", true
                )
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Error al obtener perfil"));
        }
    }

    @PostMapping("/verificar-usuario/{id}")
    public ResponseEntity<?> verificarPermisosUsuario(@PathVariable Long id) {
        try {
            UsuarioResponseDTO usuario = usuarioService.obtenerUsuarioPorId(id).orElse(null);
            
            if (usuario == null) {
                return ResponseEntity.badRequest().body(Map.of("error", "Usuario no encontrado"));
            }

            boolean esUsuario = usuario.getRol() == Rol.USUARIO;
            
            return ResponseEntity.ok(Map.of(
                "esUsuario", esUsuario,
                "usuario", usuario,
                "acceso", esUsuario ? "USUARIO" : "ACCESO_LIMITADO"
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Error al verificar permisos"));
        }
    }

    @GetMapping("/configuracion/{id}")
    public ResponseEntity<?> obtenerConfiguracionUsuario(@PathVariable Long id) {
        try {
            UsuarioResponseDTO usuario = usuarioService.obtenerUsuarioPorId(id).orElse(null);
            
            if (usuario == null || usuario.getRol() != Rol.USUARIO) {
                return ResponseEntity.badRequest().body(Map.of("error", "Usuario no válido"));
            }

            return ResponseEntity.ok(Map.of(
                "configuracionPersonal", Map.of(
                    "tema", "claro",
                    "idioma", "español",
                    "notificaciones", true,
                    "privacidad", "normal"
                ),
                "limitaciones", Map.of(
                    "maxCompras", 10,
                    "descuentoDisponible", true,
                    "accesoReportes", false
                )
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Error al obtener configuración"));
        }
    }
}
