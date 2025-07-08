package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Categoria;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CategoriaRepository extends JpaRepository<Categoria, Long> {
    
    Optional<Categoria> findByNombre(String nombre);
    boolean existsByNombre(String nombre);
    
    List<Categoria> findByActivaTrue();
    List<Categoria> findByNombreContainingIgnoreCase(String nombre);
    
    @Query("SELECT c FROM Categoria c WHERE c.activa = true ORDER BY c.nombre")
    List<Categoria> findCategoriasActivasOrdenadas();
    
    @Query("SELECT c FROM Categoria c JOIN c.productos p GROUP BY c ORDER BY COUNT(p) DESC")
    List<Categoria> findCategoriasConMasProductos();
}
