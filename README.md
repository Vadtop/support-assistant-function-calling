# Support Assistant with Function Calling

AI support assistant with function calling for fintech use case. LLM autonomously decides when to use FAQ search or loan calculator tools.

## 🎯 Project Goal

Educational project — demonstrates function calling.
LLM autonomously decides when to invoke a tool: 
FAQ search or loan calculator.

## 🏗️ Architecture

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

## ✨ Features

- **Function calling**: LLM automatically invokes `search_faq()` or `calculate_loan()` when needed
- **Smart decision making**: Model chooses between tools or direct response
- **Multiple tools**: FAQ search + loan calculator in one assistant
- **Token-based FAQ search**: Simple but effective (easy to scale to vector DB)
- **Loan calculator**: Extract parameters from natural language and calculate payments
- **FastAPI**: Production-ready API with auto-documentation
- **Fintech scenario**: FAQ about cards, limits, transfers, balance, cashback

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI** — modern web framework for APIs
- **OpenAI API** (via OpenRouter) — LLM with function calling
- **Token-based search** — simple yet effective FAQ search

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/support-assistant-function-calling.git
cd support-assistant-function-calling

# Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
# Create .env file in project root:
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

## 🚀 Usage

### Start API server

```bash
uvicorn app.main:app --reload
```

Open interactive docs at: http://localhost:8000/docs

### Example Requests

#### FAQ Search

```bash
curl -X POST "http://localhost:8000/support/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I check my card balance?"}'
```

Response:

```json
{
  "assistant_answer": "You can check balance in mobile app...",
  "tool_used": true,
  "tool_name": "search_faq",
  "faq_results": [...]
}
```

#### Loan Calculation

```bash
curl -X POST "http://localhost:8000/support/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I want a loan of 500,000 rubles for 12 months at 15%"}'
```

Response:

```json
{
  "assistant_answer": "Monthly payment: 45,129 rubles...",
  "tool_used": true,
  "tool_name": "calculate_loan",
  "calculation_result": {
    "monthly_payment": 45129.16,
    "total_payment": 541549.87,
    "overpayment": 41549.87
  }
}
```

#### General Question (no tool)

```bash
curl -X POST "http://localhost:8000/support/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Thank you!"}'
```

Response:

```json
{
  "assistant_answer": "You're welcome! Let me know if you need help.",
  "tool_used": false
}
```

## 🌐 API Endpoints

### `GET /`
Health check endpoint.

### `GET /faq/search`
Test FAQ search without LLM.
- Parameters: `q` (search query), `top_k` (number of results)

### `POST /support/chat`
Main assistant endpoint with function calling.
- Request body: `{"message": "your question here"}`

## 📂 Project Structure

```
support-assistant-function-calling/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app + endpoints
│   ├── faq_data.py       # Knowledge base (12 FAQ items)
│   └── tools.py          # Tools: search_faq + calculate_loan
├── examples/
│   └── conversations.md  # Dialog examples
├── .env                  # API keys (not in git)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Technical Highlights

### Core Concepts

- **Function calling** — LLM can invoke external functions/APIs for data retrieval
- **Tool decision making** — model autonomously decides when to use tools
- **Parameter extraction** — LLM extracts structured data from natural language
- **Multiple tools** — one assistant can handle different types of requests

### Implementation Details

- Tool definition via JSON schema (function name, description, parameters)
- Two-step flow: (1) LLM decides → (2) execute tool → (3) LLM formulates answer
- `tool_choice="auto"` — model decides when to use tool vs direct response
- Handling multiple tools with if/elif branches

## 📊 Project Evolution

### Current Version (v1.0)

- ✅ Function calling with 2 tools (FAQ search + loan calculator)
- ✅ FastAPI REST API
- ✅ Token-based FAQ search (12 items)
- ✅ Loan calculator with parameter extraction
- ✅ Examples and documentation

### Planned (v1.1)

- ⏳ Add vector DB (Pinecone/Weaviate) for FAQ search
- ⏳ Multi-turn conversations with dialog history
- ⏳ Third tool: create_ticket for escalation
- ⏳ Metrics (latency, tool usage rate)

### Future (v2.0)

- 🔮 Deploy to Railway/Render
- 🔮 Add monitoring and logging
- 🔮 A/B testing (with tool vs without tool)

## 💡 Why This Approach?

Starting with simple token-based search and manual tool handling, then scaling to vector DB and advanced orchestration. This gives:

- Clear understanding of function calling internals
- Ability to debug tool invocation issues

## 📧 Contact

GitHub: [@Vadtop](https://github.com/Vadtop)
