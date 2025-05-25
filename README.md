# 🩺 Medquery-assistant : AI-Powered Medical Chat Assistant

**Medquery-assistant** is an intelligent, context-aware medical chatbot that enables users to interact naturally and get accurate, helpful medical responses. It uses the power of advanced language models (LLMs) to maintain conversation context and respond to both follow-up and fresh queries with precision.

---

## 🚀 Features

- 💬 **Conversational Interface:** Clean and intuitive chat UI built with HTML, CSS, and JavaScript.
- 🧠 **Context-Aware Responses:** Maintains and utilizes conversation history using a nested query mechanism.
- 🔄 **Nested Query Handling:** Enables follow-up questions to be answered with relevant context.
- ⚡ **Dual-Model Architecture:**
  - **Meta LLaMA 3.3 70B** – Powers nested queries with contextual understanding.
  - **Gemini 2.5 Flash** – Generates high-quality model responses in real-time.
- 🔐 **Secure & Efficient Backend:** Python-based backend for managing chat flow, model integration, and context management.

---

## 🧰 Tech Stack

| Layer       | Technology                      |
|------------|----------------------------------|
| Frontend   | HTML, CSS, JavaScript            |
| Backend    | FastAPI (Python) – handles API routes and server logic efficiently    |
| LLMs       | LLaMA 3.3 70B, Gemini 2.5 Flash   |
| Chat Logic | Custom context + nested query engine |

---

## 🛠️ How It Works

1. **User initiates a conversation** through the chat UI.
2. The system checks if the input is a **new question** or a **follow-up**.
3. For follow-ups, the backend retrieves the relevant **conversation context**.
4. **LLaMA 3.3 70B** handles the nested query resolution using conversation history.
5. The **refined prompt** is passed to **Gemini 2.5 Flash** to generate the final response.
6. The response is rendered on the frontend in real time.

---

## 📦 Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/meghana-choudhary/Medquery-assistant.git
cd Medquery-assistant
```
2. **Install Dependencies:**

```bash
pip install -r requirements.txt
```
3. **Create Environment File:** Create a file named .env in the root directory of the project.

4. **Add API Keys:** Open the .env file and add your API keys like this:

```bash
GROQ_API_KEY=YOUR_GROQ_API_KEY
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

5. **Run the Backend:**

```bash
python app.py
```
## 🧪 Example Use
👤: What are the symptoms of diabetes?

🤖: Common symptoms include frequent urination, increased thirst, and unexplained weight loss.

👤: And what about for children?

🤖: In children, symptoms may also include irritability, fatigue, and blurred vision...
