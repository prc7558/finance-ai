// Main application JavaScript

// Global state
let currentAccounts = [];
let dashboardData = null;

// Get translation function
function t(key) {
  const lang = window.getCurrentLang ? window.getCurrentLang() : 'en';
  return window.translations && window.translations[lang] && window.translations[lang][key] 
    ? window.translations[lang][key] 
    : key;
}

// Tab switching
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const tabName = tab.dataset.tab;
      
      // Update tabs
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      
      tab.classList.add('active');
      document.getElementById(tabName).classList.add('active');
      
      // Load data when switching to specific tabs
      if (tabName === 'dashboard') {
        loadDashboard();
      } else if (tabName === 'accounts') {
        loadAccounts();
      } else if (tabName === 'charts') {
        if (window.loadChartsData) {
          window.loadChartsData();
        }
      }
    });
  });

  // Load initial data
  loadDashboard();
  
  // Setup chat
  document.getElementById('sendBtn').addEventListener('click', sendMessage);
  document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
  
  // Setup upload form
  document.getElementById('uploadForm').addEventListener('submit', uploadCSV);
  
  // Setup export button
  document.getElementById('exportPdfBtn').addEventListener('click', exportPDF);
});

// Load dashboard data
async function loadDashboard() {
  try {
    const response = await fetch('/api/dashboard');
    const data = await response.json();
    dashboardData = data;
    
    document.getElementById('totalBalance').textContent = `₹${data.total_balance.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
    document.getElementById('totalIncome').textContent = `₹${data.total_income.toLocaleString('en-IN')}`;
    document.getElementById('totalExpenses').textContent = `₹${data.total_expenses.toLocaleString('en-IN')}`;
    document.getElementById('accountCount').textContent = data.account_count || 0;
    
    const netChange = data.net_change;
    const netChangeText = netChange >= 0 ? 
      `+₹${Math.abs(netChange).toLocaleString('en-IN')} ${t('this_period')}` :
      `-₹${Math.abs(netChange).toLocaleString('en-IN')} ${t('this_period')}`;
    document.getElementById('netChange').textContent = netChangeText;
    
    // Display insights
    const insightsContainer = document.getElementById('insightsContainer');
    if (data.insights && data.insights.length > 0) {
      insightsContainer.innerHTML = `<div class="section-title" data-i18n="financial_insights">${t('financial_insights')}</div>`;
      data.insights.forEach(insight => {
        const div = document.createElement('div');
        div.className = insight.type;
        div.innerHTML = `<strong>${escapeHTML(insight.title)}:</strong> ${escapeHTML(insight.message)}`;
        insightsContainer.appendChild(div);
      });
    } else {
      insightsContainer.innerHTML = `<div class="section-title" data-i18n="financial_insights">${t('financial_insights')}</div><div class="loading" data-i18n="upload_data_prompt">${t('upload_data_prompt')}</div>`;
    }
    
    // Update chat status
    const accountText = data.account_count || 0;
    document.getElementById('chatStatus').textContent = `● ${t('ready_to_help').replace('● ', '')}`;
    
  } catch (error) {
    console.error('Error loading dashboard:', error);
  }
}

// Load accounts
async function loadAccounts() {
  try {
    const response = await fetch('/api/accounts');
    const data = await response.json();
    currentAccounts = data.accounts || [];
    
    const accountsList = document.getElementById('accountsList');
    
    if (currentAccounts.length === 0) {
      accountsList.innerHTML = `<div class="loading" data-i18n="no_accounts">${t('no_accounts')}</div>`;
      return;
    }
    
    accountsList.innerHTML = '';
    currentAccounts.forEach(account => {
      const div = document.createElement('div');
      div.className = 'account';
      div.innerHTML = `
        <div class="account-info">
          <strong>${escapeHTML(account.bank_name)}</strong>
          <span>${account.account_type} • ${account.rows} ${t('transactions')}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
          <div class="amount-small ${account.balance >= 0 ? 'positive' : 'negative'}">
            ₹${Math.abs(account.balance).toLocaleString('en-IN', {minimumFractionDigits: 2})}
          </div>
          <button class="delete-account" onclick="deleteAccount(${account.id})" data-i18n="delete">${t('delete')}</button>
        </div>
      `;
      accountsList.appendChild(div);
    });
    
  } catch (error) {
    console.error('Error loading accounts:', error);
  }
}

// Delete account
async function deleteAccount(accountId) {
  if (!confirm(t('confirm_delete'))) return;
  
  try {
    const response = await fetch(`/api/accounts/${accountId}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      loadAccounts();
      loadDashboard();
      alert(t('account_deleted'));
    }
  } catch (error) {
    console.error('Error deleting account:', error);
    alert(t('upload_failed'));
  }
}

// Upload CSV
async function uploadCSV(e) {
  e.preventDefault();
  
  const uploadBtn = document.getElementById('uploadBtn');
  const formData = new FormData();
  
  formData.append('file', document.getElementById('csvFile').files[0]);
  formData.append('bank_name', document.getElementById('bankName').value);
  formData.append('account_type', document.getElementById('accountType').value);
  
  uploadBtn.disabled = true;
  uploadBtn.textContent = t('loading');
  
  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (data.success) {
      alert(t('account_connected'));
      document.getElementById('uploadForm').reset();
      loadAccounts();
      loadDashboard();
    } else {
      alert('Error: ' + (data.error || t('upload_failed')));
    }
  } catch (error) {
    console.error('Error uploading:', error);
    alert(t('upload_failed'));
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.textContent = t('upload_connect');
  }
}

// Chat functionality
async function sendMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  
  if (!message) return;
  
  appendChatMessage('user', message);
  input.value = '';
  
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ question: message })
    });
    
    const data = await response.json();
    appendChatMessage('ai', data.answer || 'No response available.');
  } catch (error) {
    console.error('Error:', error);
    appendChatMessage('ai', t('error_occurred'));
  }
}

function appendChatMessage(sender, text) {
  const messagesContainer = document.getElementById('chatMessages');
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('chat-message', sender);
  messageDiv.innerHTML = formatText(text);
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function formatText(text) {
  const escaped = escapeHTML(text);
  return escaped
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");
}

// Export PDF
async function exportPDF() {
  const btn = document.getElementById('exportPdfBtn');
  btn.disabled = true;
  btn.innerHTML = `<span>⏳</span><span>${t('loading')}</span>`;
  
  try {
    const response = await fetch('/export-pdf');
    
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `financial_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      
      alert(t('pdf_generated'));
    } else {
      const data = await response.json();
      alert('Error: ' + (data.error || t('pdf_failed')));
    }
  } catch (error) {
    console.error('Error:', error);
    alert(t('pdf_failed'));
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span style="font-size: 20px;">📥</span><span data-i18n="download_pdf">${t('download_pdf')}</span>`;
  }
}

// Make deleteAccount available globally
window.deleteAccount = deleteAccount;
