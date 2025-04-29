"""
Agents module for the Control Center.
Provides access to all agent creators.
"""
from typing import Dict, Any

from .system_admin_agent import create_system_admin_agent
from .monitoring_agent import create_monitoring_agent
from .ai_coordinator_agent import create_ai_coordinator_agent
from .user_manager_agent import create_user_manager_agent
from .security_agent import create_security_agent

# Map of agent types to their creation functions
AGENT_CREATORS = {
    "system_admin": create_system_admin_agent,
    "monitoring": create_monitoring_agent,
    "ai_coordinator": create_ai_coordinator_agent,
    "user_manager": create_user_manager_agent,
    "security": create_security_agent
}


def create_agent(agent_type: str, api_key: str, config: Dict[str, Any] = None):
    """
    Create an agent of the specified type.
    
    Args:
        agent_type: Type of agent to create
        api_key: API key for the LLM
        config: Additional configuration options
        
    Returns:
        CrewAI Agent instance
        
    Raises:
        ValueError: If the agent type is not supported
    """
    creator = AGENT_CREATORS.get(agent_type)
    if not creator:
        raise ValueError(f"Unsupported agent type: {agent_type}")
    
    return creator(api_key, config)