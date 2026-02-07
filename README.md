# Support Assistant: Function Calling & ReAct Agent

AI-powered bank support assistant demonstrating two approaches to LLM tool usage: **Function Calling (v1)** and **ReAct Agent (v2)**.

Built to showcase practical understanding of agents, function calling, and production-ready AI systems for fintech use cases.

---

## 🎯 Project Goal

Demonstrate mastery of:
- **Function calling** — how LLM invokes external tools and autonomously decides when to use them
- **Agent patterns** — ReAct loop for multi-step reasoning
- **Production architecture** — FastAPI, error handling, scalability

This project is part of my transition to an AI/LLM Engineer role, with focus on real-world applications.

---

## 🏗️ Two Approaches

### v1: Function Calling (Simple & Fast)

**Architecture:**
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

**Pros:**
- ✅ Fast (1-2 LLM calls)
- ✅ Lower cost
- ✅ Predictable behavior
- ✅ Easy to debug

**Cons:**
- ❌ Limited to single tool per request
- ❌ Logic controlled by code (if/else)
- ❌ No multi-step reasoning

**Best for:** Simple use cases where speed matters (customer FAQ, single calculations)

📂 **Code:** `/v1_function_calling/`

---

### v2: ReAct Agent (Smart & Flexible)

**Architecture:**
```
User Question
    ↓
LLM Agent (ReAct loop)
    ↓
Thought: What should I do?
    ↓
Action: choose tool (search_faq / calculate_loan / create_ticket)
    ↓
Observation: tool result
    ↓
... (repeat if needed)
    ↓
Thought: I know the answer
    ↓
Final Answer
```

**Pros:**
- ✅ Multi-step reasoning (can call multiple tools)
- ✅ Autonomous decision making
- ✅ Handles complex scenarios (e.g., search FAQ → not found → create ticket)
- ✅ No hardcoded logic

**Cons:**
- ❌ Slower (N LLM calls in loop)
- ❌ Higher cost
- ❌ Less predictable (needs error handling)

**Best for:** Complex support scenarios requiring reasoning and escalation

📂 **Code:** `/v2_agent/`

---

## ✨ Features

### v1 (Function Calling)
- **2 tools**: FAQ search + loan calculator
- **FastAPI REST API** with auto-documentation
- **Token-based search** (simple, effective)
- **Parameter extraction** from natural language
- **Production-ready** error handling

### v2 (ReAct Agent)
- **3 tools**: FAQ search + loan calculator + ticket creation
- **Multi-step reasoning**: search → analyze → escalate if needed
- **LangChain ReAct agent** with autonomous tool selection
- **Conversation flow**: Thought → Action → Observation → Answer
- **Graceful degradation**: handles parsing errors and timeouts

---

## 🚀 Real-World Applications & Scaling

### 1. Production Use Cases

**A) Internal IT/HR Support Bot**
- Replace 12 FAQ items with company knowledge base (100-500 items)
- Add tools: `reset_password`, `create_jira_ticket`, `check_vacation_balance`
- Integrate with Slack/Telegram
- **Value**: Reduces support team load by 60-80%

**B) E-commerce Customer Support**
- Add tools: `track_order`, `process_return`, `check_stock`
- Integrate with CRM (Zendesk, Intercom)
- Handle: "Where's my order?", "How to return?", "What sizes available?"
- **Value**: 24/7 instant responses, 70% questions closed without human

**C) Fintech Client Service**
- Add tools: `check_transactions`, `block_card`, `exchange_rate`
- Handle: balance checks, transaction history, security issues
- **Value**: Real-time data access, instant card blocking

### 2. Easy Extensions (Just Add Tools)

The agent architecture allows adding new tools without changing core logic:

```python
@tool
def check_transaction(card_number: str, days: int) -> str:
    """Get last N transactions"""
    # Call bank API
    return "Last 3 transactions: ..."

@tool
def track_order(order_id: str) -> str:
    """Check order delivery status"""
    # Call delivery API
    return "Order arrives tomorrow"
```

Agent automatically learns to use new tools — no if/else needed.

### 3. Architectural Scaling

**Add Memory (Context):**
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
```

Now agent remembers conversation history.

**Upgrade FAQ to Vector Search:**
```python
from langchain.vectorstores import Chroma
vectorstore = Chroma.from_texts(faq_data, embeddings)
```

Semantic search instead of keyword matching.

**Wrap in Production API:**
```python
# Already FastAPI in v1, easily add to v2
@app.post("/chat")
def chat_endpoint(message: str):
    return agent.invoke(message)
