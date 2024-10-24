# Groq Integration

The `ChatGroq` class implements integration with Groq's language models. This implementation provides a standardized interface while handling Groq-specific requirements for API interaction.

## Class Overview

```python
class ChatGroq(BaseLLM):
    def __init__(
        self,
        model_name: GroqModel,
        temperature: Optional[TemperatureValidator] = 0.7,
        api_key: Optional[str] = None,
    )
```

## Parameters

- `model_name`: The specific Groq model to use
- `temperature`: Controls response randomness (0.0 to 1.0)
- `api_key`: Optional API key for authentication

## Methods

### generate(prompt: str) -> AIMessage

Generates a completion using the Groq API:

- Formats messages according to Groq's specifications
- Includes system message for consistent behavior
- Returns structured response in `AIMessage` format
- Includes metadata about generation parameters

## Error Handling

All API errors are caught and wrapped in `BaseLLMException` for consistent error handling across the library.

## Example Usage

```python
from god_llm.plugins import ChatGroq

# Initialize the client
groq = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    temperature=0.7
)

# Generate a response
try:
    response = groq.generate("Explain machine learning")
    print(response.content)
except BaseLLMException as e:
    print(f"Error: {e}")
```