"""
System Administrator Agent for Control Center.
Responsible for overall system administration and management.
"""
from crewai import Agent
from typing import Dict, List, Any, Optional


def create_system_admin_agent(api_key: str, config: Optional[Dict[str, Any]] = None) -> Agent:
    """
    Create a System Administrator agent.
    
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
        name="SystemAdministrator",
        role="System Administrator",
        goal="Ensure the proper operation and maintenance of the Space WH system",
        backstory=(
            "You are an experienced system administrator with deep knowledge of AI systems. "
            "You're responsible for ensuring all components of the Space WH system are running "
            "properly, making administrative decisions, and coordinating responses to system issues."
        ),
        verbose=config.get("verbose", True),
        allow_delegation=True,
        max_delegation=3,
        tools=config.get("tools", []),
        # Use the LLM API key provided
        llm_config={
            "model": "gpt-4",  # or config.get("model", "gpt-4")
            "api_key": api_key,
            "temperature": 0.2
        }
    )