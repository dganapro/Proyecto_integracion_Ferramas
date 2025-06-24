package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.HistorialPrecio;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface HistorialPrecioRepository extends JpaRepository<HistorialPrecio, Long> {
}
