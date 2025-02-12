document.getElementById('chatbot-send').addEventListener('click', function() {
    var userInput = document.getElementById('chatbot-input').value;
    if (userInput.trim() !== '') {
        sendMessageToServer(userInput);
        document.getElementById('chatbot-input').value = '';
    }
});

function sendMessageToServer(message) {
    console.log("Sending....")
    var newMessageDiv = document.createElement('div');
    var messagesContainer = document.getElementById('chatbot-messages');
    messagesContainer.appendChild(newMessageDiv);
    displayMessage(newMessageDiv, messagesContainer,"User: "+message);

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
        .then(async response => {
            var newMessageDiv = document.createElement('div');
            var messagesContainer = document.getElementById('chatbot-messages');
            messagesContainer.appendChild(newMessageDiv);
            displayMessage(newMessageDiv, messagesContainer,"SigridBot: ");

            const reader = response.body.getReader();
            while (true) {
                await new Promise(resolve => setTimeout(resolve, 80));

                const {done, value} = await reader.read();
                if (done) break;
                console.log(new TextDecoder().decode(value));
                displayMessage(newMessageDiv, messagesContainer, new TextDecoder().decode(value));
                // Process each chunk of data here
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        })
        .finally(() => {
            // Hide typing indicator
            document.getElementById('chatbot-typing').style.display = 'none';
        });
}

function displayMessage(newMessageDiv,messagesContainer, message) {
    newMessageDiv.textContent += message;
    newMessageDiv.textContent += '\n';

    // Scroll to the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
