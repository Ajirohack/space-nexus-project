"""
User management tasks for Control Center agents.
"""
from crewai import Task
from typing import Dict, List, Any, Optional


def create_user_permission_review_task(
    agent_name: str,
    user_id: str,
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to review and manage user permissions.
    
    Args:
        agent_name: Name of the agent to assign the task to
        user_id: ID of the user to review
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({"user_id": user_id})
    
    return Task(
        description=(
            f"Review the permissions and access levels for user {user_id}. "
            "Analyze their current permissions, usage patterns, and any recent access requests. "
            "Determine if their current access level is appropriate, and recommend any changes."
        ),
        expected_output=(
            "A detailed permission review report including current permissions, usage analysis, "
            "identified issues or anomalies, and specific recommendations for permission adjustments."
        ),
        agent=agent_name,
        context=context
    )


def create_mode_elevation_review_task(
    agent_name: str,
    user_id: str,
    current_mode: str,
    requested_mode: str,
    justification: str,
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to review a user's request for mode elevation.
    
    Args:
        agent_name: Name of the agent to assign the task to
        user_id: ID of the user requesting mode elevation
        current_mode: User's current mode
        requested_mode: Mode the user is requesting
        justification: User's justification for the request
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({
        "user_id": user_id,
        "current_mode": current_mode,
        "requested_mode": requested_mode,
        "justification": justification
    })
    
    return Task(
        description=(
            f"Review user {user_id}'s request to elevate from {current_mode} mode to {requested_mode} mode. "
            f"Their justification is: '{justification}'. "
            "Analyze the user's history, permissions, and the validity of their justification. "
            "Determine whether this mode elevation should be approved or denied."
        ),
        expected_output=(
            "A comprehensive review decision including analysis of the user's history, the validity "
            "of their justification, security considerations, any recommended restrictions or "
            "conditions, and a clear approval or denial recommendation with rationale."
        ),
        agent=agent_name,
        context=context
    )


def create_user_activity_analysis_task(
    agent_name: str,
    user_id: str,
    activity_data: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to analyze user activity patterns.
    
    Args:
        agent_name: Name of the agent to assign the task to
        user_id: ID of the user to analyze
        activity_data: Data about user activity
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({
        "user_id": user_id,
        "activity_data": activity_data
    })
    
    return Task(
        description=(
            f"Analyze the activity patterns for user {user_id} based on the provided data. "
            "Look for patterns in their tool usage, query types, response interactions, and general behavior. "
            "Identify any anomalies, potential security concerns, or areas where their experience could be improved."
        ),
        expected_output=(
            "A detailed user activity analysis including identified usage patterns, anomaly detection results, "
            "potential security concerns, and specific recommendations for improving the user's experience "
            "or addressing any identified issues."
        ),
        agent=agent_name,
        context=context
    )


def create_user_feedback_analysis_task(
    agent_name: str,
    feedback_data: Dict[str, Any],
    control_center: Any,
    context: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a task to analyze user feedback.
    
    Args:
        agent_name: Name of the agent to assign the task to
        feedback_data: User feedback data
        control_center: Reference to the Control Center
        context: Additional context for the task
        
    Returns:
        A CrewAI Task
    """
    context = context or {}
    context.update({"feedback_data": feedback_data})
    
    return Task(
        description=(
            "Analyze the provided user feedback data to identify common concerns, satisfaction levels, "
            "and areas for improvement. Categorize the feedback by type and severity, and identify "
            "actionable insights that can be used to enhance the system."
        ),
        expected_output=(
            "A comprehensive feedback analysis report with categorized feedback, identified patterns, "
            "priority areas for improvement, specific actionable recommendations, and expected "
            "impact on user satisfaction for each recommendation."
        ),
        agent=agent_name,
        context=context
    )