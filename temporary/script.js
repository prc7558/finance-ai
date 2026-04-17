document.addEventListener('DOMContentLoaded', function() {

  // ---------------- TAB SWITCHING ----------------
  const tabs = document.querySelectorAll('.tab');
  const contents = document.querySelectorAll('.tab-content');

  function openTab(tabName) {
    tabs.forEach(tab => {
      const isActive = tab.dataset.tab === tabName;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });
    contents.forEach(content => {
      const isActive = content.id === tabName;
      content.classList.toggle('active', isActive);
      content.setAttribute('aria-hidden', isActive ? 'false' : 'true');
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      openTab(tab.dataset.tab);
      try { history.replaceState(null, '', '#' + tab.dataset.tab); } catch(e) {}
    });
  });

  const hash = location.hash.replace('#', '');
  openTab(hash && document.getElementById(hash) ? hash : 'dashboard');

  // ---------------- CHAT FUNCTIONALITY ----------------
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');

  sendBtn.addEventListener('click', () => {
    const msg = chatInput.value.trim();
    if (!msg) return;

    appendChatMessage('You', msg);

    chatInput.value = '';

    // Send question to Flask backend
    fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ question: msg })
    })
    .then(res => res.json())
    .then(data => {
      appendChatMessage('AI', data.answer || 'No response available.');
    })
    .catch(err => {
      console.error(err);
      appendChatMessage('AI', 'Error: Could not get response.');
    });
  });

  function appendChatMessage(sender, text) {
    const chatDiv = document.createElement('div');
    chatDiv.className = 'chat-message';
    chatDiv.textContent = `${sender}: ${text}`;
    const chatCard = document.querySelector('#chat .chat-card');
    chatCard.appendChild(chatDiv);
    chatCard.scrollTop = chatCard.scrollHeight;
  }

  // ---------------- CSV UPLOAD ----------------
  const uploadBtn = document.getElementById('uploadBtn');
  uploadBtn.addEventListener('click', () => {
    const fileInput = document.getElementById('csvFile');
    if (!fileInput.files.length) return alert('Please select a CSV file.');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      if (data.summary) {
        document.getElementById('csvSummary').innerHTML = `
          CSV Loaded: ${data.summary.rows} rows × ${data.summary.columns.length} columns.<br>
          Preview: <pre>${JSON.stringify(data.summary.preview, null, 2)}</pre>
        `;
      } else {
        alert('Error processing CSV.');
      }
    })
    .catch(err => {
      console.error(err);
      alert('Failed to upload CSV.');
    });
  });

});
