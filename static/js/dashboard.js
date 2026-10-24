/* ==========================================================================
   Dashboard Interactive Logic & Chart.js Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Sidebar Toggle & Overlay Logic
  const menuToggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const sidebarOverlay = document.getElementById('sidebar-overlay');
  const sidebarCloseBtn = document.getElementById('sidebar-close-btn');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('active');
    if (sidebarOverlay) sidebarOverlay.classList.add('active');
    document.body.classList.add('sidebar-open');
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('active');
    if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    document.body.classList.remove('sidebar-open');
  }

  if (menuToggle) {
    menuToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (sidebar && sidebar.classList.contains('active')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  if (sidebarCloseBtn) {
    sidebarCloseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeSidebar();
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
      closeSidebar();
    });
  }

  // Close sidebar on mobile when navigating via a link
  if (sidebar) {
    const navLinks = sidebar.querySelectorAll('.sidebar-menu a, .sidebar-footer a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          closeSidebar();
        }
      });
    });
  }

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar && sidebar.classList.contains('active')) {
      closeSidebar();
    }
  });

  // Auto Dismiss Flash Messages after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // Chart.js Setup (Only runs if chart canvases are present)
  const lineCtx = document.getElementById('progressLineChart');
  const doughnutCtx = document.getElementById('categoryDoughnutChart');

  if (lineCtx && window.Chart) {
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    const textColor = isDark ? '#94a3b8' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';

    new Chart(lineCtx, {
      type: 'line',
      data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
        datasets: [{
          label: 'Interview Performance Score (%)',
          data: [68, 74, 82, 79, 89, 96],
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.15)',
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointBackgroundColor: '#8b5cf6'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          },
          y: {
            min: 50,
            max: 100,
            grid: { color: gridColor },
            ticks: { color: textColor }
          }
        }
      }
    });
  }

  if (doughnutCtx && window.Chart) {
    new Chart(doughnutCtx, {
      type: 'doughnut',
      data: {
        labels: ['Technical Coding', 'System Design', 'Behavioral / HR', 'Problem Solving'],
        datasets: [{
          data: [40, 25, 20, 15],
          backgroundColor: [
            '#6366f1',
            '#a855f7',
            '#10b981',
            '#f59e0b'
          ],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              padding: 15,
              color: document.documentElement.getAttribute('data-theme') !== 'light' ? '#94a3b8' : '#475569'
            }
          }
        },
        cutout: '72%'
      }
    });
  }
});
