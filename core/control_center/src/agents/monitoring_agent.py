"""
Monitoring Agent for Control Center.
Responsible for monitoring system health and performance.
"""
from crewai import Agent
from typing import Dict, List, Any, Optional


def create_monitoring_agent(api_key: str, config: Optional[Dict[str, Any]] = None) -> Agent:
    """
    Create a Monitoring agent.
    
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
        name="SystemMonitor",
        role="System Monitoring Specialist",
        goal="Monitor and analyze system health, performance, and detect anomalies",
        backstory=(
            "You are a vigilant system monitor with expertise in performance analysis and anomaly detection. "
            "You continuously watch over the Space WH system to identify and report potential issues, "
            "bottlenecks, or unusual patterns that might affect system performance or reliability."
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