# Anthropic Integration

The `ChatAnthropic` class provides integration with Anthropic's language models through their official API. This implementation handles authentication, message formatting, and response processing specific to Anthropic's requirements.

## Class Overview

```python
class ChatAnthropic(BaseLLM):
    def __init__(
        self,
        model_name: AnthropicModel,
        temperature: Optional[TemperatureValidator] = 0.7,
        api_key: Optional[str] = None,
    )
```

## Parameters

- `model_name`: The specific Anthropic model to use (e.g., "claude-3")
- `temperature`: Controls response randomness (0.0 to 1.0)
- `api_key`: Optional API key for authentication

## Methods

### generate(prompt: str) -> AIMessage

Generates a completion using the Anthropic API:

- Includes system message defining assistant behavior
- Handles message formatting according to Anthropic's requirements
- Returns structured response in `AIMessage` format
- Includes metadata about the generation settings

## Error Handling

Errors during generation are wrapped in `BaseLLMException` with detailed error messages.

## Example Usage

```python
from god_llm.plugins import ChatAnthropic

# Initialize the client
anthropic = ChatAnthropic(
    model_name="claude-3",
    temperature=0.7
)

# Generate a response
try:
    response = anthropic.generate("Explain quantum computing")
    print(response.content)
except BaseLLMException as e:
    print(f"Error: {e}")
```