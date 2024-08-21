document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("chat-form");
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");

    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const query = userInput.value;
            if (query.trim() === "") return;

            const userMessage = document.createElement("div");
            userMessage.textContent = "用户: " + query;
            chatBox.appendChild(userMessage);

            fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "query=" + encodeURIComponent(query)
            })
            .then(response => response.json())
            .then(data => {
                const responseMessage = document.createElement("div");
                responseMessage.textContent = "客服: " + data.response;
                chatBox.appendChild(responseMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            });

            userInput.value = "";
        });
    }

    const voiceButton = document.getElementById("voice-button");
    if (voiceButton) {
        voiceButton.addEventListener("mousedown", function() {
            fetch("/voice_query", {
                method: "POST"
            })
            .then(response => response.json())
            .then(data => {
                const userMessage = document.createElement("div");
                userMessage.textContent = "用户: " + data.query;
                chatBox.appendChild(userMessage);

                const responseMessage = document.createElement("div");
                responseMessage.textContent = "客服: " + data.response;
                chatBox.appendChild(responseMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        });
    }
});
