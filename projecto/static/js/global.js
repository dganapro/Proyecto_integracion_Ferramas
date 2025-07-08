// Función global para agregar al carrito
function addToCart(productoId, cantidad = 1) {
    const btn = event.target;
    const originalText = btn.innerHTML;

    // Loading state
    btn.classList.add('btn-loading');
    btn.disabled = true;

    fetch('/api/carrito/agregar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            producto_id: productoId,
            cantidad: cantidad
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartCount();
                showNotification('Producto agregado al carrito', 'success');
            } else {
                showNotification(data.error || 'Error al agregar producto', 'error');
            }
        })
        .catch(error => {
            showNotification('Error de conexión', 'error');
            console.error('Error:', error);
        })
        .finally(() => {
            // Remove loading state
            btn.classList.remove('btn-loading');
            btn.disabled = false;
            btn.innerHTML = originalText;
        });
}

// Actualizar contador del carrito
function updateCartCount() {
    fetch('/api/carrito/resumen/')
        .then(response => response.json())
        .then(data => {
            const cartBadge = document.querySelector('.cart-count');
            if (cartBadge) {
                cartBadge.textContent = data.total_items;
                cartBadge.style.display = data.total_items > 0 ? 'flex' : 'none';
            }
        })
        .catch(error => console.error('Error:', error));
}

// Mostrar notificaciones
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

// Obtener token CSRF
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

// Actualizar contador al cargar la página
document.addEventListener('DOMContentLoaded', function () {
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
});