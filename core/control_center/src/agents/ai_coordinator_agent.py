"""
AI Coordinator Agent for Control Center.
Responsible for managing and coordinating AI components.
"""
from crewai import Agent
from typing import Dict, List, Any, Optional


def create_ai_coordinator_agent(api_key: str, config: Optional[Dict[str, Any]] = None) -> Agent:
    """
    Create an AI Coordinator agent.
    
    Args:
        api_key: API key for the LLM
        config: Additional configuration options
        
    Returns:
        CrewAI Agent
    """
    # Use default config if none provided
    config = config or {}
    
    # Create the agent with detailed role and goals
    return Agent(
        name="AICoordinator",
        role="AI Systems Coordinator",
        goal="Manage AI components, coordinate responses, and ensure optimal AI behavior",
        backstory=(
            "You are an expert in AI systems management with specialized knowledge in multi-agent architectures. "
            "Your role is to coordinate the AI components of the Space WH system, analyze AI-related issues, "
            "and ensure all AI systems are functioning optimally and ethically."
        ),
        verbose=config.get("verbose", True),
        allow_delegation=True,
        max_delegation=2,
        tools=config.get("tools", []),
        # Use the LLM API key provided
        llm_config={
            "model": "gpt-4",  # or config.get("model", "gpt-4")
            "api_key": api_key,
            "temperature": 0.2
        }
    )