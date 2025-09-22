const chatMessages = document.getElementById('chatMessages');
const welcomeContainer = document.getElementById('welcomeContainer');
const inputForm = document.getElementById('inputForm');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
let isThinking = false;

// Initialize Mermaid with proper configuration
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  themeVariables: {
    primaryColor: '#667eea',
    primaryTextColor: '#374151',
    primaryBorderColor: '#667eea',
    lineColor: '#6b7280',
    sectionBkgColor: '#f8fafc',
    altSectionBkgColor: '#e2e8f0',
    gridColor: '#e5e7eb',
    tertiaryColor: '#f1f5f9',
    background: '#ffffff',
    secondaryColor: '#f3f4f6',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  },
  flowchart: {
    htmlLabels: true,
    curve: 'basis',
    padding: 15
  }
});

// Auto-resize textarea
userInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

function addMessage(sender, content) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}`;

  if (sender === 'user') {
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
  } else {
    // For bot messages, process mermaid diagrams
    renderMermaidContent(messageDiv, content);
  }

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function renderMermaidContent(element, content) {
  const mermaidRegex = /```mermaid\n([\s\S]*?)\n```/g;
  let processedContent = content;
  const matches = [...content.matchAll(mermaidRegex)];

  if (matches.length > 0) {
    for (let i = 0; i < matches.length; i++) {
      const fullMatch = matches[i][0];
      const mermaidCode = matches[i][1];
      const diagramId = `mermaid-diagram-${Date.now()}-${i}`;

      try {
        const { svg } = await mermaid.render(diagramId, mermaidCode);
        const diagramType = detectDiagramType(mermaidCode);
        const diagramContainer = `<div class="mermaid-container ${diagramType}-diagram">${svg}</div>`;
        processedContent = processedContent.replace(fullMatch, diagramContainer);
      } catch (error) {
        console.error('Mermaid render error:', error);
        processedContent = processedContent.replace(fullMatch,
          `<div class="code-block diagram-error">Diagram could not be rendered</div>`);
      }
    }
  }

  // Format the text content with proper line breaks
  processedContent = processedContent.replace(/\n/g, '<br>');
  element.innerHTML = processedContent;
  chatMessages.appendChild(element);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function detectDiagramType(mermaidCode) {
  const code = mermaidCode.toLowerCase().trim();

  if (code.startsWith('flowchart') || code.startsWith('graph')) {
    return 'flowchart';
  } else if (code.startsWith('timeline')) {
    return 'timeline';
  } else if (code.startsWith('journey')) {
    return 'journey';
  } else if (code.startsWith('mindmap')) {
    return 'mindmap';
  } else if (code.startsWith('sequencediagram') || code.startsWith('sequenceDiagram')) {
    return 'sequence';
  } else if (code.startsWith('classDiagram')) {
    return 'class';
  } else if (code.startsWith('stateDiagram')) {
    return 'state';
  } else if (code.startsWith('pie')) {
    return 'pie';
  } else if (code.startsWith('gantt')) {
    return 'gantt';
  }

  return 'flowchart';
}

function showTypingIndicator() {
  if (isThinking) return;

  isThinking = true;
  const typingDiv = document.createElement('div');
  typingDiv.className = 'message bot typing';
  typingDiv.id = 'typing-indicator';
  typingDiv.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
  const typingIndicator = document.getElementById('typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
  isThinking = false;
}

function sendSuggestion(suggestion) {
  if (welcomeContainer) {
    welcomeContainer.style.display = 'none';
  }
  sendMessage(suggestion);
}

async function sendMessage(message) {
  if (isThinking) return;

  const text = message || userInput.value.trim();
  if (!text) return;

  // Hide welcome container if it exists
  if (welcomeContainer) {
    welcomeContainer.style.display = 'none';
  }

  // Add user message
  addMessage('user', text);

  // Clear input
  if (!message) {
    userInput.value = '';
  }

  // Show typing indicator
  showTypingIndicator();

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_message: text })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Hide typing indicator
    hideTypingIndicator();

    // Add bot response
    addMessage('bot', data.response);

  } catch (error) {
    console.error('Chat error:', error);
    hideTypingIndicator();
    addMessage('bot', 'Sorry, I encountered an error. Please try again.');
  }
}

function signOut() {
  window.location.href = '/';
}

// Event listeners
if (inputForm) {
  inputForm.addEventListener('submit', function(e) {
    e.preventDefault();
    sendMessage();
  });
}

if (userInput) {
  userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}

if (sendButton) {
  sendButton.addEventListener('click', function() {
    sendMessage();
  });
}