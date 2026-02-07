import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from v1_function_calling.tools import search_faq, faq_search_tool, calculate_loan, loan_calculator_tool


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

app = FastAPI(title="Support Assistant API", version="1.0")


# Модель запроса для чата
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "Support Assistant API is running"}


@app.get("/faq/search")
def faq_search_endpoint(q: str, top_k: int = 3):
    """Тестовый эндпойнт для проверки поиска по FAQ без LLM."""
    results = search_faq(q, top_k)
    return {
        "query": q,
        "results_count": len(results),
        "results": results
    }


@app.post("/support/chat")
def support_chat(req: ChatRequest):
    """
    Основной эндпойнт ассистента поддержки с function calling.
    LLM сам решает, когда вызывать search_faq или calculate_loan.
    """
    user_message = req.message
    
    # Первый запрос к LLM
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты — ассистент службы поддержки банка. "
                    "Твоя задача: помогать клиентам с вопросами про продукты, карты, переводы, лимиты, кредиты. "
                    "Если вопрос про продукты банка — используй функцию search_faq. "
                    "Если вопрос про расчёт кредита — используй функцию calculate_loan. "
                    "Если общий вопрос (приветствие, благодарность) — отвечай сам."
                )
            },
            {"role": "user", "content": user_message}
        ],
        tools=[faq_search_tool, loan_calculator_tool],
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # Если модель запросила вызов функции
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        
        if tool_call.function.name == "search_faq":
            # Парсим аргументы
            arguments = json.loads(tool_call.function.arguments)
            query = arguments.get("query", "")
            
            # Выполняем поиск
            faq_results = search_faq(query)
            
            # Второй запрос: отдаём модели результаты
            followup_response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты — ассистент службы поддержки банка."
                    },
                    {"role": "user", "content": user_message},
                    message,  # исходное сообщение с tool_calls
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "search_faq",
                        "content": json.dumps(faq_results, ensure_ascii=False)
                    }
                ]
            )
            
            final_message = followup_response.choices[0].message
            
            return {
                "assistant_answer": final_message.content,
                "tool_used": True,
                "tool_name": "search_faq",
                "tool_query": query,
                "faq_results": faq_results
            }
        
        elif tool_call.function.name == "calculate_loan":
            # Парсим аргументы
            arguments = json.loads(tool_call.function.arguments)
            
            # Выполняем расчёт
            result = calculate_loan(
                amount=arguments.get("amount"),
                rate=arguments.get("rate"),
                months=arguments.get("months")
            )
            
            # Второй запрос: отдаём модели результаты
            followup_response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты — ассистент банка."
                    },
                    {"role": "user", "content": user_message},
                    message,  # исходное сообщение с tool_calls
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "calculate_loan",
                        "content": json.dumps(result, ensure_ascii=False)
                    }
                ]
            )
            
            final_message = followup_response.choices[0].message
            
            return {
                "assistant_answer": final_message.content,
                "tool_used": True,
                "tool_name": "calculate_loan",
                "calculation_result": result
            }
    
    # Если функция не вызывалась — прямой ответ
    return {
        "assistant_answer": message.content,
        "tool_used": False
    }
