"""
Admin Crew for Control Center.
Handles system administration tasks.
"""
import logging
from typing import Dict, List, Any, Optional
from crewai import Crew, Agent, Task, Process

from ..agents import create_agent

# Logger setup
logger = logging.getLogger("control_center.admin_crew")


class AdminCrew:
    """
    Administrative crew for system management tasks.
    Coordinates system administration, user management, and security agents.
    """
    
    def __init__(
        self,
        api_key: str,
        control_center: Any,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Admin Crew.
        
        Args:
            api_key: API key for the LLM
            control_center: Reference to the Control Center
            config: Additional configuration options
        """
        self.api_key = api_key
        self.control_center = control_center
        self.config = config or {}
        
        # Create the agents for this crew
        self.system_admin = create_agent("system_admin", api_key, config.get("system_admin_config"))
        self.user_manager = create_agent("user_manager", api_key, config.get("user_manager_config"))
        self.security = create_agent("security", api_key, config.get("security_config"))
        
        # Initialize the crew
        self.crew = Crew(
            agents=[self.system_admin, self.user_manager, self.security],
            tasks=[],  # Tasks will be added dynamically
            verbose=config.get("verbose", True),
            process=Process.sequential,  # or Process.hierarchical
            manager_llm_config={
                "model": "gpt-4",  # or config.get("manager_model", "gpt-4")
                "api_key": api_key,
                "temperature": 0.1
            }
        )
        
        logger.info("Admin Crew initialized")
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the crew.
        
        Args:
            task: Task to add
        """
        self.crew.tasks.append(task)
        logger.info(f"Added task to Admin Crew: {task.description[:50]}...")
    
    def run(self) -> Dict[str, Any]:
        """
        Run the admin crew with its current tasks.
        
        Returns:
            Dictionary with task results
        """
        if not self.crew.tasks:
            logger.warning("No tasks assigned to Admin Crew")
            return {"error": "No tasks assigned"}
        
        logger.info(f"Running Admin Crew with {len(self.crew.tasks)} tasks")
        
        try:
            results = self.crew.kickoff()
            logger.info("Admin Crew completed tasks successfully")
            return {"results": results}
        except Exception as e:
            logger.error(f"Error running Admin Crew: {str(e)}")
            return {"error": str(e)}
    
    def reset_tasks(self) -> None:
        """Reset all tasks in the crew."""
        self.crew.tasks = []
        logger.info("Reset all tasks in Admin Crew")
    
    def handle_system_incident(self, incident_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a system incident using the admin crew.
        
        Args:
            incident_details: Details about the incident
            
        Returns:
            Results from the incident response
        """
        from ..tasks import create_incident_response_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create an incident response task assigned to the system admin
        incident_task = create_incident_response_task(
            agent_name=self.system_admin.name,
            incident_details=incident_details,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(incident_task)
        
        # Run the crew to handle the incident
        return self.run()
    
    def perform_system_health_check(self) -> Dict[str, Any]:
        """
        Perform a comprehensive system health check.
        
        Returns:
            Health check results
        """
        from ..tasks import create_system_health_check_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a health check task assigned to the system admin
        health_task = create_system_health_check_task(
            agent_name=self.system_admin.name,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(health_task)
        
        # Run the crew to perform the health check
        return self.run()
    
    def review_user_permissions(self, user_id: str) -> Dict[str, Any]:
        """
        Review a user's permissions.
        
        Args:
            user_id: ID of the user to review
            
        Returns:
            Permission review results
        """
        from ..tasks import create_user_permission_review_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a permission review task assigned to the user manager
        permission_task = create_user_permission_review_task(
            agent_name=self.user_manager.name,
            user_id=user_id,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(permission_task)
        
        # Run the crew to review permissions
        return self.run()
    
    def review_mode_elevation(
        self,
        user_id: str,
        current_mode: str,
        requested_mode: str,
        justification: str
    ) -> Dict[str, Any]:
        """
        Review a user's request for mode elevation.
        
        Args:
            user_id: ID of the user requesting elevation
            current_mode: User's current mode
            requested_mode: Mode the user is requesting
            justification: User's justification for the request
            
        Returns:
            Mode elevation review results
        """
        from ..tasks import create_mode_elevation_review_task
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Create a mode elevation review task assigned to the user manager
        elevation_task = create_mode_elevation_review_task(
            agent_name=self.user_manager.name,
            user_id=user_id,
            current_mode=current_mode,
            requested_mode=requested_mode,
            justification=justification,
            control_center=self.control_center
        )
        
        # Add the task to the crew
        self.add_task(elevation_task)
        
        # Run the crew to review the elevation request
        return self.run()
    
    def check_security_status(self) -> Dict[str, Any]:
        """
        Check the security status of the system.
        
        Returns:
            Security status results
        """
        # Custom task for security assessment
        security_task = Task(
            description=(
                "Perform a comprehensive security assessment of the Space WH system. "
                "Check for unauthorized access attempts, suspicious activities, "
                "potential vulnerabilities, and overall security posture."
            ),
            expected_output=(
                "A detailed security report including current threats, "
                "vulnerabilities, suspicious activities detected, and "
                "specific security recommendations."
            ),
            agent=self.security.name
        )
        
        # Reset previous tasks
        self.reset_tasks()
        
        # Add the security task to the crew
        self.add_task(security_task)
        
        # Run the crew to check security status
        return self.run()