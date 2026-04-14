# Support Assistant with Function Calling

AI support assistant with function calling for fintech. LLM autonomously decides when to search FAQ or calculate loan payments.

---

## Architecture

```
User Question
    ↓
LLM (GPT-4o-mini) + tools definition
    ↓
[Decision: use tool?]
    ↓
YES → execute tool (search_faq / calculate_loan)
    ↓
Tool results → LLM
    ↓
Final answer based on real data
```

---

## Features

- **Function calling** — LLM automatically invokes `search_faq()` or `calculate_loan()` when needed
- **Smart decision making** — model chooses between tools or direct response
- **Multiple tools** — FAQ search + loan calculator in one assistant
- **Token-based FAQ search** — simple but effective (easy to scale to vector DB)
- **Loan calculator** — extract parameters from natural language and calculate payments
- **FastAPI** — production-ready API with auto-documentation
- **v2: LangChain Agent** — ReAct agent with tool usage and memory

---

## Quick Start

### Docker

```bash
git clone https://github.com/Vadtop/support-assistant-function-calling.git
cd support-assistant-function-calling

# Set API key
echo "OPENROUTER_API_KEY=your-key-here" > .env

docker-compose up --build
```

### Manual

```bash
pip install -r requirements.txt
echo "OPENROUTER_API_KEY=your-key-here" > .env
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/faq/search?q=...` | Test FAQ search without LLM |
| POST | `/support/chat` | Main assistant with function calling |

---

## Examples

```bash
# FAQ search — triggers search_faq tool
curl -X POST http://localhost:8000/support/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I check my card balance?"}'

# Loan calculation — triggers calculate_loan tool
curl -X POST http://localhost:8000/support/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want a loan of 500000 rubles for 12 months at 15%"}'

# General question — no tool needed
curl -X POST http://localhost:8000/support/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Thank you!"}'
```

---

## Project Structure

```
support-assistant-function-calling/
├── v1_function_calling/    # OpenAI function calling API
├── v2_agent/              # LangChain ReAct agent
├── examples/              # Dialog examples
├── requirements.txt
└── README.md
```

---

## Tech Stack

- Python 3.11
- FastAPI — REST API
- OpenAI API (via OpenRouter) — LLM with function calling
- LangChain — agent framework (v2)
- Docker

---

## Author

[Vadim Titov](https://github.com/Vadtop)
