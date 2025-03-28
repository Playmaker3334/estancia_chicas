let ubicacionPrincipal = window.scrollY;

AOS.init();

window.addEventListener("scroll", function() {
    let desplazamientoActual = window.scrollY;
    let nav = document.getElementsByTagName("nav")[0];

    if (ubicacionPrincipal >= desplazamientoActual) {
        nav.style.top = "0px";
    } else {
        nav.style.top = "-100px";
    }
    ubicacionPrincipal = desplazamientoActual;
});

// Menú de navegación suave
document.querySelectorAll('.enlaces-header a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        const offset = 80; // Ajusta según la altura de tu menú
        const targetPosition = target.offsetTop - offset;

        window.scrollTo({
            top: targetPosition - 20,
            behavior: 'smooth'
        });
    });
});

// Menú hamburguesa
document.addEventListener("DOMContentLoaded", function() {
    const menu = document.querySelector(".hamburguer");
    const enlaces = document.querySelector(".enlaces-header");

    menu.addEventListener("click", function() {
        enlaces.classList.toggle("active");
    });

    // Código para expandir la pestaña roja en todas las pantallas
    document.querySelectorAll(".service .info").forEach(info => {
        // Detecta si es un dispositivo táctil
        function esTactil() {
            return 'ontouchstart' in window || navigator.maxTouchPoints;
        }

        if (esTactil()) {
            // Para móvil
            info.addEventListener("click", function () {
                this.classList.toggle("expandido"); // Alterna la clase al tocar
            });
        } else {
            // Para escritorio
            info.addEventListener("mouseenter", function () {
                this.classList.add("expandido"); // Levanta la pestaña al pasar el cursor
            });

            info.addEventListener("mouseleave", function () {
                this.classList.remove("expandido"); // Baja la pestaña al quitar el cursor
            });
        }
    });

    // Validación y envío del formulario con AJAX
    const form = document.getElementById("contacto-form");
    
    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent default form submission
            
            // Validate form
            const nombre = document.getElementById("nombre").value.trim();
            const apellidos = document.getElementById("apellidos").value.trim();
            const correo = document.getElementById("correo").value.trim();
            const telefono = document.getElementById("telefono").value.trim();
            const mensaje = document.getElementById("mensaje").value.trim();
            
            // Basic validation
            if (!nombre || !apellidos || !correo || !telefono || !mensaje) {
                showMessage("Todos los campos son obligatorios", "error");
                return;
            }
            
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) {
                showMessage("Correo inválido", "error");
                return;
            }
            
            // Create FormData object to handle file uploads
            const formData = new FormData(form);
            
            // Show loading message
            showMessage("Enviando formulario...", "info");
            
            // Send AJAX request
            fetch('/add_contact', {
                method: 'POST',
                body: formData,
                // Don't set Content-Type header, fetch sets it automatically with boundary for FormData
            })
            .then(response => response.json())
            .then(data => {
                // Remove any existing messages
                removeMessages();
                
                if (data.status === 'success') {
                    // Success message
                    showMessage("Formulario enviado correctamente", "success");
                    form.reset(); // Clear form
                } else {
                    // Error message
                    showMessage("Error al enviar el formulario: " + data.message, "error");
                }
            })
            .catch(error => {
                // Remove any existing messages
                removeMessages();
                
                console.error('Error:', error);
                showMessage("Error al enviar el formulario", "error");
            });
        });
    }
    
    // Function to show messages
    function showMessage(message, type) {
        // Remove any existing messages first
        removeMessages();
        
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = 'form-message ' + type;
        messageDiv.textContent = message;
        
        // Insert before the form
        form.parentNode.insertBefore(messageDiv, form);
        
        // Remove success and info messages after 5 seconds
        if (type === 'success' || type === 'info') {
            setTimeout(() => {
                messageDiv.remove();
            }, 5000);
        }
    }
    
    // Function to remove all message elements
    function removeMessages() {
        document.querySelectorAll('.form-message').forEach(msg => {
            msg.remove();
        });
    }
});