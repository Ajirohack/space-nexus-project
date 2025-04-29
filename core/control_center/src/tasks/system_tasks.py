"""
System management tasks for Control Center agents.
"""
from crewai import Task
from typing import Dict, List, Any, Callable, Optional


def create_system_health_check_task(
    agent_name: str,
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to check system health.
    
    Args:
        agent_name: Name of the agent to assign the task to
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    return Task(
        description=(
            "Perform a comprehensive health check of all system components. "
            "Analyze their current status, performance metrics, and identify any issues. "
            "Create a detailed report with your findings including any recommendations."
        ),
        expected_output=(
            "A detailed health report with status of all components, identified issues, "
            "performance analysis, and specific recommendations for improvements or fixes."
        ),
        agent=agent_name,
        context=context or {}
    )


def create_incident_response_task(
    agent_name: str, 
    incident_details: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to respond to a system incident.
    
    Args:
        agent_name: Name of the agent to assign the task to
        incident_details: Details of the incident
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({"incident_details": incident_details})
    
    return Task(
        description=(
            f"Investigate and respond to the following incident: {incident_details.get('title', 'Unknown incident')}. "
            f"The incident was detected in component: {incident_details.get('component', 'unknown')}. "
            f"Details: {incident_details.get('description', 'No details provided')}. "
            "Analyze the incident, determine its impact, propose a solution, and take appropriate actions."
        ),
        expected_output=(
            "A comprehensive incident report including analysis of the incident, steps taken to address it, "
            "current status, and recommendations to prevent similar incidents in the future."
        ),
        agent=agent_name,
        context=context
    )


def create_performance_optimization_task(
    agent_name: str,
    component_name: str,
    metrics: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to optimize system performance.
    
    Args:
        agent_name: Name of the agent to assign the task to
        component_name: Name of the component to optimize
        metrics: Performance metrics for the component
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({
        "component_name": component_name,
        "metrics": metrics
    })
    
    return Task(
        description=(
            f"Analyze the performance of {component_name} based on the provided metrics. "
            "Identify bottlenecks, inefficiencies, or areas for improvement. "
            "Create an optimization plan to enhance the component's performance."
        ),
        expected_output=(
            "A detailed optimization plan including specific issues identified, "
            "recommended changes, expected improvements, and implementation steps."
        ),
        agent=agent_name,
        context=context
    )


def create_system_update_task(
    agent_name: str,
    update_details: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to plan and execute a system update.
    
    Args:
        agent_name: Name of the agent to assign the task to
        update_details: Details of the update
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({"update_details": update_details})
    
    return Task(
        description=(
            f"Plan and execute the following system update: {update_details.get('title', 'Unknown update')}. "
            f"Components affected: {update_details.get('components', ['unknown'])}. "
            f"Update description: {update_details.get('description', 'No details provided')}. "
            "Create an update plan, including safety measures, rollback procedures, and verification steps."
        ),
        expected_output=(
            "A complete update execution report including the plan, steps taken, verification results, "
            "any issues encountered, and post-update status of all affected components."
        ),
        agent=agent_name,
        context=context
    )