```

**Integrate with Messaging:**
- Telegram bot (aiogram)
- Slack app
- WhatsApp Business API
- Web widget

---

## 🛠️ Tech Stack

**Core:**
- Python 3.11
- OpenAI API via OpenRouter (gpt-4o-mini)
- LangChain 0.1.x (for v2 agent)

**v1 Stack:**
- FastAPI — REST API framework
- Pydantic — data validation
- Token-based search

**v2 Stack:**
- LangChain ReAct Agent
- PromptTemplate for ReAct loop
- AgentExecutor with error handling

---

## 📦 Quick Start

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/support-assistant-function-calling.git
cd support-assistant-function-calling

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Create .env file
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

### Run v1 (Function Calling + FastAPI)

```bash
cd v1_function_calling
uvicorn main:app --reload
# Visit http://localhost:8000/docs
```

### Run v2 (ReAct Agent)

```bash
cd v2_agent
python agent_main.py
```

---

## 📊 Example Interactions

### v1: FAQ Search

```
User: "How can I check my card balance?"
Assistant: "You can check balance in mobile app in 'My Cards' section or via SMS command BAL to 900."
```

### v2: Multi-Step Reasoning

```
User: "I can't login to the app!"
Agent: 
  Thought: Need to check FAQ for login issues
  Action: search_faq("login app")
  Observation: No relevant FAQ found
  Thought: This is a technical issue, need support
  Action: create_ticket("User cannot login")
  Observation: Ticket TICKET-123456 created
  Final Answer: "Support ticket created, specialist will contact you within 24 hours."
```

---

## 🧠 What I Learned

### Technical Skills

**Function Calling:**
- Tool definition via JSON schema
- Two-step flow: decision → execution → answer
- `tool_choice="auto"` for autonomous decisions
- Multi-tool handling

**ReAct Agents:**
- Thought → Action → Observation loop
- LLM autonomous tool selection
- Multi-step reasoning without hardcoded logic
- Error handling for unreliable LLM outputs

**Production:**
- FastAPI for production APIs
- Error handling and graceful degradation
- Trade-offs: latency vs flexibility
- Provider compatibility (OpenRouter vs OpenAI tools format)

### Interview-Ready Concepts

#### 1. Function Calling vs Agents

| Aspect | Function Calling | Agent |
|--------|-----------------|-------|
| Control | Code controls logic | LLM controls logic |
| Steps | Single tool call | Multi-step reasoning |
| Speed | Fast (1-2 calls) | Slower (N calls) |
| Use case | Simple queries | Complex reasoning |

#### 2. When to Use What?

- **Function Calling (v1)**: Speed-critical, simple flows, predictable behavior
- **Agents (v2)**: Complex scenarios, need reasoning, multi-tool workflows

#### 3. Production Considerations

- **Latency**: agents are 2-3x slower
- **Cost**: agents use 3-5x more tokens
- **Reliability**: agents need max_iterations and error handling
- **Debugging**: verbose mode essential for agents

#### 4. Scaling Path

1. **Start**: token-based FAQ (like now)
2. **Scale**: vector DB for semantic search
3. **Advanced**: RAG with document retrieval
4. **Enterprise**: multi-agent systems with specialized agents

---

## 📂 Project Structure

```
support-assistant-function-calling/
├── v1_function_calling/      # FastAPI + Function Calling
│   ├── main.py               # API endpoints
│   ├── faq_data.py          # Knowledge base
│   └── tools.py             # Tool implementations
├── v2_agent/                # LangChain ReAct Agent
│   ├── agent_main.py        # Agent + tools
│   ├── faq_data.py         # Knowledge base
│   └── README.md           # v2 documentation
├── examples/
│   └── conversations.md    # Dialog examples
├── requirements.txt
└── README.md              # This file
```

---

## 🎓 Interview Readiness

### Key Questions I Can Answer

**Q: What is function calling and why use it?**

A: Function calling allows LLM to invoke external functions/APIs for real-time data retrieval. Prevents hallucinations, enables integration with internal systems, and provides structured tool invocation.

**Q: What's the difference between function calling and agents?**

A: Function calling = LLM suggests tool, code executes (single step). Agent = LLM controls full workflow, can do multi-step reasoning (search FAQ → not found → create ticket).

**Q: When would you use v1 vs v2?**

A: v1 for simple, latency-sensitive use cases (FAQ, calculations). v2 for complex scenarios requiring reasoning (troubleshooting, multi-step workflows).

**Q: How would you scale this to production?**

A:
- Replace token search with vector DB (semantic search)
- Add conversation memory for context
- Implement monitoring and logging
- Add rate limiting and authentication
- Deploy on cloud with auto-scaling (Railway/Render)

**Q: What are the risks of agents in production?**

A: Latency (slower), cost (more tokens), unpredictability (need error handling), infinite loops (need max_iterations). Solution: fallback to simpler responses, timeouts, extensive logging.

---

## 📝 Notes

- This is a learning & portfolio project demonstrating production-ready patterns
- API keys not included — use your own via `.env`
- Built as part of intensive AI/LLM Engineering learning path
- Focus areas: RAG, function calling, agents, production best practices

---

## 📧 Contact

**Built by Vadim Titov**

Transitioning to AI/LLM Engineer role

**Focus:** RAG, function calling, agents, AI assistants for customer support and fintech

**Portfolio:** [GitHub](https://github.com/Vadtop)

---

## 🔄 Version History

- **v1.0 (Feb 2026)**: Function calling with FastAPI, 2 tools (FAQ + loan calc)
- **v2.0 (Feb 2026)**: ReAct agent with LangChain, 3 tools (+ ticket creation), multi-step reasoning

### Next planned:
- Vector DB integration for semantic FAQ search
- Conversation memory for context
- Deployment to production (Railway/Render)
- Metrics dashboard (response time, tool usage, user satisfaction)
