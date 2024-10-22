# God LLM 🤖

A framework for recursive thought expansion and exploration using Large Language Models.

> Inspired by the article I wrote [Let's Build a God LLM](https://medium.com/@islamhachimi/lets-a-build-a-god-llm-0beaf2460659) which explores the concept of recursive thought expansion and deep exploration using language models.

## 🌟 Features

### Core Functionality
- **Recursive Thought Expansion**: Generate and explore interconnected thoughts while maintaining context
- **Context Preservation**: Maintains parent context during deep exploration
- **Relevance Filtering**: Automatically removes irrelevant thought branches
- **Detailed Reporting**: Generate comprehensive analysis of thought patterns
- **Debug Mode**: Conditional logging for development (`DEBUG=True|False`)
- **Enhanced Visualization**: Better representation of thought trees

### Advanced Capabilities
- **Grounded Prompting**: Improved prompt templates to maintain focus
- **Context Management**: Efficient handling of conversation history
- **Custom Visualization**: Methods for displaying thought hierarchies

## 🛠️ Upcoming Features

### High Priority
- **Tool Integration**
  - [ ] Implement `with_tools()` method for LLM classes
  - [ ] Support for Tavily integration
  - [ ] RAG (Retrieval Augmented Generation) implementation
  - [ ] Function calling in BaseLLM inheritor classes
  - [ ] Off-the-shelf tool library
  - [ ] Custom tool creation framework

### Technical Improvements
- [ ] Fix infinite expansion in `expand()` method
- [ ] Implement comprehensive test suite
- [ ] Enhanced graph visualization
- [ ] Better divergence control in thought expansion

## 🚀 Getting Started

```python
from god_llm.core.god import God
from god_llm.plugins.groq import ChatGroq

llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    api_key="gsk_oLJNYyXBJsbhTjKncdhaWGdyb3FY7SERaUTLJqfQpPS1RSwoszKyhH", #Dummy API key
)
god = God(llm=llm)

god.expand("Why?")
```

## 📘 Usage Examples

### Basic Thought Expansion
```python
god.report()
```

### Using Tools
```python
# Coming soon
llm = llm.with_tools([
    TavilyTool(),
    CustomTool(),
    RAGTool()
])
```

## 🤝 Contributing

Contributions are welcome! Please check out our [contribution guidelines](CONTRIBUTING.md) before getting started.

## 🐛 Known Issues

- `expand()` method may run indefinitely in certain cases
- Graph visualization can diverge from initial prompt
- Deep expansion may lose context of original prompt

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original concept inspired by [Islam Hachimi's article](https://medium.com/@islamhachimi/lets-a-build-a-god-llm-0beaf2460659)
- All contributors and feedback providers

---
Built with ❤️ for better thought exploration