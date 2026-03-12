# AI Chat Template

AI chat template using **LangGraph**, **FastAPI**, and **Clean Architecture**.

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Project Setup](#-project-setup)
- [API Routes](#-api-routes)
- [Testing](#-testing)
- [Pre-commit](#-pre-commit)

---

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns in layers. The structure is organized as follows:

```
src/
├── domain/           # Business rules and interfaces
├── application/      # Application use cases
├── infrastructure/   # Infrastructure implementations
├── presentation/     # Presentation layer (DTOs, Controllers)
└── main/            # Application composition and configuration
```

### 📦 Application Layers

#### **Domain** (`src/domain/`)
Core application layer containing pure business rules.

**What to put here:**
- **`models/`**: Domain entities and data models
- **`strategies/`**: Strategy interfaces (e.g., `AIStrategyInterface`)
- **`use_cases/`**: Use case interfaces (e.g., `ChatAIInterface`)
- **`interfaces/`**: Domain contracts and abstractions

**Important rule:** This layer should NOT depend on any other layer. It only defines interfaces and business rules.

#### **Application** (`src/application/`)
Implementation of application use cases.

**What to put here:**
- **`use_cases/`**: Concrete implementations of use cases (e.g., `ChatAI`)
- Strategy orchestration and application logic
- Coordination between different domain components

#### **Infrastructure** (`src/infrastructure/`)
Technical implementations and external integrations.

**What to put here:**
- **`ai/`**: AI implementations (see detailed section below)
- **`config/`**: Application settings (`settings.py`)
- Database integrations, external APIs, etc.

#### **Presentation** (`src/presentation/`)
User/client interface layer.

**What to put here:**
- **`controllers/`**: Controllers that process HTTP requests
- **`dtos/`**: Data Transfer Objects for input/output validation
- **`http_types/`**: HTTP types (`HttpRequest`, `HttpResponse`)
- **`interfaces/`**: Controller interfaces
- **`middlewares/`**: Error handling middlewares

#### **Main** (`src/main/`)
Application composition and configuration.

**What to put here:**
- **`routes/`**: FastAPI route definitions
- **`composers/`**: Dependency injection factories
- **`adapters/`**: Request adapters
- **`server/`**: FastAPI server configuration
- **`dependencies/`**: Shared dependencies

### 🤖 AI Directory (`src/infrastructure/ai/`)

Dedicated directory for artificial intelligence implementations using LangGraph.

```
infrastructure/ai/
├── strategies/              # AI strategy implementations
│   └── langgraph_strategy.py  # LangGraph strategy
└── langgraph_services/      # LangGraph services and configurations
    ├── callbacks/           # Custom callback handlers
    │   └── custom_callback_handler.py
    ├── graphs/              # LangGraph graph definitions
    │   └── default_graph.py    # Default supervisor graph
    ├── interfaces/          # Graph builder interfaces
    │   └── graph_builder.py
    ├── middlewares/         # Graph middlewares
    │   └── handle_tool_errors.py
    ├── prompts/            # Prompt templates
    ├── states/             # Graph state definitions
    ├── tools/              # Tools for the graph
    └── utils/              # Utilities
```

**Main components:**

- **`strategies/langgraph_strategy.py`**: Implementation of `AIStrategyInterface` using LangGraph. Responsible for generating AI responses.

- **`langgraph_services/graphs/`**: Contains LangGraph execution graphs. The `default_graph.py` implements a supervisor pattern that can delegate tasks to multiple agents.

- **`langgraph_services/callbacks/`**: Custom handlers to capture events during graph execution (useful for logging, metrics, etc).

- **`langgraph_services/interfaces/graph_builder.py`**: Interface that defines the contract for graph construction, allowing different implementations.

---

## 🚀 Project Setup

### 1. **Configure OpenAI API Key**

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-api-key-here
APP_NAME="AI Chat Template"
APP_PORT=8999
APP_VERSION="0.1.0"
CONVERSATION_MODEL="gpt-4o"
```

**Available variables:**
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `APP_NAME`: Application name (optional)
- `APP_PORT`: Server port (default: 8999)
- `APP_VERSION`: Application version (optional)
- `CONVERSATION_MODEL`: Conversation model (default: "gpt-4.1")

### 2. **Sync Dependencies**

```bash
uv sync
```

This command will install all dependencies defined in `pyproject.toml`.

### 3. **Run the Application**

```bash
uv run python3 run.py
```

The server will be available at `http://localhost:8999`

---

## 🛣️ API Routes

### **Health Check**

Check the application status.

```
GET /
```

**Response:**
```json
{
  "status": "ok",
  "app": "AI Chat Template",
  "version": "0.1.0"
}
```

### **Send Message**

Send a message to the AI chat.

```
POST /api/chat/messages
```

**Body:**
```json
{
  "content": "hello"
}
```

**Response:**
```json
{
  "data": "Hello! How can I help you today?",
  "status_code": 201
}
```

**cURL example:**
```bash
curl -X POST "http://localhost:8999/api/chat/messages" \
  -H "Content-Type: application/json" \
  -d '{"content": "hello"}'
```

---

## 🧪 Testing

This project includes comprehensive unit tests for all major components.

### **Test Structure**

```
src/tests/
├── conftest.py           # Pytest fixtures and configuration
├── test_dtos.py          # DTO validation tests
├── test_use_cases.py     # Use case logic tests
├── test_controllers.py   # Controller tests
├── test_http_types.py    # HTTP types tests
├── test_adapters.py      # Adapter tests
└── test_settings.py      # Configuration tests
```

### **Running Tests**

Run all tests:
```bash
uv run pytest
```

Run tests with coverage:
```bash
uv run pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
uv run pytest src/tests/test_use_cases.py
```

Run specific test:
```bash
uv run pytest src/tests/test_use_cases.py::TestChatAI::test_send_message_success
```

Run tests in verbose mode:
```bash
uv run pytest -v
```

### **Test Coverage**

The tests cover:
- ✅ **DTOs**: Input validation and serialization
- ✅ **Use Cases**: Business logic and error handling
- ✅ **Controllers**: Request handling and response formatting
- ✅ **HTTP Types**: Request/Response structures
- ✅ **Adapters**: Request adaptation logic
- ✅ **Settings**: Configuration management

### **Writing New Tests**

When adding new features, follow these patterns:

1. **Use fixtures** from `conftest.py` for common mocks
2. **Test happy path** and error cases
3. **Use descriptive test names** that explain what is being tested
4. **Mark async tests** with `@pytest.mark.asyncio`

Example:
```python
@pytest.mark.asyncio
async def test_new_feature_success(mock_dependency):
    """Test that new feature works correctly."""
    # Arrange
    service = MyService(dependency=mock_dependency)
    
    # Act
    result = await service.do_something()
    
    # Assert
    assert result == expected_value
```

---

## 🔍 Pre-commit

This project uses pre-commit hooks to ensure code quality.

### **Configuration**

The `.pre-commit-config.yaml` file defines the following hooks:

1. **Pylint**: Python static code analysis
2. **Requirements**: Automatic `requirements.txt` update

### **Installation**

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

### **Usage**

Hooks will run automatically on every commit. To run manually:

```bash
# Run on all files
pre-commit run --all-files

# Run only pylint
pre-commit run pylint --all-files
```

---

## 🧩 Customization

### **Add Agents to Supervisor**

Edit the `src/main/composers/chat/send_message.py` file:

```python
graph_builder = _build_graph(
    llm=llm,
    crm_agents=[
        # Add your agents here
        # agent1,
        # agent2,
    ],
)
```

### **Modify AI Model**

Edit the `.env` file:

```bash
CONVERSATION_MODEL="gpt-4o"  # or another model
```

### **Add Tools**

1. Create your tools in `src/infrastructure/ai/langgraph_services/tools/`
2. Configure them in the appropriate composer

---

## 📝 Main Dependencies

- **FastAPI**: Web framework for APIs
- **LangGraph**: AI agent orchestration
- **LangChain**: Framework for LLM applications
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework

---

## 📄 License

This is a project template. Adapt it to your needs.
