"""
AI Analytics Crew for Control Center.
Handles advanced AI monitoring, optimization, and behavior analysis.
"""
import logging
from typing import Dict, List, Any, Optional
from crewai import Crew, Agent, Task, Process

from ..agents import create_agent

# Logger setup
logger = logging.getLogger("control_center.ai_analytics_crew")


class AIAnalyticsCrew:
    """
    AI Analytics crew for specialized AI system monitoring.
    Focuses on AI-specific analytics, optimization, and coordination with the AI Council.
    """
    
    def __init__(
        self,
        api_key: str,
        control_center: Any,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the AI Analytics Crew.
        
        Args:
            api_key: API key for the LLM
            control_center: Reference to the Control Center
            config: Additional configuration options
        """
        self.api_key = api_key
        self.control_center = control_center
        self.config = config or {}
        
        # Create the agents for this crew
        self.ai_coordinator = create_agent("ai_coordinator", api_key, config.get("ai_coordinator_config"))
        self.monitoring_agent = create_agent("monitoring", api_key, config.get("monitoring_config"))
        
        # Initialize the crew
        self.crew = Crew(
            agents=[self.ai_coordinator, self.monitoring_agent],
            tasks=[],  # Tasks will be added dynamically
            verbose=config.get("verbose", True),
            process=Process.sequential,  # or Process.hierarchical
            manager_llm_config={
                "model": config.get("manager_model", "gpt-4"),
                "api_key": api_key,
                "temperature": 0.1
            }
        )
        
        logger.info("AI Analytics Crew initialized")
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the crew.
        
        Args:
            task: Task to add
        """
        self.crew.tasks.append(task)
        logger.info(f"Added task to AI Analytics Crew: {task.description[:50]}...")
    
    def run(self) -> Dict[str, Any]:
        """
        Run the AI analytics crew with its current tasks.
        
        Returns:
            Dictionary with task results
        """
        if not self.crew.tasks:
            logger.warning("No tasks assigned to AI Analytics Crew")
            return {"error": "No tasks assigned"}
        
        logger.info(f"Running AI Analytics Crew with {len(self.crew.tasks)} tasks")
        
        try:
            results = self.crew.kickoff()
            logger.info("AI Analytics Crew completed tasks successfully")
            return {"results": results}
        except Exception as e:
            logger.error(f"Error running AI Analytics Crew: {str(e)}")
            return {"error": str(e)}
    
    def reset_tasks(self) -> None:
        """Reset all tasks in the crew."""
        self.crew.tasks = []
        logger.info("Reset all tasks in AI Analytics Crew")
    
    def analyze_ai_behavior(self, behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze AI behavior patterns.
        
        Args:
            behavior_data: Data about AI behavior to analyze
            
        Returns:
            Behavior analysis results
        """
        from ..tasks import create_ai_behavior_analysis_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create an AI behavior analysis task
        behavior_task = create_ai_behavior_analysis_task(
            agent_name=self.ai_coordinator.name,
            behavior_data=behavior_data,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(behavior_task)
        
        # Run the crew to analyze AI behavior
        return self.run()
    
    def optimize_operation_mode(self, mode: str, usage_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize a specific operation mode.
        
        Args:
            mode: The mode to optimize (archivist, orchestrator, godfather, entity)
            usage_data: Data about mode usage patterns
            
        Returns:
            Mode optimization results
        """
        from ..tasks import create_mode_optimization_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a mode optimization task
        optimization_task = create_mode_optimization_task(
            agent_name=self.ai_coordinator.name,
            mode=mode,
            usage_data=usage_data,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(optimization_task)
        
        # Run the crew to optimize the operation mode
        return self.run()
    
    def coordinate_with_ai_council(self, council_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Coordinate with the AI Council to align system goals and behavior.
        
        Args:
            council_data: Optional data about recent AI Council activities/decisions
            
        Returns:
            Coordination results
        """
        from ..tasks import create_ai_council_coordination_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create context with council data if provided
        context = {"council_data": council_data} if council_data else None
        
        # Create a council coordination task
        council_task = create_ai_council_coordination_task(
            agent_name=self.ai_coordinator.name,
            control_center=self.control_center,
            context=context
        )
        
        # Add the task to the crew
        self.add_task(council_task)
        
        # Run the crew to coordinate with the AI Council
        return self.run()
    
    def analyze_ai_errors(self, error_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze AI system errors.
        
        Args:
            error_data: Data about AI errors to analyze
            
        Returns:
            Error analysis results
        """
        from ..tasks import create_ai_error_analysis_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create an AI error analysis task
        error_task = create_ai_error_analysis_task(
            agent_name=self.ai_coordinator.name,
            error_data=error_data,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(error_task)
        
        # Run the crew to analyze AI errors
        return self.run()