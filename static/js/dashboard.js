/* ==========================================================================
   Dashboard Interactive Logic & Chart.js Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Sidebar Toggle
  const menuToggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
  }

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
