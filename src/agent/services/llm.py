from langchain_openai import ChatOpenAI
from agent.core.config import settings

def get_llm(temperature : float = 0.0) -> ChatOpenAI:
    if not settings.openrouter_api_key:
        raise ValueError ("OpenRouter api key is missing")
    
    return ChatOpenAI(
        model = settings.default_model,
        api_key = settings.openrouter_api_key,
        base_url = "https://openrouter.ai/api/v1",
        temperature = temperature,
        default_headers = {
            "HTTP-Referer": "http://localhost:8000", # Update in production
            "X-Title": settings.app_name,
        }
    )