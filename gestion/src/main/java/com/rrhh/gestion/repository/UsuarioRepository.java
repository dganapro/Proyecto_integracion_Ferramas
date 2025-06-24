package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Usuario;
import com.rrhh.gestion.entity.Rol;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    
    Optional<Usuario> findByNombreUsuario(String nombreUsuario);
    
    Optional<Usuario> findByEmail(String email);
    
    boolean existsByNombreUsuario(String nombreUsuario);
    
    boolean existsByEmail(String email);
    
    List<Usuario> findByRol(Rol rol);
    
    List<Usuario> findByActivoTrue();
    
    List<Usuario> findByActivoFalse();
    
    @Query("SELECT u FROM Usuario u WHERE u.activo = true AND u.rol = :rol")
    List<Usuario> findActiveUsersByRole(@Param("rol") Rol rol);
    
    @Query("SELECT u FROM Usuario u WHERE u.nombreUsuario LIKE %:busqueda% OR u.nombre LIKE %:busqueda% OR u.apellido LIKE %:busqueda% OR u.email LIKE %:busqueda%")
    List<Usuario> buscarUsuarios(@Param("busqueda") String busqueda);
}
