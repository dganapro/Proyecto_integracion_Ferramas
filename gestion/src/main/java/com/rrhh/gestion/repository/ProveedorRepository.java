package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Proveedor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ProveedorRepository extends JpaRepository<Proveedor, Long> {
    
    Optional<Proveedor> findByRut(String rut);
    boolean existsByRut(String rut);
    
    List<Proveedor> findByEstado(Proveedor.EstadoProveedor estado);
    List<Proveedor> findByNombreContainingIgnoreCase(String nombre);
    
    @Query("SELECT p FROM Proveedor p WHERE p.estado = 'ACTIVO' ORDER BY p.nombre")
    List<Proveedor> findProveedoresActivosOrdenados();
}
