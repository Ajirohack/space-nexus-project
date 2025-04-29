"""
Tasks module for the Control Center.
Provides access to all task creation functions.
"""
# System tasks
from .system_tasks import (
    create_system_health_check_task,
    create_incident_response_task,
    create_performance_optimization_task,
    create_system_update_task
)

# AI tasks
from .ai_tasks import (
    create_ai_council_coordination_task,
    create_ai_behavior_analysis_task,
    create_mode_optimization_task,
    create_ai_error_analysis_task
)

# User tasks
from .user_tasks import (
    create_user_permission_review_task,
    create_mode_elevation_review_task,
    create_user_activity_analysis_task,
    create_user_feedback_analysis_task
)

# Export all task creators
__all__ = [
    # System tasks
    'create_system_health_check_task',
    'create_incident_response_task',
    'create_performance_optimization_task',
    'create_system_update_task',
    
    # AI tasks
    'create_ai_council_coordination_task',
    'create_ai_behavior_analysis_task',
    'create_mode_optimization_task',
    'create_ai_error_analysis_task',
    
    # User tasks
    'create_user_permission_review_task',
    'create_mode_elevation_review_task',
    'create_user_activity_analysis_task',
    'create_user_feedback_analysis_task'
]