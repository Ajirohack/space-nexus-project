"""
Security Crew for Control Center.
Handles system security, access control, and vulnerability management.
"""
import logging
from typing import Dict, List, Any, Optional
from crewai import Crew, Agent, Task, Process

from ..agents import create_agent

# Logger setup
logger = logging.getLogger("control_center.security_crew")


class SecurityCrew:
    """
    Security crew for system protection and access control.
    Focuses on security monitoring, threat detection, and vulnerability management.
    """
    
    def __init__(
        self,
        api_key: str,
        control_center: Any,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Security Crew.
        
        Args:
            api_key: API key for the LLM
            control_center: Reference to the Control Center
            config: Additional configuration options
        """
        self.api_key = api_key
        self.control_center = control_center
        self.config = config or {}
        
        # Create the agents for this crew
        self.security_agent = create_agent("security", api_key, config.get("security_config"))
        self.user_manager = create_agent("user_manager", api_key, config.get("user_manager_config"))
        
        # Initialize the crew
        self.crew = Crew(
            agents=[self.security_agent, self.user_manager],
            tasks=[],  # Tasks will be added dynamically
            verbose=config.get("verbose", True),
            process=Process.sequential,  # or Process.hierarchical
            manager_llm_config={
                "model": config.get("manager_model", "gpt-4"),
                "api_key": api_key,
                "temperature": 0.1
            }
        )
        
        logger.info("Security Crew initialized")
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the crew.
        
        Args:
            task: Task to add
        """
        self.crew.tasks.append(task)
        logger.info(f"Added task to Security Crew: {task.description[:50]}...")
    
    def run(self) -> Dict[str, Any]:
        """
        Run the security crew with its current tasks.
        
        Returns:
            Dictionary with task results
        """
        if not self.crew.tasks:
            logger.warning("No tasks assigned to Security Crew")
            return {"error": "No tasks assigned"}
        
        logger.info(f"Running Security Crew with {len(self.crew.tasks)} tasks")
        
        try:
            results = self.crew.kickoff()
            logger.info("Security Crew completed tasks successfully")
            return {"results": results}
        except Exception as e:
            logger.error(f"Error running Security Crew: {str(e)}")
            return {"error": str(e)}
    
    def reset_tasks(self) -> None:
        """Reset all tasks in the crew."""
        self.crew.tasks = []
        logger.info("Reset all tasks in Security Crew")
    
    def evaluate_security_posture(self) -> Dict[str, Any]:
        """
        Evaluate the overall security posture of the system.
        
        Returns:
            Security evaluation results
        """
        from ..tasks import create_security_evaluation_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a security evaluation task
        security_task = create_security_evaluation_task(
            agent_name=self.security_agent.name,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(security_task)
        
        # Run the crew to evaluate security posture
        return self.run()
    
    def analyze_access_patterns(self, access_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user access patterns for suspicious activity.
        
        Args:
            access_data: Data about user access patterns
            
        Returns:
            Access pattern analysis results
        """
        from ..tasks import create_access_pattern_analysis_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create an access pattern analysis task
        access_task = create_access_pattern_analysis_task(
            agent_name=self.security_agent.name,
            access_data=access_data,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(access_task)
        
        # Run the crew to analyze access patterns
        return self.run()
    
    def review_permission_request(
        self,
        user_id: str,
        requested_resource: str,
        access_level: str,
        justification: str
    ) -> Dict[str, Any]:
        """
        Review a user's request for additional permissions.
        
        Args:
            user_id: ID of the user requesting permissions
            requested_resource: Resource the user is requesting access to
            access_level: Level of access being requested
            justification: User's justification for the request
            
        Returns:
            Permission review results
        """
        from ..tasks import create_permission_review_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a permission review task
        permission_task = create_permission_review_task(
            agent_name=self.user_manager.name,
            user_id=user_id,
            requested_resource=requested_resource,
            access_level=access_level,
            justification=justification,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(permission_task)
        
        # Run the crew to review the permission request
        return self.run()
    
    def identify_vulnerabilities(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify potential vulnerabilities in the system.
        
        Args:
            system_data: Data about system components and configurations
            
        Returns:
            Vulnerability assessment results
        """
        from ..tasks import create_vulnerability_assessment_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a vulnerability assessment task
        vulnerability_task = create_vulnerability_assessment_task(
            agent_name=self.security_agent.name,
            system_data=system_data,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(vulnerability_task)
        
        # Run the crew to identify vulnerabilities
        return self.run()
    
    def investigate_security_incident(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Investigate a security incident.
        
        Args:
            incident_data: Data about the security incident
            
        Returns:
            Investigation results
        """
        from ..tasks import create_security_incident_investigation_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a security incident investigation task
        investigation_task = create_security_incident_investigation_task(
            agent_name=self.security_agent.name,
            incident_data=incident_data,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(investigation_task)
        
        # Run the crew to investigate the security incident
        return self.run()