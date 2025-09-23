const chatMessages = document.getElementById('chatMessages');
const welcomeContainer = document.getElementById('welcomeContainer');
const inputForm = document.getElementById('inputForm');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
let isThinking = false;

// Auto-resize textarea
if (userInput) {
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
}

function addMessage(sender, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    // Create message header
    const header = document.createElement('div');
    header.className = 'message-header';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'U' : 'AI';
    header.appendChild(avatar);

    const senderLabel = document.createElement('div');
    senderLabel.className = 'message-sender';
    senderLabel.textContent = sender === 'user' ? 'You' : 'EduHelp Pro';
    header.appendChild(senderLabel);

    messageDiv.appendChild(header);

    // Create content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (sender === 'user') {
        contentDiv.textContent = content;
    } else {
        // For bot messages, process HTML content and handle diagrams
        contentDiv.innerHTML = content.replace(/\n\n/g, '<br><br>').replace(/\n/g, '<br>');

        // Handle Kroki diagrams
        setTimeout(() => {
            const krokiImages = contentDiv.querySelectorAll('.kroki-diagram img');
            krokiImages.forEach((img, index) => {
                img.style.opacity = '0.6';
                img.style.transition = 'opacity 0.3s ease';

                img.onload = function() {
                    console.log(`Diagram ${index + 1} loaded successfully`);
                    this.style.opacity = '1';
                };

                img.onerror = function() {
                    console.error(`Failed to load diagram ${index + 1}`);
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'diagram-error';
                    errorDiv.innerHTML = '⚠️ Diagram could not be loaded';
                    this.parentElement.replaceChild(errorDiv, this);
                };

                setTimeout(() => {
                    if (!img.complete) {
                        img.onerror();
                    }
                }, 10000);
            });
        }, 100);
    }

    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    if (isThinking) return;

    isThinking = true;
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typing-indicator';

    // Create header for typing indicator
    const header = document.createElement('div');
    header.className = 'message-header';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = 'AI';
    header.appendChild(avatar);

    const senderLabel = document.createElement('div');
    senderLabel.className = 'message-sender';
    senderLabel.textContent = 'EduHelp Pro';
    header.appendChild(senderLabel);

    typingDiv.appendChild(header);

    // Create content with typing dots
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = '<div class="thinking-indicator"><span>Thinking</span><div class="thinking-dots"><div class="thinking-dot"></div><div class="thinking-dot"></div><div class="thinking-dot"></div></div></div>';
    typingDiv.appendChild(content);

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

    const text = message || (userInput ? userInput.value.trim() : '');
    if (!text) return;

    // Hide welcome container
    if (welcomeContainer) {
        welcomeContainer.style.display = 'none';
    }

    // Add user message
    addMessage('user', text);

    // Clear input
    if (!message && userInput) {
        userInput.value = '';
        userInput.style.height = 'auto';
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
        hideTypingIndicator();

        if (data.response) {
            addMessage('bot', data.response);
        } else {
            addMessage('bot', 'Sorry, I received an empty response. Please try again.');
        }

    } catch (error) {
        console.error('Chat error:', error);
        hideTypingIndicator();
        addMessage('bot', 'Sorry, I encountered an error. Please try again.');
    }
}

function signOut() {
    window.location.href = '/';
}

// Event listeners with null checks
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
    sendButton.addEventListener('click', function(e) {
        e.preventDefault();
        sendMessage();
    });
}

// Debug: Log when script loads
console.log('Chat.js loaded successfully');
console.log('Elements found:', {
    chatMessages: !!chatMessages,
    welcomeContainer: !!welcomeContainer,
    inputForm: !!inputForm,
    userInput: !!userInput,
    sendButton: !!sendButton
});