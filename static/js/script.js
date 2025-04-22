document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // Handle form submission
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get user message
        const userMessage = userInput.value.trim();
        if (!userMessage) return;
        
        // Add user message to chat
        addMessageToChat(userMessage, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Send message to backend
        sendMessage(userMessage);
    });

    function addMessageToChat(message, sender) {
        // Create message element
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        
        // Create message content
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = message;
        
        // Create timestamp
        const timeElement = document.createElement('div');
        timeElement.classList.add('message-time');
        timeElement.textContent = 'Just now';
        
        // Append elements
        messageElement.appendChild(contentElement);
        messageElement.appendChild(timeElement);
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage(message) {
        // Show loading indicator
        addMessageToChat('...', 'bot');
        
        // Send request to backend
        fetch('/api/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            chatMessages.removeChild(chatMessages.lastChild);
            
            // Add bot response
            addMessageToChat(data.bot_response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            // Remove loading indicator
            chatMessages.removeChild(chatMessages.lastChild);
            
            // Add error message
            addMessageToChat('Sorry, something went wrong. Please try again.', 'bot');
        });
    }
});