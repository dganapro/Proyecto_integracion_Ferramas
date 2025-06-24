package com.rrhh.gestion.controller;

import com.rrhh.gestion.dto.UsuarioRegistroDTO;
import com.rrhh.gestion.dto.UsuarioResponseDTO;
import com.rrhh.gestion.entity.Rol;
import com.rrhh.gestion.service.UsuarioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/usuarios")
@CrossOrigin(origins = "*")
public class UsuarioController {

    @Autowired
    private UsuarioService usuarioService;

    @GetMapping
    public ResponseEntity<List<UsuarioResponseDTO>> obtenerTodosLosUsuarios() {
        List<UsuarioResponseDTO> usuarios = usuarioService.obtenerTodosLosUsuarios();
        return ResponseEntity.ok(usuarios);
    }

    @GetMapping("/activos")
    public ResponseEntity<List<UsuarioResponseDTO>> obtenerUsuariosActivos() {
        List<UsuarioResponseDTO> usuarios = usuarioService.obtenerUsuariosActivos();
        return ResponseEntity.ok(usuarios);
    }

    @GetMapping("/rol/{rol}")
    public ResponseEntity<List<UsuarioResponseDTO>> obtenerUsuariosPorRol(@PathVariable String rol) {
        try {
            Rol rolEnum = Rol.valueOf(rol.toUpperCase());
            List<UsuarioResponseDTO> usuarios = usuarioService.obtenerUsuariosPorRol(rolEnum);
            return ResponseEntity.ok(usuarios);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<UsuarioResponseDTO> obtenerUsuarioPorId(@PathVariable Long id) {
        Optional<UsuarioResponseDTO> usuario = usuarioService.obtenerUsuarioPorId(id);
        return usuario.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/buscar")
    public ResponseEntity<List<UsuarioResponseDTO>> buscarUsuarios(@RequestParam String q) {
        List<UsuarioResponseDTO> usuarios = usuarioService.buscarUsuarios(q);
        return ResponseEntity.ok(usuarios);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> actualizarUsuario(@PathVariable Long id, @RequestBody UsuarioRegistroDTO datosActualizados) {
        try {
            UsuarioResponseDTO usuarioActualizado = usuarioService.actualizarUsuario(id, datosActualizados);
            return ResponseEntity.ok(usuarioActualizado);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @PutMapping("/{id}/estado")
    public ResponseEntity<?> cambiarEstadoUsuario(@PathVariable Long id, @RequestBody Map<String, Boolean> estado) {
        try {
            boolean activo = estado.getOrDefault("activo", true);
            usuarioService.cambiarEstadoUsuario(id, activo);
            return ResponseEntity.ok(Map.of("mensaje", "Estado del usuario actualizado"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> eliminarUsuario(@PathVariable Long id) {
        try {
            usuarioService.eliminarUsuario(id);
            return ResponseEntity.ok(Map.of("mensaje", "Usuario eliminado exitosamente"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @GetMapping("/estadisticas")
    public ResponseEntity<?> obtenerEstadisticas() {
        long totalUsuarios = usuarioService.contarUsuariosPorRol(Rol.USUARIO);
        long totalAdministradores = usuarioService.contarUsuariosPorRol(Rol.ADMINISTRADOR);
        long totalActivos = usuarioService.obtenerUsuariosActivos().size();

        return ResponseEntity.ok(Map.of(
            "totalUsuarios", totalUsuarios,
            "totalAdministradores", totalAdministradores,
            "totalActivos", totalActivos,
            "totalGeneral", totalUsuarios + totalAdministradores
        ));
    }
}
