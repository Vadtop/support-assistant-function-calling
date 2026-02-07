"""
v2.0: Agent Approach with LangChain (ReAct)
LLM autonomously decides which tools to use and in what order
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
import os
import json
from dotenv import load_dotenv

# Импорт FAQ
import sys
sys.path.append(os.path.dirname(__file__))
from faq_data import FAQ_DATABASE

load_dotenv()

# ========== TOOLS ==========

@tool
def search_faq(query: str) -> str:
    """Search FAQ database about bank products, services, limits, transfers, cashback. Always respond in Russian."""
    query_lower = query.lower()
    results = []
    
    for item in FAQ_DATABASE:
        if any(word in item["question"].lower() for word in query_lower.split()):
            results.append(f"Q: {item['question']}\nA: {item['answer']}")
    
    if results:
        return "\n\n".join(results[:3])
    return "Информация не найдена в FAQ"

@tool
def calculate_loan(loan_params) -> str:
    """Calculate monthly loan payment. 
    Args:
        loan_params: Loan parameters as JSON string or dict. Example: {"amount": 500000, "rate": 15, "months": 12}
            - amount (float): Loan amount in rubles
            - rate (float): Annual interest rate (percentage)
            - months (int): Loan term in months
    """
    try:
        # Если пришла строка - парсим JSON, если словарь - используем как есть
        if isinstance(loan_params, str):
            params = json.loads(loan_params)
        else:
            params = loan_params
        
        amount = float(params["amount"])
        rate = float(params["rate"])
        months = int(params["months"])
        
        # Расчёт
        monthly_rate = rate / 12 / 100
        if monthly_rate == 0:
            payment = amount / months
        else:
            payment = amount * (monthly_rate * (1 + monthly_rate) ** months) / \
                      ((1 + monthly_rate) ** months - 1)
        
        total = payment * months
        overpayment = total - amount
        
        return f"""Расчёт кредита:
- Сумма: {amount:,.0f} руб
- Ставка: {rate}% годовых
- Срок: {months} мес
- Ежемесячный платёж: {payment:,.2f} руб
- Переплата: {overpayment:,.2f} руб"""
    except Exception as e:
        return f"Ошибка расчёта: {str(e)}. Получено: {type(loan_params)} = {loan_params}"

@tool
def create_ticket(description: str) -> str:
    """Create support ticket when you cannot solve the problem yourself.
    Args:
        description: Customer problem description
    """
    ticket_id = "TICKET-" + str(abs(hash(description)))[-6:]
    return f"✅ Тикет {ticket_id} создан. Специалист свяжется в течение 24 часов."

# ========== AGENT SETUP ==========

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

tools = [search_faq, calculate_loan, create_ticket]

# ReAct промпт (английский — стандартный для LangChain)
prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You are a Russian bank AI assistant. Always provide final answers in Russian. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action as valid JSON string
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question in Russian

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

# Создаём ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Создаём executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# ========== MAIN FUNCTION ==========

def chat(message: str) -> dict:
    """Обработка сообщения через agent"""
    try:
        response = agent_executor.invoke({"input": message})
        return {
            "answer": response["output"],
            "approach": "react_agent",
            "version": "v2.0"
        }
    except Exception as e:
        return {
            "answer": f"Ошибка: {str(e)}",
            "approach": "react_agent",
            "version": "v2.0"
        }

# ========== TESTS ==========

if __name__ == "__main__":
    print("="*60)
    print("🤖 SUPPORT ASSISTANT v2.0 (ReAct Agent)")
    print("="*60)
    
    test_queries = [
        "Привет!",
        "Как узнать баланс карты?",
        "Хочу взять кредит 500 тысяч на год под 15%",
        "Не могу войти в приложение!",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"❓ ВОПРОС: {query}")
        print("="*60)
        
        result = chat(query)
        print(f"\n✅ ОТВЕТ:\n{result['answer']}\n")
