# 🤖 GenAI Tool-Using Agent (Dockerized)

This is a Python-based AI agent that can answer your questions, use tools like Wikipedia search, weather, joke fetching, IP lookup, and more. It leverages Google Gemini's API and is containerized with Docker for easy setup and usage.

---

## 🧠 Features

- 🔍 Search Wikipedia
- 🌤️ Fetch real-time weather
- 📖 Define words
- 🎲 Roll a dice
- 😂 Tell jokes
- 🌐 Get public IP
- 📅 Show today's date
- 🧪 Generate UUID
- 📡 Ping websites for IP

---

## 🚀 How to Run with Docker

### 📦 Pull the Docker Image

```bash
docker pull akshaydev07/genai-agent
```

### 🔐 Set Your Gemini API Key

This agent uses the Gemini API from Google. You need an API key.

#### Option 1: Using `.env` file

1. Create a `.env` file in the same directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

2. Run the container:
   ```bash
   docker run -it --env-file .env akshaydev07/genai-agent
   ```

#### Option 2: Using `--env` flag

```bash
docker run -it --env GEMINI_API_KEY=your_gemini_api_key_here akshaydev07/genai-agent
```

---

## 🛠️ Technologies Used

- **Python 3.11** — Main programming language
- **Docker** — For containerization and deployment
- **Google Generative AI (Gemini API)** — Core AI processing
- **Requests** — For making API calls
- **python-dotenv** — For managing environment variables
- **Wikipedia API** — For search and summaries
- **Dictionary API** — For word definitions
- **wttr.in** — For weather data
- **Official Joke API** — For jokes and fun responses

---
## 💻 Example Query

```bash
Enter your query > What is the weather in Delhi?
```

The agent will walk through step-by-step reasoning and tool invocation and return the result.

---

## 📁 Project Structure

```
.
├── agent.py             # Main Python script
├── Dockerfile           # Docker build file
├── requirements.txt     # Python dependencies
├── .env.example         # Sample environment variable file
```

---

🌐 Docker Hub
-----------

[→ Docker Hub: akshaydev07/genai-agent](https://hub.docker.com/repository/docker/akshaydev07/genai-agent)

---

🔗 GitHub Repository
--------------------

[→ GitHub: akshaydev07/genai-agent](https://github.com/akshay0712-dev/GenAI/tree/main/AI%20Agent)

---

📋 License
----------

This project is open-source and free to use.
