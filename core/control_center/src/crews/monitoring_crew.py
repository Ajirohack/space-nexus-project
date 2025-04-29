"""
Monitoring Crew for Control Center.
Handles system monitoring and AI coordination tasks.
"""
import logging
from typing import Dict, List, Any, Optional
from crewai import Crew, Agent, Task, Process

from ..agents import create_agent

# Logger setup
logger = logging.getLogger("control_center.monitoring_crew")


class MonitoringCrew:
    """
    Monitoring crew for system performance and AI coordination.
    Coordinates monitoring specialists and AI coordinators.
    """
    
    def __init__(
        self,
        api_key: str,
        control_center: Any,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Monitoring Crew.
        
        Args:
            api_key: API key for the LLM
            control_center: Reference to the Control Center
            config: Additional configuration options
        """
        self.api_key = api_key
        self.control_center = control_center
        self.config = config or {}
        
        # Create the agents for this crew
        self.monitoring_agent = create_agent("monitoring", api_key, config.get("monitoring_config"))
        self.ai_coordinator = create_agent("ai_coordinator", api_key, config.get("ai_coordinator_config"))
        
        # Initialize the crew
        self.crew = Crew(
            agents=[self.monitoring_agent, self.ai_coordinator],
            tasks=[],  # Tasks will be added dynamically
            verbose=config.get("verbose", True),
            process=Process.sequential,  # or Process.hierarchical
            manager_llm_config={
                "model": "gpt-4",  # or config.get("manager_model", "gpt-4")
                "api_key": api_key,
                "temperature": 0.1
            }
        )
        
        logger.info("Monitoring Crew initialized")
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the crew.
        
        Args:
            task: Task to add
        """
        self.crew.tasks.append(task)
        logger.info(f"Added task to Monitoring Crew: {task.description[:50]}...")
    
    def run(self) -> Dict[str, Any]:
        """
        Run the monitoring crew with its current tasks.
        
        Returns:
            Dictionary with task results
        """
        if not self.crew.tasks:
            logger.warning("No tasks assigned to Monitoring Crew")
            return {"error": "No tasks assigned"}
        
        logger.info(f"Running Monitoring Crew with {len(self.crew.tasks)} tasks")
        
        try:
            results = self.crew.kickoff()
            logger.info("Monitoring Crew completed tasks successfully")
            return {"results": results}
        except Exception as e:
            logger.error(f"Error running Monitoring Crew: {str(e)}")
            return {"error": str(e)}
    
    def reset_tasks(self) -> None:
        """Reset all tasks in the crew."""
        self.crew.tasks = []
        logger.info("Reset all tasks in Monitoring Crew")
    
    def coordinate_ai_council(self) -> Dict[str, Any]:
        """
        Coordinate with the AI Council.
        
        Returns:
            Coordination results
        """
        from ..tasks import create_ai_council_coordination_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create an AI Council coordination task
        coordination_task = create_ai_council_coordination_task(
            agent_name=self.ai_coordinator.name,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(coordination_task)
        
        # Run the crew to coordinate with the AI Council
        return self.run()
    
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
    
    def analyze_component_performance(self, component_name: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and optimize component performance.
        
        Args:
            component_name: Name of the component to analyze
            metrics: Performance metrics for the component
            
        Returns:
            Performance analysis results
        """
        from ..tasks import create_performance_optimization_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a performance optimization task
        performance_task = create_performance_optimization_task(
            agent_name=self.monitoring_agent.name,
            component_name=component_name,
            metrics=metrics,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(performance_task)
        
        # Run the crew to analyze component performance
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