let jwtToken = "";

function saveToken() {
    const token = document.getElementById('tokenInput').value;
    if (token) {
        jwtToken = token;
        alert('JWT Token saved securely in memory!');
    }
}

function appendMessage(text, isUser, meta = "") {
    const chatbox = document.getElementById('chatbox');
    
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerText = isUser ? '👤' : '🤖';
    
    const contentBox = document.createElement('div');
    
    const content = document.createElement('div');
    content.className = 'content';
    // Use marked.js or similar if you want markdown, for now simple text formatting
    content.innerHTML = text.replace(/\n/g, '<br>');
    
    contentBox.appendChild(content);
    
    if (meta) {
        const metaSpan = document.createElement('span');
        metaSpan.className = 'meta';
        metaSpan.innerText = meta;
        contentBox.appendChild(metaSpan);
    }
    
    msgDiv.appendChild(avatar);
    msgDiv.appendChild(contentBox);
    
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage(presetMsg = null) {
    const input = document.getElementById('userInput');
    const msg = presetMsg || input.value;
    
    if (!msg.trim()) return;
    
    appendMessage(msg, true);
    input.value = '';
    
    // Show typing indicator
    const typingId = 'typing-' + Date.now();
    const chatbox = document.getElementById('chatbox');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message';
    typingDiv.id = typingId;
    typingDiv.innerHTML = `<div class="avatar">🤖</div><div class="content">Thinking...</div>`;
    chatbox.appendChild(typingDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
    
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Mode 1: JWT
        if (jwtToken) {
            headers['Authorization'] = `Bearer ${jwtToken}`;
        } 
        // Mode 2: Dev Fallback
        else {
            headers['x-user-role'] = document.getElementById('roleSelect').value;
            headers['x-user-id'] = document.getElementById('userIdInput').value;
        }

        // Dynamically get the API URL (usually port 8000 on the same host)
        const apiUrl = `http://${window.location.hostname}:8000/api/v1/chat`;
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ message: msg })
        });
        
        document.getElementById(typingId).remove();
        
        if (!response.ok) {
            const err = await response.json();
            appendMessage(`Error: ${err.detail || 'Authentication failed. Please check your token or role.'}`, false);
            return;
        }
        
        const data = await response.json();
        
        // Add meta tags for intent and latency
        let meta = "";
        if (data.intent && data.time) {
            meta = `Intent: [${data.intent}] • Latency: ${data.time}`;
        }
        
        appendMessage(data.response, false, meta);
        
    } catch (error) {
        document.getElementById(typingId).remove();
        appendMessage(`Connection Error (${error.message}): Is the FastAPI server running on port 8000?`, false);
    }
}

function handleKeyPress(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}