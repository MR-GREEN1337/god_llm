from abc import ABC, abstractmethod
import datetime
from typing import Any, Dict, Literal, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

LLMProviderType = Literal["ollama", "openai", "anthropic", "bedrock", "groq"]

# TODO: Replace Model names with up-to-date and actual model names
GroqModel = Literal[
    "gemma2-9b-it",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
]

OpenAIModel = Literal[
    "gemma2-9b-it",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
]

AnthropicModel = Literal[
    "gemma2-9b-it",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
]


class BaseMessage(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    content: str
    created_at: datetime.datetime = datetime.datetime.now()
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
    model_config["populate_by_name"] = True


class AIMessage(BaseMessage):
    provider: Optional[LLMProviderType] = None
    model: Optional[Union[GroqModel, OpenAIModel, AnthropicModel]] = None


class UserMessage(BaseMessage):
    pass


class BaseLLM(ABC):
    def __init__(self, provider: LLMProviderType, api_key: Optional[str] = None):
        from god_llm.auth import Auth

        self.provider = provider
        self.auth = Auth()
        if api_key:
            self.auth.set_key(provider, api_key)
        elif not self.auth.get_key(provider):
            raise ValueError(f"No API key provided or found for {provider}")

    @abstractmethod
    def generate(self, prompt: str) -> AIMessage:
        pass


class TemperatureValidator(BaseModel):
    temperature: float = Field(
        ..., ge=0.0, le=1.0, description="Temperature must be between 0 and 1."
    )

    @field_validator("temperature")
    def validate_temperature(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError("Temperature must be between 0 and 1.")
        return v


class BaseTool(ABC):
    pass
