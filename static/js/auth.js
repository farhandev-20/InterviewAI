/* ==========================================================================
   Authentication & Form Interactive Script
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Show / Hide Password toggle
  const togglePassBtns = document.querySelectorAll('.toggle-password');
  togglePassBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.previousElementSibling || document.getElementById(btn.getAttribute('data-target'));
      if (input) {
        if (input.type === 'password') {
          input.type = 'text';
          btn.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
          input.type = 'password';
          btn.classList.replace('fa-eye-slash', 'fa-eye');
        }
      }
    });
  });

  // Password Strength Meter (Register Page)
  const passwordInput = document.getElementById('password');
  const strengthBar = document.getElementById('strength-bar');

  if (passwordInput && strengthBar) {
    passwordInput.addEventListener('input', () => {
      const val = passwordInput.value;
      let score = 0;

      if (val.length >= 8) score += 25;
      if (/[A-Z]/.test(val)) score += 25;
      if (/[0-9]/.test(val)) score += 25;
      if (/[^A-Za-z0-9]/.test(val)) score += 25;

      strengthBar.style.width = score + '%';
      if (score <= 25) {
        strengthBar.style.backgroundColor = '#f43f5e'; // Red
      } else if (score <= 50) {
        strengthBar.style.backgroundColor = '#f59e0b'; // Amber
      } else if (score <= 75) {
        strengthBar.style.backgroundColor = '#3b82f6'; // Blue
      } else {
        strengthBar.style.backgroundColor = '#10b981'; // Green
      }
    });
  }

  // Forgot Password Modal UI Trigger
  const forgotTrigger = document.getElementById('forgot-password-trigger');
  const forgotModal = document.getElementById('forgot-password-modal');
  const closeModalBtn = document.getElementById('close-modal-btn');

  if (forgotTrigger && forgotModal) {
    forgotTrigger.addEventListener('click', (e) => {
      e.preventDefault();
      forgotModal.classList.add('active');
    });

    if (closeModalBtn) {
      closeModalBtn.addEventListener('click', () => {
        forgotModal.classList.remove('active');
      });
    }

    forgotModal.addEventListener('click', (e) => {
      if (e.target === forgotModal) {
        forgotModal.classList.remove('active');
      }
    });
  }
});
