// Phidelis Ann Foundation - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {

    // Smooth scrolling for anchor links
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

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            }
        });
    });

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Phone number formatting helper
    const phoneInputs = document.querySelectorAll('input[name*="phone"], input[name*="Phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.startsWith('0') && value.length === 10) {
                // Convert local Kenyan format to international
                this.value = '+254' + value.substring(1);
            } else if (value.startsWith('254') && value.length === 12) {
                this.value = '+' + value;
            }
        });
    });

    // Date picker min date (for drop-off dates - must be future)
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        input.setAttribute('min', today);
    });

    console.log('Phidelis Ann Foundation website loaded successfully.');
});
