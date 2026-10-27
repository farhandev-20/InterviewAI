/* ==========================================================================
   Theme Switcher Engine (Dark / Light Mode)
   Default: Dark Mode
   Saved in LocalStorage
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const THEME_KEY = 'interviewai_theme';
  const html = document.documentElement;

  // Retrieve stored theme or default to dark
  const savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
  applyTheme(savedTheme);

  // Bind theme toggle buttons across pages
  const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
  toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const currentTheme = html.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
    });
  });

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);

    // Update button icons if present
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    toggleBtns.forEach(btn => {
      const icon = btn.querySelector('i');
      if (icon) {
        if (theme === 'dark') {
          icon.className = 'fas fa-sun';
          btn.setAttribute('title', 'Switch to Light Mode');
        } else {
          icon.className = 'fas fa-moon';
          btn.setAttribute('title', 'Switch to Dark Mode');
        }
      }
    });
  }

  // Global Flash Messages Auto-Dismiss & Close Handlers
  function dismissAlert(alertEl) {
    if (!alertEl || alertEl.dataset.dismissing === 'true') return;
    alertEl.dataset.dismissing = 'true';
    alertEl.style.opacity = '0';
    alertEl.style.transform = 'translateY(-10px)';
    alertEl.style.transition = 'opacity 0.35s ease, transform 0.35s ease, margin 0.35s ease, max-height 0.35s ease';
    setTimeout(() => {
      if (alertEl.parentNode) alertEl.remove();
    }, 360);
  }

  const alerts = document.querySelectorAll('.flash-messages .alert');
  alerts.forEach(alert => {
    // Dismiss button click
    const closeBtn = alert.querySelector('.alert-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dismissAlert(alert);
      });
    }

    // Auto-dismiss after 4 seconds
    setTimeout(() => {
      dismissAlert(alert);
    }, 4000);
  });
});
