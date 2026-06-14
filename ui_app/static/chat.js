async function sendMessage() {
  const msgI = document.getElementById('message');
  const msg = msgI.value.trim();
  const role = document.getElementById('role').value;
  const uid = document.getElementById('user_id').value.trim();
  const cb = document.getElementById('chat-box');
  
  if (!msg || !uid) {
    alert('Enter ID and message!');
    return;
  }
  
  cb.innerHTML += '<div class="user-msg"><span>' + msg + '</span></div>';
  msgI.value = '';
  
  const lid = 'l-' + Date.now();
  cb.innerHTML += '<div class="ai-msg" id="' + lid + '"><span>Thinking...</span></div>';
  cb.scrollTop = cb.scrollHeight;
  
  try {
    const r = await fetch('http://localhost:8000/api/v1/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-user-role': role,
        'x-user-id': uid,
        'x-session-id': uid
      },
      body: JSON.stringify({ message: msg })
    });
    
    const d = await r.json();
    const loaderElem = document.getElementById(lid);
    if (loaderElem) {
      loaderElem.querySelector('span').textContent = d.response || 'No response';
    }
  } catch (e) {
    console.error("Chat Error:", e);
    const loaderElem = document.getElementById(lid);
    if (loaderElem) {
      loaderElem.querySelector('span').textContent = 'Error connecting.';
    }
  }
  cb.scrollTop = cb.scrollHeight;
}