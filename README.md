# Space-WH

A clean build implementation of the Space project, integrating modern AI agent frameworks for enhanced functionality and performance.

## Overview

Space-WH is a comprehensive AI system featuring a multi-layered architecture with tiered access modes, multi-agent orchestration, and extensive tool integration. It leverages cutting-edge frameworks including CrewAI, LangChain, AutoGen, and LangGraph to create a powerful, extensible system for AI-driven tasks.

## Architecture

Space-WH follows a three-layer architecture:

1. **User/Client Access Layer**
   - Client interfaces
   - User management
   - Frontend interfaces

2. **Admin Access & Control Layer**
   - API Gateway
   - Control Center
   - System Engine Control

3. **Core AI & Data Modules Layer**
   - AI Council (CrewAI)
   - RAG System (LangChain)
   - Tools/Packages (MCP & LangChain)
   - Tiered engines (AutoGen)

## Mode System

Space-WH implements a tiered mode system:

- **Archivist Mode**: Basic information retrieval and content generation
- **Orchestrator Mode**: Enhanced capabilities with advanced content creation
- **Godfather Mode**: Comprehensive access with professional tools
- **Entity Mode**: Unrestricted access with full system capabilities

## Key Components

- **AI Council**: Multi-agent orchestration using CrewAI
- **RAG System**: Knowledge retrieval with LangChain
- **Tools/Packages**: Extensible tool system with MCP
- **System Engine Control**: Workflow management with LangGraph
- **Engines**: Tiered processing using AutoGen

## Getting Started

1. Clone the repository
2. Install dependencies with `npm install`
3. Configure environment variables
4. Start the system with `npm start`

## Configuration

Create a `.env` file with the following variables:

```
PORT=3000
NODE_ENV=development
OPENAI_API_KEY=your-api-key
```

## Development

This project is under active development. Refer to the documentation in the `/docs` directory for implementation details and component guides.
