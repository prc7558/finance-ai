// Chart.js configurations and rendering

let categoryChart = null;
let monthlyChart = null;
let dailyChart = null;

function getChartColors(theme) {
  if (theme === 'dark') {
    return {
      primary: '#3b82f6',
      success: '#10b981',
      warning: '#f59e0b',
      danger: '#ef4444',
      info: '#06b6d4',
      purple: '#a855f7',
      pink: '#ec4899',
      text: '#f1f5f9',
      grid: '#334155'
    };
  }
  return {
    primary: '#2563eb',
    success: '#059669',
    warning: '#d97706',
    danger: '#dc2626',
    info: '#0891b2',
    purple: '#9333ea',
    pink: '#db2777',
    text: '#1e293b',
    grid: '#e2e8f0'
  };
}

function renderCategoryChart(categories) {
  const canvas = document.getElementById('categoryChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  const colors = getChartColors(theme);
  
  // Destroy existing chart
  if (categoryChart) {
    categoryChart.destroy();
  }
  
  const labels = Object.keys(categories);
  const data = Object.values(categories);
  
  const backgroundColors = [
    colors.primary,
    colors.success,
    colors.warning,
    colors.danger,
    colors.info,
    colors.purple,
    colors.pink,
    '#6366f1',
    '#8b5cf6',
    '#14b8a6'
  ];
  
  categoryChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: backgroundColors,
        borderWidth: 2,
        borderColor: theme === 'dark' ? '#1e293b' : '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: colors.text,
            padding: 10,
            font: {
              size: 11
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.parsed || 0;
              return label + ': ₹' + value.toLocaleString('en-IN');
            }
          }
        }
      }
    }
  });
}

function renderMonthlyChart(monthlySummary) {
  const canvas = document.getElementById('monthlyChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  const colors = getChartColors(theme);
  
  // Destroy existing chart
  if (monthlyChart) {
    monthlyChart.destroy();
  }
  
  const labels = Object.keys(monthlySummary);
  const data = Object.values(monthlySummary);
  
  monthlyChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Net Amount',
        data: data,
        backgroundColor: data.map(val => val >= 0 ? colors.success : colors.danger),
        borderColor: data.map(val => val >= 0 ? colors.success : colors.danger),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.parsed.y || 0;
              return 'Net: ₹' + value.toLocaleString('en-IN');
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: colors.grid
          },
          ticks: {
            color: colors.text,
            callback: function(value) {
              return '₹' + value.toLocaleString('en-IN', { notation: 'compact' });
            }
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: colors.text
          }
        }
      }
    }
  });
}

function renderDailyChart(dailySpending) {
  const canvas = document.getElementById('dailyChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  const colors = getChartColors(theme);
  
  // Destroy existing chart
  if (dailyChart) {
    dailyChart.destroy();
  }
  
  const labels = Object.keys(dailySpending);
  const data = Object.values(dailySpending);
  
  dailyChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Daily Net Amount',
        data: data,
        borderColor: colors.primary,
        backgroundColor: colors.primary + '20',
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.parsed.y || 0;
              return '₹' + value.toLocaleString('en-IN');
            }
          }
        }
      },
      scales: {
        y: {
          grid: {
            color: colors.grid
          },
          ticks: {
            color: colors.text,
            callback: function(value) {
              return '₹' + value.toLocaleString('en-IN', { notation: 'compact' });
            }
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: colors.text,
            maxRotation: 45,
            minRotation: 45,
            font: {
              size: 10
            }
          }
        }
      }
    }
  });
}

async function loadChartsData() {
  try {
    const response = await fetch('/api/dashboard');
    const data = await response.json();
    
    if (data.categories && Object.keys(data.categories).length > 0) {
      renderCategoryChart(data.categories);
    }
    
    if (data.monthly_summary && Object.keys(data.monthly_summary).length > 0) {
      renderMonthlyChart(data.monthly_summary);
    }
    
    if (data.daily_spending && Object.keys(data.daily_spending).length > 0) {
      renderDailyChart(data.daily_spending);
    }
  } catch (error) {
    console.error('Error loading charts data:', error);
  }
}

// Update charts when theme changes
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.attributeName === 'data-theme') {
      // Reload charts with new theme colors
      loadChartsData();
    }
  });
});

observer.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ['data-theme']
});

// Export functions
if (typeof window !== 'undefined') {
  window.renderCategoryChart = renderCategoryChart;
  window.renderMonthlyChart = renderMonthlyChart;
  window.renderDailyChart = renderDailyChart;
  window.loadChartsData = loadChartsData;
}
