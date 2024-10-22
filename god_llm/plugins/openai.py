from .base import AIMessage, BaseLLM, OpenAIModel, TemperatureValidator
from typing import Optional
import functools
import openai
from .exceptions import BaseLLMException


class ChatOpenAI(BaseLLM):
    """
    A class for generating text completions using OpenAI models, supporting temperature
    settings for controlling the variability of responses. It manages authentication
    and client interaction with the OpenAI API.

    Attributes:
    - model_name: The OpenAI model name to use for generating completions.
    - temperature: (Optional) Controls randomness in the output, with a default value of 0.7.
    - api_key: (Optional) The API key for authenticating with the Groq API. If not provided,
      it retrieves the key from the authentication module.

    Methods:
    - generate(prompt: str) -> str: Sends the prompt to the OpenAI model and returns the
      generated response, including predefined system messages.
    """

    def __init__(
        self,
        model_name: OpenAIModel,
        temperature: Optional[TemperatureValidator] = 0.7,
        api_key: Optional[str] = None,
    ):
        super().__init__("groq", api_key)
        self.model_name = model_name
        self.api_key = self.auth.get_key("openai")
        self.client = functools.partial(
            openai.OpenAI(api_key=self.api_key).chat.completions.create,
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
            result = client.choices[0].message.content

            return AIMessage(
                model_name=self.model_name,
                content=result,
                provider="openai",
                metadata={"temperature": self.temperature, "media_type": "text"},
            )
        except Exception as e:
            raise BaseLLMException(f"Error generating completion: {e}")
