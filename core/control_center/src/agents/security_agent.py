"""
Security Agent for Control Center.
Responsible for security monitoring, threat detection, and protection.
"""
from crewai import Agent
from typing import Dict, List, Any, Optional


def create_security_agent(api_key: str, config: Optional[Dict[str, Any]] = None) -> Agent:
    """
    Create a Security agent.
    
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
        name="SecuritySpecialist",
        role="Security and Threat Protection Specialist",
        goal="Secure the system from threats, monitor for security issues, and respond to incidents",
        backstory=(
            "You are a security expert with a background in AI systems protection. "
            "You constantly monitor for potential security threats, unauthorized access attempts, "
            "and suspicious behaviors. Your role is to ensure the system remains secure and to "
            "respond appropriately to any security incidents."
        ),
        verbose=config.get("verbose", True),
        allow_delegation=True,
        max_delegation=1,
        tools=config.get("tools", []),
        # Use the LLM API key provided
        llm_config={
            "model": "gpt-4",  # or config.get("model", "gpt-4")
            "api_key": api_key,
            "temperature": 0.1
        }
    )