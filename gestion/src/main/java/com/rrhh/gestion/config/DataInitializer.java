package com.rrhh.gestion.config;

import com.rrhh.gestion.entity.Rol;
import com.rrhh.gestion.entity.Usuario;
import com.rrhh.gestion.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        // Crear usuario administrador por defecto si no existe
        if (!usuarioRepository.existsByNombreUsuario("admin")) {
            Usuario admin = new Usuario();
            admin.setNombreUsuario("admin");
            admin.setNombre("Administrador");
            admin.setApellido("Sistema");
            admin.setEmail("admin@sistema.com");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setRol(Rol.ADMINISTRADOR);
            admin.setActivo(true);
            admin.setFechaCreacion(LocalDateTime.now());
            
            usuarioRepository.save(admin);
            System.out.println("✅ Usuario administrador creado: admin / admin123");
        }

        // Crear usuario regular por defecto si no existe
        if (!usuarioRepository.existsByNombreUsuario("usuario")) {
            Usuario usuario = new Usuario();
            usuario.setNombreUsuario("usuario");
            usuario.setNombre("Usuario");
            usuario.setApellido("Demo");
            usuario.setEmail("usuario@demo.com");
            usuario.setPassword(passwordEncoder.encode("usuario123"));
            usuario.setRol(Rol.USUARIO);
            usuario.setActivo(true);
            usuario.setFechaCreacion(LocalDateTime.now());
            
            usuarioRepository.save(usuario);
            System.out.println("✅ Usuario regular creado: usuario / usuario123");
        }

        System.out.println("🚀 Sistema de usuarios inicializado correctamente");
        System.out.println("📋 Usuarios disponibles:");
        System.out.println("   👤 Admin: admin / admin123");
        System.out.println("   👤 Usuario: usuario / usuario123");
    }
}