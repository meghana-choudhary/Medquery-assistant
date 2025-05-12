document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
    });
  });
});

// Initialize chat with a welcome message
window.onload = function () {
  addMessage("Hi! I'm MedBot. How can I help you today?", "bot");
};

function formatMessage(text) {
  // Format bold text (enclosed in **)
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Convert numbered lists with : to proper HTML list items
  text = text.replace(/(\d+\. \*\*.*?\*\*:)/g, "<strong>$1</strong>");

  // Convert line breaks to <br> tags
  text = text.replace(/\n/g, "<br>");

  return text;
}

function addMessage(text, sender) {
  const chatMessages = document.getElementById("chat-messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src =
    sender === "bot"
      ? "https://cdn-icons-png.flaticon.com/512/4712/4712027.png"
      : "https://cdn-icons-png.flaticon.com/512/1144/1144760.png";

  const messageContent = document.createElement("div");
  messageContent.className = "message-content";
  messageContent.innerHTML = formatMessage(text);

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(messageContent);

  // Add the new message class for animation
  messageDiv.classList.add("new");
  chatMessages.appendChild(messageDiv);

  // Scroll to the bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // Remove the new class after animation
  setTimeout(() => {
    messageDiv.classList.remove("new");
  }, 100);
}

function getUserMessagesString() {
  const chatMessages = document.getElementById("chat-messages");
  const userMessages = chatMessages.querySelectorAll(".user .message-content");
  let pastQueries = "";

  userMessages.forEach((msg, index) => {
    pastQueries += `${index + 1}. ${msg.textContent.trim()}\n`;
  });

  return pastQueries.trim();
}

async function sendMessage() {
  let queries = getUserMessagesString();

  const inputElement = document.getElementById("user-input");
  const userMessage = inputElement.value.trim();

  if (userMessage === "") return;

  // Add user message to chat
  addMessage(userMessage, "user");
  inputElement.value = "";

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ history: queries, message: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    addMessage(data.response, "bot");
  } catch (error) {
    console.error("Error:", error);
    addMessage("Sorry, I encountered an error. Please try again.", "bot");
  }
}

// Allow sending message with Enter key
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      // let queries=getUserMessagesString();
      // console.log(typeof(queries))
      sendMessage();
    }
  });
