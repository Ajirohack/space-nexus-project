"""
AI management tasks for Control Center agents.
"""
from crewai import Task
from typing import Dict, List, Any, Optional


def create_ai_council_coordination_task(
    agent_name: str,
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to coordinate with the AI Council.
    
    Args:
        agent_name: Name of the agent to assign the task to
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    return Task(
        description=(
            "Coordinate with the AI Council to ensure optimal agent performance. "
            "Review recent AI Council activities, analyze their decision patterns, and "
            "provide guidance on improving multi-agent coordination and efficiency."
        ),
        expected_output=(
            "A coordination report detailing AI Council performance analysis, identified "
            "improvement areas, recommended adjustments to agent behaviors, and "
            "specific guidance for enhancing multi-agent coordination."
        ),
        agent=agent_name,
        context=context or {}
    )


def create_ai_behavior_analysis_task(
    agent_name: str,
    behavior_data: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to analyze AI behavior patterns.
    
    Args:
        agent_name: Name of the agent to assign the task to
        behavior_data: Data about AI behavior to analyze
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({"behavior_data": behavior_data})
    
    return Task(
        description=(
            "Analyze the provided AI behavior data to identify patterns, anomalies, or potential issues. "
            "Focus on decision consistency, reasoning patterns, potential biases, and alignment with "
            "system objectives. Provide recommendations for behavior optimization."
        ),
        expected_output=(
            "A comprehensive behavior analysis report with identified patterns, anomalies, "
            "evaluation of alignment with objectives, and specific recommendations for "
            "adjustments to improve AI decision-making quality and consistency."
        ),
        agent=agent_name,
        context=context
    )


def create_mode_optimization_task(
    agent_name: str,
    mode: str,
    usage_data: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to optimize a specific operation mode.
    
    Args:
        agent_name: Name of the agent to assign the task to
        mode: The mode to optimize (archivist, orchestrator, godfather, entity)
        usage_data: Data about mode usage patterns
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({
        "mode": mode,
        "usage_data": usage_data
    })
    
    return Task(
        description=(
            f"Analyze and optimize the '{mode}' operational mode based on the provided usage data. "
            f"Evaluate the effectiveness, efficiency, and user satisfaction of this mode. "
            f"Identify specific areas for improvement in agent configuration, tool usage, and response quality."
        ),
        expected_output=(
            f"A detailed optimization plan for the '{mode}' mode including specific configuration changes, "
            "tool access adjustments, agent behavior modifications, and expected improvements in "
            "performance metrics and user satisfaction."
        ),
        agent=agent_name,
        context=context
    )


def create_ai_error_analysis_task(
    agent_name: str,
    error_data: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to analyze AI system errors.
    
    Args:
        agent_name: Name of the agent to assign the task to
        error_data: Data about errors to analyze
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({"error_data": error_data})
    
    return Task(
        description=(
            "Analyze the provided AI system error data to identify root causes, patterns, and systemic issues. "
            "Focus on understanding why these errors occurred, their impact on system performance, "
            "and how they can be prevented in the future."
        ),
        expected_output=(
            "A comprehensive error analysis report with categorized error types, identified root causes, "
            "impact assessment, error patterns, and specific recommendations for addressing each "
            "error category and preventing similar issues in the future."
        ),
        agent=agent_name,
        context=context
    )