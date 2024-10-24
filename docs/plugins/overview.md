# Plugins Overview

The God LLM library implements a plugin-based architecture that allows for easy integration of different LLM providers and extensibility of functionality. This document outlines the core concepts, components, and implementation details of the plugin system.

## Architecture Overview

The plugin system is built around several key components:

### 1. Base Classes

#### BaseLLM
The foundation of the plugin system, providing the interface that all LLM providers must implement:

```python
class BaseLLM(ABC):
    def __init__(self, provider: LLMProviderType, api_key: Optional[str] = None):
        self.provider = provider
        self.auth = Auth()
        if api_key:
            self.auth.set_key(provider, api_key)
        elif not self.auth.get_key(provider):
            raise ValueError(f"No API key provided or found for {provider}")

    @abstractmethod
    def generate(self, prompt: str) -> AIMessage:
        pass
```

#### BaseMessage and Derivatives
Message classes that standardize communication:

```python
class BaseMessage(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    content: str
    created_at: datetime.datetime
    metadata: Optional[Dict[str, Any]] = None
```

### 2. Provider Plugins

Each LLM provider is implemented as a plugin that inherits from `BaseLLM`:

- **ChatAnthropic**: Anthropic Claude models
- **ChatGroq**: Groq LLM services
- **ChatOpenAI**: OpenAI GPT models

### 3. Type System

The library uses a robust type system to ensure consistency:

```python
LLMProviderType = Literal["ollama", "openai", "anthropic", "bedrock", "groq"]

GroqModel = Literal[
    "gemma2-9b-it",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
]

# Similar literals for OpenAI and Anthropic models
```

## Plugin Implementation

### Provider Plugin Structure

Each provider plugin follows this general structure:

1. **Initialization**:
   - Set up authentication
   - Configure provider-specific client
   - Initialize model parameters

2. **Message Generation**:
   - Format prompts according to provider requirements
   - Handle API communication
   - Process and standardize responses

Example:
```python
class ChatProvider(BaseLLM):
    def __init__(
        self,
        model_name: ModelType,
        temperature: Optional[TemperatureValidator] = 0.7,
        api_key: Optional[str] = None,
    ):
        super().__init__("provider_name", api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.client = self._initialize_client()

    def generate(self, prompt: str) -> AIMessage:
        try:
            response = self._generate_response(prompt)
            return self._format_response(response)
        except Exception as e:
            raise BaseLLMException(str(e))
```

### Common Features Across Plugins

All plugins implement:

1. **Temperature Control**:
   - Standardized temperature validation
   - Consistent application across providers

2. **Error Handling**:
   - Provider-specific errors wrapped in `BaseLLMException`
   - Consistent error reporting format

3. **Message Formatting**:
   - Standardized input/output message format
   - Provider-specific message adaptation

4. **Metadata Handling**:
   - Common metadata fields across providers
   - Provider-specific metadata extensions

## Adding New Plugins

To add a new provider plugin:

1. Create a new class inheriting from `BaseLLM`
2. Implement required methods:
   - `__init__`
   - `generate`
3. Add provider type to `LLMProviderType`
4. Define model types if needed
5. Implement error handling

Example template:
```python
from god_llm.plugins.base import BaseLLM, AIMessage
from god_llm.plugins.exceptions import BaseLLMException

class NewProvider(BaseLLM):
    def __init__(
        self,
        model_name: str,
        temperature: Optional[TemperatureValidator] = 0.7,
        api_key: Optional[str] = None,
    ):
        super().__init__("new_provider", api_key)
        self.model_name = model_name
        self.temperature = temperature
        # Initialize provider-specific client

    def generate(self, prompt: str) -> AIMessage:
        try:
            # Implementation details here
            return AIMessage(...)
        except Exception as e:
            raise BaseLLMException(f"Error: {e}")
```

## Best Practices

1. **Error Handling**:
   - Always wrap provider-specific errors
   - Provide meaningful error messages
   - Use appropriate error types

2. **Type Safety**:
   - Use type hints consistently
   - Define provider-specific types
   - Validate inputs appropriately

3. **Configuration**:
   - Use environment variables when possible
   - Provide clear configuration options
   - Document required settings

4. **Testing**:
   - Write unit tests for each plugin
   - Test error conditions
   - Mock API responses

## Future Extensions

The plugin system is designed to be extensible for future additions:

1. **New Providers**:
   - Additional LLM providers
   - Different model types
   - Custom implementations

2. **Enhanced Features**:
   - Streaming responses
   - Batch processing
   - Advanced parameter control

3. **Tool Integration**:
   - Function calling
   - External tool integration
   - Custom capabilities