# System Engine Control

## Overview

System Engine Control is a core component of the Space WH platform that manages workflow orchestration and request routing based on user modes. It uses LangGraph for implementing mode-based workflow management and provides integration with other core components like AI Council, RAG System, and Tools/Packages System.

## Architecture

The System Engine Control component follows a graph-based workflow architecture:

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ API Interface │────▶│ Engine Router │────▶│  Engine Tiers │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     ▲                     │
        │                     │                     │
        │                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Permission    │     │ Workflow      │     │ Component     │
│ Control       │────▶│ Management    │◀────│ Integration   │
└───────────────┘     └───────────────┘     └───────────────┘
```

### Key Components

1. **Control Interface (`control.py`)** - The main interface for interacting with the System Engine Control
2. **Workflow Management (`workflow.py`)** - Graph-based workflow using LangGraph
3. **Engine Router (`router.py`)** - Routes requests to the appropriate engine based on user mode
4. **Engine Implementations (`engines.py`)** - Processing logic for each engine tier
5. **API Service (`api.py`)** - RESTful API for accessing the System Engine Control

## Features

- **Mode-Based Engine Selection**: Routes requests to appropriate engines based on user mode (Archivist, Orchestrator, Godfather, Entity)
- **Graph-Based Workflow**: Uses LangGraph for sophisticated workflow management
- **Component Integration**: Integrates with AI Council, RAG System, and Tools/Packages System
- **REST API**: Provides a RESTful interface for other components to interact with
- **Request Tracking**: Monitors active requests and provides status information
- **Error Handling**: Comprehensive error handling and recovery mechanisms

## User Modes and Engine Tiers

The System Engine Control supports four user modes, each with a corresponding engine tier:

| Mode | Engine | AI Council Configuration | Available Tools | Memory Persistence |
|------|--------|--------------------------|-----------------|-------------------|
| Archivist | Engine 1 | Basic (2 Agents) | Basic search, document reading | Session-only |
| Orchestrator | Engine 2 | Standard (5 Agents) | Advanced search, document R/W, data analysis | Short-term |
| Godfather | Engine 3 | Advanced (7 Agents) | Comprehensive tools, code development | Medium-term |
| Entity | Engine 4 | Complete (8+ Agents) | Unrestricted tools, advanced automation | Long-term |

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Programmatic Usage

```python
from core.engine_control.src import SystemEngineControl, RequestInput

# Initialize system engine control
engine_control = SystemEngineControl(
    ai_council=ai_council,  # Your AI Council instance
    rag_system=rag_system,  # Your RAG System instance
    tools_system=tools_system  # Your Tools System instance
)

# Create a request
request = RequestInput(
    user_id="user123",
    message="What is the capital of France?",
    mode="archivist",  # or "orchestrator", "godfather", "entity"
    context={}
)

# Process the request
response = await engine_control.process_request(request)

# Access the response
print(response.response)  # The text response
print(response.tools_used)  # List of tools used
print(response.processing_time_ms)  # Processing time in milliseconds
print(response.metadata)  # Additional metadata
```

### Running the API Service

```bash
# Run with default settings
python -m core.engine_control.src.main

# Run with custom host and port
python -m core.engine_control.src.main --host 127.0.0.1 --port 8080

# Run in debug mode
python -m core.engine_control.src.main --debug
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /status` - Get system status
- `GET /active-requests` - List active requests
- `POST /process` - Process a new request
- `DELETE /requests/{request_id}` - Cancel an active request

## Integration with Other Components

The System Engine Control is designed to integrate with:

1. **AI Council**: For multi-agent collaboration
2. **RAG System**: For knowledge retrieval
3. **Tools/Packages System**: For tool execution

These components should be initialized and passed to the SystemEngineControl constructor.

## Development

### Project Structure

```
core/engine_control/
├── requirements.txt         # Dependencies
├── README.md                # This file
└── src/
    ├── __init__.py          # Package exports
    ├── schemas.py           # Data schemas
    ├── router.py            # Mode-based routing
    ├── engines.py           # Engine implementations
    ├── workflow.py          # LangGraph workflow
    ├── control.py           # Main control interface
    ├── api.py               # REST API service
    └── main.py              # CLI entrypoint
```

### Adding a New Engine

To add a new engine tier:

1. Create a new Engine class in `engines.py`
2. Update the router in `router.py` to include the new engine
3. Add the engine to the workflow in `workflow.py`

## License

Copyright © 2025 Space WH Project
