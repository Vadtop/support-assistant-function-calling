from typing import List, Dict
from app.faq_data import FAQ

def normalize(text: str) -> List[str]:
    """Нормализация: нижний регистр, убираем знаки препинания, разбиваем на токены."""
    return text.lower().replace("?", "").replace(",", "").replace(".", "").split()

def score(query_tokens: List[str], question_tokens: List[str]) -> int:
    """Простая метрика: количество совпадающих токенов."""
    return sum(1 for token in query_tokens if token in question_tokens)

def search_faq(query: str, top_k: int = 3) -> List[Dict]:
    """
    Поиск по FAQ на основе количества совпадающих токенов.
    Возвращает top_k наиболее релевантных записей.
    """
    query_tokens = normalize(query)
    scored_items = []
    
    for item in FAQ:
        question_tokens = normalize(item["question"])
        s = score(query_tokens, question_tokens)
        if s > 0:
            scored_items.append((s, item))
    
    # Сортируем по убыванию score
    scored_items.sort(key=lambda x: x[0], reverse=True)
    
    # Возвращаем top_k результатов
    return [item for _, item in scored_items[:top_k]]


# JSON-схема для function calling (понадобится в блоке 3)
faq_search_tool = {
    "type": "function",
    "function": {
        "name": "search_faq",
        "description": "Поиск по базе знаний (FAQ) банка. Используй, когда клиент задаёт вопрос про продукты, лимиты, баланс, переводы, карты.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Вопрос клиента на естественном языке (например: 'как узнать баланс')"
                }
            },
            "required": ["query"]
        }
    }
}

def calculate_loan(amount: float, rate: float, months: int) -> dict:
    """
    Рассчитать ежемесячный платёж по кредиту.
    
    Args:
        amount: Сумма кредита в рублях
        rate: Процент годовых
        months: Срок кредита в месяцах
    
    Returns:
        dict с ежемесячным платежом, общей суммой и переплатой
    """
    monthly_rate = rate / 12 / 100
    payment = amount * (monthly_rate / (1 - (1 + monthly_rate) ** -months))
    
    return {
        "monthly_payment": round(payment, 2),
        "total_payment": round(payment * months, 2),
        "overpayment": round(payment * months - amount, 2)
    }


# Tool definition для function calling
loan_calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate_loan",
        "description": "Рассчитать ежемесячный платёж по кредиту и общую переплату",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Сумма кредита в рублях"
                },
                "rate": {
                    "type": "number",
                    "description": "Процентная ставка годовых (например, 15 для 15%)"
                },
                "months": {
                    "type": "integer",
                    "description": "Срок кредита в месяцах"
                }
            },
            "required": ["amount", "rate", "months"]
        }
    }
}
