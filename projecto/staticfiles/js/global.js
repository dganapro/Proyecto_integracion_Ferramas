// Función global para agregar al carrito
function addToCart(productoId, cantidad = 1, buttonElement = null) {
    // Si se pasa el elemento del botón, usarlo; si no, usar el event.target
    const btn = buttonElement || event.target;
    const originalText = btn.innerHTML;

    // Loading state
    btn.classList.add('btn-loading');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Agregando...';

    // Usar el endpoint correcto
    fetch(`/agregar-al-carrito/${productoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `cantidad=${cantidad}`
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error('Error en la respuesta del servidor');
    })
    .then(data => {
        updateCartCount();
        showNotification('¡Producto agregado al carrito!', 'success');
        
        // Efecto visual temporal
        btn.innerHTML = '<i class="fas fa-check me-1"></i>¡Agregado!';
        btn.classList.remove('btn-ferramas-primary', 'btn-primary');
        btn.classList.add('btn-success');
        
        // Restaurar después de 2 segundos
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-ferramas-primary');
            btn.classList.remove('btn-loading');
            btn.disabled = false;
        }, 2000);
    })
    .catch(error => {
        showNotification('Error al agregar producto al carrito', 'error');
        console.error('Error:', error);
        
        // Restaurar botón en caso de error
        btn.innerHTML = originalText;
        btn.classList.remove('btn-loading');
        btn.disabled = false;
    });
}

// Actualizar contador del carrito
function updateCartCount() {
    fetch('/api/carrito/resumen/')
        .then(response => response.json())
        .then(data => {
            const cartBadges = document.querySelectorAll('.cart-count, .badge[data-cart-count]');
            cartBadges.forEach(badge => {
                badge.textContent = data.total_items || 0;
                badge.style.display = (data.total_items > 0) ? 'inline-flex' : 'none';
            });
            
            // Actualizar localStorage para persistencia
            localStorage.setItem('cart_count', data.total_items || 0);
        })
        .catch(error => {
            console.error('Error al actualizar contador del carrito:', error);
            
            // Usar valor de localStorage como fallback
            const savedCount = localStorage.getItem('cart_count') || 0;
            const cartBadges = document.querySelectorAll('.cart-count, .badge[data-cart-count]');
            cartBadges.forEach(badge => {
                badge.textContent = savedCount;
                badge.style.display = (savedCount > 0) ? 'inline-flex' : 'none';
            });
        });
}

// Mostrar notificaciones mejoradas
function showNotification(message, type) {
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const iconClass = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} alert-dismissible fade show position-fixed animate-fade-in-up`;
    alertDiv.style.cssText = 'top: 90px; right: 20px; z-index: 1050; min-width: 300px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);';
    alertDiv.innerHTML = `
        <i class="fas ${iconClass} me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertDiv);

    // Auto-dismiss después de 4 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.classList.remove('show');
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 150);
        }
    }, 4000);
}

// Obtener token CSRF mejorado
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Función para validar formularios en tiempo real
function validateForm(formId, requiredFields) {
    const form = document.getElementById(formId);
    if (!form) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    
    function checkValidity() {
        let isValid = true;
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field && (!field.value || field.value.trim() === '')) {
                isValid = false;
            }
        });
        
        if (submitBtn) {
            submitBtn.disabled = !isValid;
        }
    }
    
    // Agregar listeners a todos los campos requeridos
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', checkValidity);
            field.addEventListener('change', checkValidity);
        }
    });
    
    // Validar al cargar
    checkValidity();
}

// Función para formatear números como moneda
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP',
        minimumFractionDigits: 0
    }).format(amount);
}

// Función para formatear números
function formatNumber(number) {
    return new Intl.NumberFormat('es-CL').format(number);
}

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function () {
    // Actualizar contador del carrito
    updateCartCount();

    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Inicializar tooltips de Bootstrap si están disponibles
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Prevenir envío múltiple de formularios
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                setTimeout(() => {
                    submitBtn.disabled = true;
                }, 100);
            }
        });
    });
});

// Función para confirmar acciones peligrosas
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Función para mostrar loading en botones
function showLoading(button, loadingText = 'Procesando...') {
    const originalText = button.innerHTML;
    button.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${loadingText}`;
    button.disabled = true;
    
    return function() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Función para debounce (evitar múltiples llamadas rápidas)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}