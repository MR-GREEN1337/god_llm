import functools
from typing import Optional
from god_llm.plugins.base import (
    AIMessage,
    AnthropicModel,
    BaseLLM,
    TemperatureValidator,
)
import anthropic

from god_llm.plugins.exceptions import BaseLLMException


class ChatAnthropic(BaseLLM):
    """
    A class for generating text completions using Anthropic models, supporting temperature
    settings for controlling the variability of responses. It manages authentication
    and client interaction with the Anthropic API.

    Attributes:
    - model_name: The Anthropic model name to use for generating completions.
    - temperature: (Optional) Controls randomness in the output, with a default value of 0.7.
    - api_key: (Optional) The API key for authenticating with the Anthropic API. If not provided,
      it retrieves the key from the authentication module.

    Methods:
    - generate(prompt: str) -> str: Sends the prompt to the Anthropic model and returns the
      generated response, including predefined system messages.
    """

    def __init__(
        self,
        model_name: AnthropicModel,
        temperature: Optional[TemperatureValidator] = 0.7,
        api_key: Optional[str] = None,
    ):
        super().__init__("anthropic", api_key)
        self.model_name = model_name
        self.api_key = self.auth.get_key("anthropic")
        self.client = functools.partial(
            anthropic.Anthropic(api_key=self.api_key).completions.create,
            model=self.model_name,
            temperature=temperature,
        )

    def generate(self, prompt: str) -> AIMessage:
        try:
            client = self.client(
                messages=[
                    {"role": "system", "content": "you are a helpful assistant."},
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
            )
            result = client.content
            return AIMessage(
                model_name=self.model_name,
                content=result,
                provider="anthropic",
                metadata={"temperature": self.temperature, "media_type": "text"},
            )
        except Exception as e:
            raise BaseLLMException(f"Error generating completion: {e}")
