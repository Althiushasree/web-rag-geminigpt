# web-rag-geminigpt

A **Retrieval-Augmented Generation (RAG)** web application that searches the live web for relevant context and feeds it to Google Gemini to produce accurate, up-to-date, context-aware answers.

---

## How RAG Works

```
User Query
    │
    ▼
[Retriever]  ──►  Web Search (DuckDuckGo)
                      │
                      ▼
                Scrape top pages
                      │
                      ▼
                Clean & chunk text
                      │
                      ▼
[Generator]  ──►  Build prompt:
                  system msg + context chunks + query
                      │
                      ▼
               Google Gemini API
                      │
                      ▼
           Context-aware answer  ◄── returned to user
```

**Retrieval** grounds the model in real, current information.  
**Generation** synthesises that information into a coherent, natural-language answer.  
Together they avoid hallucination and knowledge-cutoff issues.

---

## Components

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web framework | Flask | HTTP server, routing, template rendering |
| Retrieval | `requests` + `BeautifulSoup` | Web search & HTML scraping |
| Generation | `google-generativeai` | Gemini 1.5 Flash API |
| Config | `python-dotenv` | Secure API key loading |
| Frontend | Vanilla HTML / CSS / JS | Chat-style UI |

---

## Prerequisites

- Python 3.9+
- A **Google Gemini API key** (free tier available)

### How to get a Gemini API key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API key**
4. Copy the key — you'll paste it into `.env` in the next step

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Althiushasree/web-rag-geminigpt.git
cd web-rag-geminigpt

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Gemini API key
cp .env.example .env
# Open .env and replace `your_api_key_here` with your real key
```

---

## Running the App

```bash
python app.py
```

Open your browser at **http://localhost:5000**.

Type any question into the search box and hit **Ask**.  
The app will:
1. Search the web for relevant pages
2. Scrape and chunk the top results
3. Send the chunks + your question to Gemini
4. Display the AI-generated answer and the source URLs

---

## Project Structure

```
web-rag-geminigpt/
├── app.py              # Flask application & API route
├── retriever.py        # Web search, scraping, chunking
├── generator.py        # Gemini prompt builder & API caller
├── config.py           # Environment variable loader
├── requirements.txt    # Python dependencies
├── .env.example        # Template for secrets
├── .gitignore          # Git ignore rules
├── templates/
│   └── index.html      # Chat-style frontend
└── static/
    └── style.css       # Dark-mode UI styles
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |

---

## License

MIT
