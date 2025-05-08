// Admin JS for Neo Doctor

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize date pickers if they exist
    const datepickers = document.querySelectorAll('.datepicker');
    if (datepickers.length > 0) {
        datepickers.forEach(function(el) {
            // This is a placeholder - you would need to implement a date picker
            // using a library like Flatpickr or bootstrap-datepicker
            console.log('Date picker initialized');
        });
    }

    // Confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                if (!confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
                    e.preventDefault();
                }
            });
        });
    }

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(function() {
            flashMessages.forEach(function(flash) {
                // Create a Bootstrap 5 alert instance and hide it
                const bsAlert = new bootstrap.Alert(flash);
                bsAlert.close();
            });
        }, 5000);
    }

    // Form validation for required fields
    const forms = document.querySelectorAll('.needs-validation');
    if (forms.length > 0) {
        Array.from(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }
});