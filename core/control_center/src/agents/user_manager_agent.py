"""
User Manager Agent for Control Center.
Responsible for managing users, permissions, and access control.
"""
from crewai import Agent
from typing import Dict, List, Any, Optional


def create_user_manager_agent(api_key: str, config: Optional[Dict[str, Any]] = None) -> Agent:
    """
    Create a User Manager agent.
    
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
        name="UserManager",
        role="User Management Specialist",
        goal="Manage user accounts, permissions, and ensure proper access controls",
        backstory=(
            "You are a meticulous user management specialist with expertise in access control systems. "
            "Your role is to manage user accounts, handle permissions, mode changes, and ensure "
            "users have the appropriate level of access to the system based on their needs and authorization."
        ),
        verbose=config.get("verbose", True),
        allow_delegation=False,
        tools=config.get("tools", []),
        # Use the LLM API key provided
        llm_config={
            "model": "gpt-4",  # or config.get("model", "gpt-4")
            "api_key": api_key,
            "temperature": 0.1
        }
    )