package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.ItemCarrito;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ItemCarritoRepository extends JpaRepository<ItemCarrito, Long> {
}
