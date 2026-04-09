

# 🌿 Serene – AI Mental Health Companion

[](https://opensource.org/licenses/MIT)
[](https://fastapi.tiangolo.com/)
[](https://nodejs.org/)
[](https://www.mongodb.com/)
[](https://github.com/)

**Serene** is a modern, AI-driven mental health companion designed to provide a safe, empathetic space for emotional expression. By blending a beautiful UI with intelligent backend sentiment analysis, it bridges the gap between technology and emotional well-being.

> 🏆 Created for **Advaya Hackathon 2024** under the theme: *Improving Healthcare Through Technology*.

-----

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🧠 **Emotional Intelligence** | Simulates therapeutic journaling using Google Gemini & DeepSeek. |
| 📊 **Sentiment Analysis** | Real-time detection of emotional tones to adapt bot responses. |
| 🔐 **Secure Auth** | JWT-protected user accounts with encrypted password storage. |
| 🌓 **Adaptive UI** | Seamless Light/Dark mode transition for late-night journaling. |
| 🚨 **Crisis Detection** | Built-in triggers to detect emergency keywords and provide resources. |
| ⚡ **Dual-Engine** | Integration between Node.js (express) and Python (FastAPI). |

-----

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Frontend** | ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black) |
| **Backend** | ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB) |
| **Database** | ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) |
| **AI/ML** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75C2?style=for-the-badge&logo=googlegemini&logoColor=white) |

-----

## 🚀 Getting Started

### 1\. Prerequisites

  * **Node.js** (v14+)
  * **Python** (3.8+)
  * **MongoDB** (Running locally or on Atlas)

### 2\. Installation & Setup

```bash
# Clone the repository
git clone <repository-url>
cd Serene-Complete

# Install Node dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 3\. Environment Variables

Create a `.env` file in the root directory:

```ini
GEMINI_API_KEY=your_gemini_key
MONGODB_URI=mongodb://localhost:27017/serene
JWT_SECRET=your_secret_key
```

### 4\. Running the App

**The easy way:**

```powershell
./start.ps1  # For Windows users
```

**The manual way:**

  * Start Python API: `uvicorn deepseek_api:app --port 9000`
  * Start Node Server: `node server.js`

-----

## 🏗️ Architecture

The project uses a **multi-service architecture**:

1.  **Frontend:** Vanilla JS/HTML5 for maximum performance.
2.  **Node.js Server:** Handles Authentication, User Data, and History.
3.  **FastAPI (Python):** Handles the "Heavy Lifting" — AI inference and Sentiment Analysis.

-----

## 👥 Our Team — *Cache Me If You Can*

| Name | Role |
| :--- | :--- |
| **Aditya K** | Team Leader & Backend Architect |
| **Punarvi M U** | Frontend & UI/UX Design |
| **Rakshith H N** | AI Integration & API Design |
| **Sunidhi Srikanth Devaru** | Sentiment Analysis & Data Flow |

-----

## 🛡️ Security & Privacy

  * **Bcrypt:** All passwords are salted and hashed before storage.
  * **JWT:** Secure, stateless sessions for chat history.
  * **Emergency Protocol:** If the AI detects self-harm intent, it immediately provides helplines.

-----

\<p align="center"\>
Made with ❤️ by Team Cache Me If You Can
\</p\>

-----

### Tips for the "Visuals":

1.  **Badges:** I used shields.io badges. They make the repo look official.
2.  **Screenshots:** Replace the `[Image of...]` tags with actual screenshots of your app. Visual proof of a "Beautiful UI" is better than writing the words "Beautiful UI."
3.  **Emojis:** Use them to break up text and act as "bullets."
4.  **Tables:** Use tables for Team Members and Features; it's much easier to scan than a list.

Does this layout feel more aligned with the "Modern UI" vibe of your project?
