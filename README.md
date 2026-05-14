# 🤖 AI Chatbot with Django & Ollama

An intelligent chatbot that combines web scraping, local AI processing, and smart caching for fast and intelligent responses.

##  Features

-  **Dynamic Web Scraping** - Automatic Google search and content extraction
-  **Local AI Processing** - Uses Ollama (Llama 3.1 8B) for response generation
-  **Smart Caching** - Instant responses for repeated questions (0.5s vs 15-30s)
-  **Multi-language Support** - Supports Greek, English, and other languages
-  **Persistent Storage** - Stores queries, responses, and scraped data in SQLite

##  Tech Stack

**Backend:**
- Python 3.13
- Django 6.0
- SQLite

**AI:**
- Ollama (Llama 3.1 8B)

**Web Scraping:**
- BeautifulSoup4
- Requests

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript

##  Performance

| Scenario | Time | Process |
|----------|------|---------|
| First query | 15-30s | Google search + Web scraping + AI processing |
| Cached query | 0.5s | Database lookup |
| Speedup | ~30-60x | After first time |

##  Installation

### Prerequisites

- Python 3.10+
- Ollama

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/Irini1996/AI_BOT.git
cd AI_BOT
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install django requests beautifulsoup4
```

4. **Install Ollama**
- Download from: https://ollama.com
- Pull the model:
```bash
ollama pull llama3.1:8b
```

5. **Database setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Run server**
```bash
python manage.py runserver
```

7. **Open in browser**
http://localhost:8000

##  How It Works

### First Query (New):
User Question → Django Backend → Google Search → Web Scraping →
Ollama AI Processing → Database Storage → Response (15-30s)

### Cached Query:
User Question → Django Backend → Database Lookup → Response (0.5s)

##  Key Components

### Database Models
- **SearchQuery** - Stores queries with hash for fast lookup
- **AIResponse** - Stores AI-generated responses
- **WebScrapedData** - Stores scraped content from websites

### Utils Functions
- `ask_ollama()` - Communication with Ollama API
- `google_search()` - Google search and URL extraction
- `scrape_webpage()` - Web scraping with BeautifulSoup

## 📁 Project Structure
ai_chatbot/
├── chatbot/
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── utils.py           # Helper functions
│   ├── urls.py            # URL routing
│   └── templates/
│       └── chatbot/
│           └── index.html # Frontend UI
├── config/
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL config
├── db.sqlite3             # SQLite database
├── manage.py
└── README.md

##  Features Demo

- **First query:** Searches online, processes with AI (~15-30s)
- **Subsequent queries:** Instant from cache (~0.5s)
- **Multilingual:** Understands and responds in multiple languages

##  Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

##  License

MIT License - See [LICENSE](LICENSE) file for details.

##  Author

**Irini**
- GitHub: [@Irini1996](https://github.com/Irini1996)

##  Acknowledgments

- Ollama for the local AI engine
- Django community
- BeautifulSoup for web scraping capabilities

---

⭐ Star this repo if you find it useful!
