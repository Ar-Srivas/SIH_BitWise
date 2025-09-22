const chatMessages = document.getElementById('chatMessages');
const welcomeContainer = document.getElementById('welcomeContainer');
const inputForm = document.getElementById('inputForm');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
let isThinking = false;

// Auto-resize textarea
userInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Handle Enter key (Shift+Enter for new line)
userInput.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!isThinking && this.value.trim()) {
      inputForm.dispatchEvent(new Event('submit'));
    }
  }
});

function createMessage(sender, text, isThinking = false) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}`;

  const headerDiv = document.createElement('div');
  headerDiv.className = 'message-header';

  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'message-avatar';
  avatarDiv.textContent = sender === 'user' ? 'Y' : 'AI';

  const senderSpan = document.createElement('span');
  senderSpan.className = 'message-sender';
  senderSpan.textContent = sender === 'user' ? 'You' : 'EduHelp Pro';

  headerDiv.appendChild(avatarDiv);
  headerDiv.appendChild(senderSpan);

  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';

  if (isThinking) {
    contentDiv.innerHTML = `
      <div class="thinking-indicator">
        <span>Thinking</span>
        <div class="thinking-dots">
          <div class="thinking-dot"></div>
          <div class="thinking-dot"></div>
          <div class="thinking-dot"></div>
        </div>
      </div>
    `;
  } else {
    contentDiv.textContent = text;
  }

  messageDiv.appendChild(headerDiv);
  messageDiv.appendChild(contentDiv);
  return messageDiv;
}

function appendMessage(sender, text, isThinkingMsg = false) {
  // Remove welcome container if it exists
  if (welcomeContainer) {
    welcomeContainer.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => {
      welcomeContainer.remove();
    }, 300);
  }

  const messageElement = createMessage(sender, text, isThinkingMsg);
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return messageElement;
}

function setInputState(disabled) {
  userInput.disabled = disabled;
  sendButton.disabled = disabled;
  isThinking = disabled;
}

function sendSuggestion(text) {
  userInput.value = text;
  inputForm.dispatchEvent(new Event('submit'));
}

function signOut() {
  console.log('Signing out...');
  // Add your sign out logic here
}

inputForm.addEventListener('submit', async function(e) {
  e.preventDefault();
  const text = userInput.value.trim();
  if (!text || isThinking) return;

  // Add user message
  appendMessage('user', text);

  // Clear input and reset height
  userInput.value = '';
  userInput.style.height = 'auto';

  // Disable input during processing
  setInputState(true);

  // Show thinking message
  const thinkingMessage = appendMessage('bot', '', true);

  try {
    // Connect to your backend chat API
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_message: text })
    });

    const data = await response.json();

    // Remove thinking message
    thinkingMessage.remove();

    // Add bot response with typing effect
    const botMessage = appendMessage('bot', '');
    typeMessage(botMessage.querySelector('.message-content'), data.response);

  } catch (error) {
    // Remove thinking message
    thinkingMessage.remove();

    // Add error message
    appendMessage('bot', 'Sorry, there was an error processing your request. Please try again.');
    console.error('Chat error:', error);
  } finally {
    // Re-enable input
    setInputState(false);
    userInput.focus();
  }
});

function typeMessage(element, text, speed = 30) {
  element.textContent = '';
  let i = 0;
  const timer = setInterval(() => {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      chatMessages.scrollTop = chatMessages.scrollHeight;
    } else {
      clearInterval(timer);
    }
  }, speed);
}

// Focus input on load
window.addEventListener('load', () => {
  userInput.focus();
});

// Add CSS animation keyframes for fadeOut
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeOut {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(-20px); }
  }
`;
document.head.appendChild(style);