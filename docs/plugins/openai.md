# OpenAI Integration

The `ChatOpenAI` class provides integration with OpenAI's language models. This implementation maintains consistency with the library's interface while handling OpenAI-specific requirements.

## Class Overview

```python
class ChatOpenAI(BaseLLM):
    def __init__(
        self,
        model_name: OpenAIModel,
        temperature: Optional[TemperatureValidator] = 0.7,
        api_key: Optional[str] = None,
    )
```

## Parameters

- `model_name`: The specific OpenAI model to use
- `temperature`: Controls response randomness (0.0 to 1.0)
- `api_key`: Optional API key for authentication

## Methods

### generate(prompt: str) -> AIMessage

Generates a completion using the OpenAI API:

- Formats messages according to OpenAI's chat completion format
- Includes system message for consistent behavior
- Returns structured response in `AIMessage` format
- Includes metadata about the generation settings

## Error Handling

API errors are caught and wrapped in `BaseLLMException` for consistent error handling across the library.

## Example Usage

```python
from god_llm.plugins import ChatOpenAI

# Initialize the client
openai = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7
)

# Generate a response
try:
    response = openai.generate("Explain neural networks")
    print(response.content)
except BaseLLMException as e:
    print(f"Error: {e}")
```