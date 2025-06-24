package com.rrhh.gestion.service;

import com.rrhh.gestion.dto.UsuarioLoginDTO;
import com.rrhh.gestion.dto.UsuarioRegistroDTO;
import com.rrhh.gestion.dto.UsuarioResponseDTO;
import com.rrhh.gestion.entity.Rol;
import com.rrhh.gestion.entity.Usuario;
import com.rrhh.gestion.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class UsuarioService {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public UsuarioResponseDTO registrarUsuario(UsuarioRegistroDTO registroDTO) {
        // Verificar si el usuario ya existe
        if (usuarioRepository.existsByNombreUsuario(registroDTO.getNombreUsuario())) {
            throw new RuntimeException("El nombre de usuario ya existe");
        }
        
        if (usuarioRepository.existsByEmail(registroDTO.getEmail())) {
            throw new RuntimeException("El email ya está registrado");
        }

        // Crear nuevo usuario
        Usuario usuario = new Usuario();
        usuario.setNombreUsuario(registroDTO.getNombreUsuario());
        usuario.setNombre(registroDTO.getNombre());
        usuario.setApellido(registroDTO.getApellido());
        usuario.setEmail(registroDTO.getEmail());
        usuario.setPassword(passwordEncoder.encode(registroDTO.getPassword()));
        usuario.setRol(registroDTO.getRol());
        usuario.setActivo(true);
        usuario.setFechaCreacion(LocalDateTime.now());

        Usuario usuarioGuardado = usuarioRepository.save(usuario);
        return convertirADTO(usuarioGuardado);
    }

    public UsuarioResponseDTO autenticarUsuario(UsuarioLoginDTO loginDTO) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findByNombreUsuario(loginDTO.getNombreUsuario());
        
        if (usuarioOpt.isEmpty()) {
            throw new RuntimeException("Usuario no encontrado");
        }

        Usuario usuario = usuarioOpt.get();
        
        if (!usuario.isActivo()) {
            throw new RuntimeException("Usuario inactivo");
        }

        if (!passwordEncoder.matches(loginDTO.getPassword(), usuario.getPassword())) {
            throw new RuntimeException("Contraseña incorrecta");
        }

        // Actualizar último acceso
        usuario.setUltimoAcceso(LocalDateTime.now());
        usuarioRepository.save(usuario);

        return convertirADTO(usuario);
    }

    public List<UsuarioResponseDTO> obtenerTodosLosUsuarios() {
        return usuarioRepository.findAll().stream()
                .map(this::convertirADTO)
                .collect(Collectors.toList());
    }

    public List<UsuarioResponseDTO> obtenerUsuariosActivos() {
        return usuarioRepository.findByActivoTrue().stream()
                .map(this::convertirADTO)
                .collect(Collectors.toList());
    }

    public List<UsuarioResponseDTO> obtenerUsuariosPorRol(Rol rol) {
        return usuarioRepository.findByRol(rol).stream()
                .map(this::convertirADTO)
                .collect(Collectors.toList());
    }

    public Optional<UsuarioResponseDTO> obtenerUsuarioPorId(Long id) {
        return usuarioRepository.findById(id)
                .map(this::convertirADTO);
    }

    public Optional<UsuarioResponseDTO> obtenerUsuarioPorNombre(String nombreUsuario) {
        return usuarioRepository.findByNombreUsuario(nombreUsuario)
                .map(this::convertirADTO);
    }

    public UsuarioResponseDTO actualizarUsuario(Long id, UsuarioRegistroDTO datosActualizados) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findById(id);
        
        if (usuarioOpt.isEmpty()) {
            throw new RuntimeException("Usuario no encontrado");
        }

        Usuario usuario = usuarioOpt.get();
        
        // Verificar si el nuevo nombre de usuario ya existe (si es diferente)
        if (!usuario.getNombreUsuario().equals(datosActualizados.getNombreUsuario()) &&
            usuarioRepository.existsByNombreUsuario(datosActualizados.getNombreUsuario())) {
            throw new RuntimeException("El nombre de usuario ya existe");
        }

        // Verificar si el nuevo email ya existe (si es diferente)
        if (!usuario.getEmail().equals(datosActualizados.getEmail()) &&
            usuarioRepository.existsByEmail(datosActualizados.getEmail())) {
            throw new RuntimeException("El email ya está registrado");
        }

        usuario.setNombreUsuario(datosActualizados.getNombreUsuario());
        usuario.setNombre(datosActualizados.getNombre());
        usuario.setApellido(datosActualizados.getApellido());
        usuario.setEmail(datosActualizados.getEmail());
        usuario.setRol(datosActualizados.getRol());
        
        if (datosActualizados.getPassword() != null && !datosActualizados.getPassword().isEmpty()) {
            usuario.setPassword(passwordEncoder.encode(datosActualizados.getPassword()));
        }

        Usuario usuarioActualizado = usuarioRepository.save(usuario);
        return convertirADTO(usuarioActualizado);
    }

    public void cambiarEstadoUsuario(Long id, boolean activo) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findById(id);
        
        if (usuarioOpt.isEmpty()) {
            throw new RuntimeException("Usuario no encontrado");
        }

        Usuario usuario = usuarioOpt.get();
        usuario.setActivo(activo);
        usuarioRepository.save(usuario);
    }

    public void eliminarUsuario(Long id) {
        if (!usuarioRepository.existsById(id)) {
            throw new RuntimeException("Usuario no encontrado");
        }
        usuarioRepository.deleteById(id);
    }

    public List<UsuarioResponseDTO> buscarUsuarios(String busqueda) {
        return usuarioRepository.buscarUsuarios(busqueda).stream()
                .map(this::convertirADTO)
                .collect(Collectors.toList());
    }

    public long contarUsuariosPorRol(Rol rol) {
        return usuarioRepository.findByRol(rol).size();
    }

    private UsuarioResponseDTO convertirADTO(Usuario usuario) {
        return new UsuarioResponseDTO(
                usuario.getId(),
                usuario.getNombreUsuario(),
                usuario.getNombre(),
                usuario.getApellido(),
                usuario.getEmail(),
                usuario.getRol(),
                usuario.isActivo(),
                usuario.getFechaCreacion(),
                usuario.getUltimoAcceso()
        );
    }
}
