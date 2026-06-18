# Veritas AI 📰🔍

**Veritas AI** is an AI-powered fact-checking agent that verifies news claims using real-time web search and Large Language Models. Simply enter a claim, and Veritas AI searches the internet, gathers evidence, analyzes the information, and returns a verdict with supporting sources.

Built with **Python**, **Gradio**, **Groq Llama 3.3 70B**, and **Tavily Search API**.

---

## ✨ Features

* 🌐 Real-time web search
* 🤖 AI-powered claim analysis
* ✅ Verdict classification:

  * TRUE
  * FALSE
  * MISLEADING
  * UNVERIFIED
* 📊 Confidence score (0–100%)
* 📝 Evidence-based summaries
* 🔗 Source citations
* 🎨 Modern dark-themed interface
* ⚡ Fast inference using Groq

---

## 📸 Demo

Enter a news claim such as:

```text
India launched its first solar mission Aditya-L1 in 2023
```

Veritas AI will:

1. Search the web for relevant information.
2. Collect supporting evidence.
3. Analyze the evidence using Llama 3.3 70B.
4. Generate a verdict with confidence score and sources.

---

## 🏗️ Project Structure

```text
VeritasAI/
│
├── app.py              # Gradio Frontend
├── agent.py            # Fact-checking agent logic
├── search_tool.py      # Tavily search integration
├── .env                # API Keys
│
└── README.md
```

---

## ⚙️ Tech Stack

| Technology    | Purpose           |
| ------------- | ----------------- |
| Python        | Core Backend      |
| Gradio        | Web Interface     |
| Groq API      | LLM Inference     |
| Llama 3.3 70B | Claim Analysis    |
| Tavily Search | Real-time Search  |
| HTML/CSS      | Custom UI Styling |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/veritas-ai.git

cd veritas-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install gradio
pip install groq
pip install tavily-python
pip install python-dotenv
```

or

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get API keys from:

* [Groq](https://groq.com?utm_source=chatgpt.com)
* [Tavily AI](https://tavily.com?utm_source=chatgpt.com)

---

## ▶️ Running the Application

```bash
python app.py
```

The Gradio interface will launch locally.

---

## 🧠 How It Works

```text
User Claim
     │
     ▼
Tavily Search API
     │
     ▼
Relevant Articles
     │
     ▼
Llama 3.3 70B (Groq)
     │
     ▼
Evidence Analysis
     │
     ▼
Verdict + Confidence + Sources
```

---

## 📋 Example Output

```json
{
  "verdict": "FALSE",
  "confidence": 95,
  "summary": "No reliable evidence supports the claim. Multiple authoritative sources contradict it.",
  "supporting": [],
  "contradicting": [
    "Official sources deny the claim",
    "No scientific evidence found"
  ]
}
```

---

## 🎯 Use Cases

* Fact-checking viral news
* Verifying social media posts
* Educational research
* Journalism assistance
* Misinformation detection
* Current affairs analysis

---

## ⚠️ Limitations

* Dependent on publicly available web information.
* Search results may vary over time.
* AI-generated analysis can occasionally be incorrect.
* Should not replace professional journalism or expert verification.

---

## 🔮 Future Improvements

* Multi-source credibility scoring
* News bias detection
* Source trust ranking
* Historical claim tracking
* PDF/article upload verification
* RAG-based evidence retrieval
* Citation highlighting
* Mobile-responsive newspaper UI

---

## 👥 Team

**Team Transformers**

Built for combating misinformation through AI-powered fact verification.

---

## 📜 License

This project is licensed under the MIT License.

---

### "Trust, but verify." 🔍✨
