package com.rrhh.gestion.controller;

import com.rrhh.gestion.dto.UsuarioLoginDTO;
import com.rrhh.gestion.dto.UsuarioRegistroDTO;
import com.rrhh.gestion.dto.UsuarioResponseDTO;
import com.rrhh.gestion.entity.Rol;
import com.rrhh.gestion.service.UsuarioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private UsuarioService usuarioService;

    @PostMapping("/registro")
    public ResponseEntity<?> registrarUsuario(@RequestBody UsuarioRegistroDTO registroDTO) {
        try {
            UsuarioResponseDTO usuarioCreado = usuarioService.registrarUsuario(registroDTO);
            return ResponseEntity.status(HttpStatus.CREATED).body(usuarioCreado);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> iniciarSesion(@RequestBody UsuarioLoginDTO loginDTO) {
        try {
            UsuarioResponseDTO usuario = usuarioService.autenticarUsuario(loginDTO);
            return ResponseEntity.ok(Map.of(
                "usuario", usuario,
                "mensaje", "Inicio de sesión exitoso",
                "tipoVista", usuario.getRol() == Rol.ADMINISTRADOR ? "admin" : "usuario"
            ));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", e.getMessage()));
        }
    }

    @PostMapping("/registro-admin")
    public ResponseEntity<?> registrarAdministrador(@RequestBody UsuarioRegistroDTO registroDTO) {
        try {
            // Forzar el rol a ADMINISTRADOR
            registroDTO.setRol(Rol.ADMINISTRADOR);
            UsuarioResponseDTO usuarioCreado = usuarioService.registrarUsuario(registroDTO);
            return ResponseEntity.status(HttpStatus.CREATED).body(usuarioCreado);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @PostMapping("/registro-usuario")
    public ResponseEntity<?> registrarUsuarioRegular(@RequestBody UsuarioRegistroDTO registroDTO) {
        try {
            // Forzar el rol a USUARIO
            registroDTO.setRol(Rol.USUARIO);
            UsuarioResponseDTO usuarioCreado = usuarioService.registrarUsuario(registroDTO);
            return ResponseEntity.status(HttpStatus.CREATED).body(usuarioCreado);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @GetMapping("/verificar-usuario/{nombreUsuario}")
    public ResponseEntity<?> verificarDisponibilidadUsuario(@PathVariable String nombreUsuario) {
        try {
            boolean existe = usuarioService.obtenerUsuarioPorNombre(nombreUsuario).isPresent();
            return ResponseEntity.ok(Map.of("disponible", !existe));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", "Error al verificar usuario"));
        }
    }

    @GetMapping("/roles")
    public ResponseEntity<?> obtenerRoles() {
        return ResponseEntity.ok(Map.of(
            "roles", new String[]{"USUARIO", "ADMINISTRADOR"}
        ));
    }
}
