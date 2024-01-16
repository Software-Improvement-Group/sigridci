document.getElementById('chatbot-send').addEventListener('click', function() {
    var userInput = document.getElementById('chatbot-input').value;
    if (userInput.trim() !== '') {
        sendMessageToServer(userInput);
        document.getElementById('chatbot-input').value = '';
    }
});

function sendMessageToServer(message) {
    console.log("Sending....")
    displayMessage("User: "+message);
    // Show typing indicator
    document.getElementById('chatbot-typing').style.display = 'block';
    // Example POST request with Fetch API
    fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message, history: [] }),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayMessage("SigridBot: "+data.reply);
        })
        .catch((error) => {
            console.error('Error:', error);
        })
        .finally(() => {
            // Hide typing indicator
            document.getElementById('chatbot-typing').style.display = 'none';
        });
}

function displayMessage(message) {
    var messagesContainer = document.getElementById('chatbot-messages');
    var newMessageDiv = document.createElement('div');
    newMessageDiv.textContent = message;
    messagesContainer.appendChild(newMessageDiv);

    // Scroll to the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
