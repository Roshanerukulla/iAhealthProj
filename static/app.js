function sendMessage(event) {
    event.preventDefault();  // Prevent form submission (if in a form)
    
    let userMessage = document.getElementById('user-input').value;  // Get user input
    
    // Append user message to the chat box
    appendMessage(userMessage, 'user');

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Send POST request to Flask backend
    fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userMessage })
    })
    .then(response => response.json())  // Convert response to JSON
    .then(data => {
        // Append bot's response along with citations
        appendMessage(data.answer, 'bot', data.sources);
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage("Sorry, something went wrong.", 'bot');
    });
}

function appendMessage(message, sender, sources = []) {
    let chatBox = document.getElementById('chat-box');

    let messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);

    // Append sources if available (for bot responses)
    if (sender === 'bot' && sources.length > 0) {
        let sourcesDiv = document.createElement('div');
        sourcesDiv.classList.add('citation');
        sourcesDiv.innerHTML = "<strong>Sources:</strong> " + sources.map(src => `<a href='${src}' target='_blank'>${src}</a>`).join(', ');
        chatBox.appendChild(sourcesDiv);
    }

    // Scroll to the bottom of the chat
    chatBox.scrollTop = chatBox.scrollHeight;
}
