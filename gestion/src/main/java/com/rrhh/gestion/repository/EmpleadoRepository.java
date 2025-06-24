package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Empleado;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EmpleadoRepository extends JpaRepository<Empleado, String> {
}
