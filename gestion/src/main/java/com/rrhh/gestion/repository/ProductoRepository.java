package com.rrhh.gestion.repository;

import com.rrhh.gestion.entity.Producto;
import com.rrhh.gestion.entity.Categoria;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@Repository
public interface ProductoRepository extends JpaRepository<Producto, Long> {
    
    // Búsqueda por código
    Optional<Producto> findByCodigo(String codigo);
    boolean existsByCodigo(String codigo);
    
    // Búsqueda por nombre
    List<Producto> findByNombreContainingIgnoreCase(String nombre);
    
    // Búsqueda por categoría
    List<Producto> findByCategoria(Categoria categoria);
    List<Producto> findByCategoriaId(Long categoriaId);
    
    // Búsqueda por estado
    List<Producto> findByEstado(Producto.EstadoProducto estado);
    
    // Productos con stock bajo
    @Query("SELECT p FROM Producto p WHERE p.stockActual <= p.stockMinimo")
    List<Producto> findProductosConStockBajo();
    
    // Productos que necesitan restock
    @Query("SELECT p FROM Producto p WHERE p.stockActual <= p.stockMinimo AND p.estado = 'ACTIVO'")
    List<Producto> findProductosQueNecesitanRestock();
    
    // Búsqueda por rango de precios
    List<Producto> findByPrecioVentaBetween(BigDecimal precioMin, BigDecimal precioMax);
    
    // Búsqueda por marca
    List<Producto> findByMarcaContainingIgnoreCase(String marca);
    
    // Búsqueda combinada
    @Query("SELECT p FROM Producto p WHERE " +
           "(:nombre IS NULL OR LOWER(p.nombre) LIKE LOWER(CONCAT('%', :nombre, '%'))) AND " +
           "(:categoria IS NULL OR p.categoria.id = :categoria) AND " +
           "(:marca IS NULL OR LOWER(p.marca) LIKE LOWER(CONCAT('%', :marca, '%'))) AND " +
           "(:precioMin IS NULL OR p.precioVenta >= :precioMin) AND " +
           "(:precioMax IS NULL OR p.precioVenta <= :precioMax) AND " +
           "(:estado IS NULL OR p.estado = :estado)")
    Page<Producto> findProductosConFiltros(
            @Param("nombre") String nombre,
            @Param("categoria") Long categoriaId,
            @Param("marca") String marca,
            @Param("precioMin") BigDecimal precioMin,
            @Param("precioMax") BigDecimal precioMax,
            @Param("estado") Producto.EstadoProducto estado,
            Pageable pageable);
    
    // Estadísticas
    @Query("SELECT COUNT(p) FROM Producto p WHERE p.estado = 'ACTIVO'")
    long countProductosActivos();
    
    @Query("SELECT SUM(p.stockActual * p.precioCompra) FROM Producto p WHERE p.precioCompra IS NOT NULL")
    BigDecimal calcularValorTotalInventario();
    
    // Top productos por stock
    @Query("SELECT p FROM Producto p ORDER BY p.stockActual DESC")
    List<Producto> findTopByStockDesc(Pageable pageable);
    
    // Top productos por precio
    @Query("SELECT p FROM Producto p WHERE p.estado = 'ACTIVO' ORDER BY p.precioVenta DESC")
    List<Producto> findTopByPrecioDesc(Pageable pageable);
}
