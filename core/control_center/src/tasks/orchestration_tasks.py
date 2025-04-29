"""
Orchestration tasks for the Control Center.
Handles task creation for workflow orchestration across system components.
"""
import logging
from typing import Dict, Any, Optional
from crewai import Task

logger = logging.getLogger("control_center.tasks.orchestration")

def create_workflow_planning_task(agent: Any, context: Dict[str, Any]) -> Task:
    """
    Create a task for planning complex workflows across system components.
    
    Args:
        agent: The agent to assign this task to
        context: Context information including workflow requirements
        
    Returns:
        Task object for workflow planning
    """
    return Task(
        description=f"""
        Plan an optimal workflow to accomplish the following objective: {context.get('objective')}.
        
        Consider the following requirements:
        1. Available components: {', '.join(context.get('available_components', []))}
        2. Expected output format: {context.get('output_format', 'JSON')}
        3. Performance constraints: {context.get('performance_constraints', 'None')}
        4. Security requirements: {context.get('security_requirements', 'Standard')}
        
        Your plan should include:
        - Component execution sequence
        - Data flow between components
        - Estimated resource usage
        - Error handling strategies
        - Validation checkpoints
        
        Output a complete workflow plan in JSON format.
        """,
        agent=agent,
        expected_output="""A detailed workflow plan in JSON format with component sequence, 
        data flow, resource estimates, error handling, and validation checkpoints."""
    )

def create_resource_allocation_task(agent: Any, context: Dict[str, Any]) -> Task:
    """
    Create a task for allocating resources to workflow components.
    
    Args:
        agent: The agent to assign this task to
        context: Context information including resource availability
        
    Returns:
        Task object for resource allocation
    """
    return Task(
        description=f"""
        Allocate system resources to the workflow components based on the following:
        1. Available compute resources: {context.get('available_compute', {})}
        2. Memory constraints: {context.get('memory_constraints', {})}
        3. Network bandwidth: {context.get('network_bandwidth', 'Standard')}
        4. Storage capacity: {context.get('storage_capacity', 'Unlimited')}
        5. Workflow priority: {context.get('priority', 'Medium')}
        
        For each component in the workflow ({', '.join(context.get('workflow_components', []))}),
        determine optimal resource allocation that ensures:
        - Performance requirements are met
        - System stability is maintained
        - Resources are used efficiently
        - Priority workflows get appropriate resources
        
        Output a resource allocation plan in JSON format.
        """,
        agent=agent,
        expected_output="""A detailed resource allocation plan in JSON format 
        with compute, memory, network, and storage allocations for each component."""
    )

def create_workflow_execution_task(agent: Any, context: Dict[str, Any]) -> Task:
    """
    Create a task for executing and monitoring a workflow.
    
    Args:
        agent: The agent to assign this task to
        context: Context information including the workflow plan
        
    Returns:
        Task object for workflow execution and monitoring
    """
    return Task(
        description=f"""
        Execute and monitor the workflow described in the provided plan:
        {context.get('workflow_plan', {})}
        
        Your responsibilities include:
        1. Initiating each component in the correct sequence
        2. Monitoring component status and performance
        3. Handling component failures and exceptions
        4. Managing data flow between components
        5. Reporting progress at each checkpoint
        6. Validating intermediate and final outputs
        
        Adjust execution as needed to maintain performance and reliability.
        Output execution status updates and final results.
        """,
        agent=agent,
        expected_output="""A comprehensive execution report with component status, 
        performance metrics, any adjustments made, and final workflow results."""
    )

def create_cross_component_optimization_task(agent: Any, context: Dict[str, Any]) -> Task:
    """
    Create a task for optimizing interactions between different system components.
    
    Args:
        agent: The agent to assign this task to
        context: Context information including component metrics
        
    Returns:
        Task object for cross-component optimization
    """
    return Task(
        description=f"""
        Analyze and optimize interactions between the following system components:
        {', '.join(context.get('components', []))}
        
        Using the performance metrics:
        {context.get('performance_metrics', {})}
        
        And the interaction patterns:
        {context.get('interaction_patterns', {})}
        
        Identify:
        1. Bottlenecks in cross-component communication
        2. Redundant data transfers
        3. Synchronization issues
        4. Resource contention points
        5. Opportunities for parallel processing
        
        Propose specific optimizations for each identified issue, prioritizing:
        - Reduced latency
        - Lower resource usage
        - Improved throughput
        - Enhanced reliability
        
        Output a detailed optimization plan with specific recommendations.
        """,
        agent=agent,
        expected_output="""A detailed optimization plan identifying bottlenecks, 
        redundancies, and other issues with specific recommendations for improvement."""
    )
"""