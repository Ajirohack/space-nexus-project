"""
Control Center for Space WH.
Central coordination system for monitoring and managing the Space WH system.
"""
import os
import uuid
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from .schema import (
    ControlCenterConfig,
    ComponentStatus,
    SystemStatus,
    SystemMetrics,
    Alert,
    AlertLevel,
    Task,
    TaskStatus
)
from .crews import AdminCrew, MonitoringCrew

# Logger setup
logger = logging.getLogger("control_center")


class ControlCenter:
    """
    Control Center for Space WH.
    Coordinates system monitoring, AI agents, and management functions.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Control Center.
        
        Args:
            config: Configuration options for the Control Center
        """
        self.config = ControlCenterConfig(**(config or {}))
        self.components: Dict[str, ComponentStatus] = {}
        self.alerts: List[Alert] = []
        self.metrics_history: List[SystemMetrics] = []
        self.tasks: Dict[str, Task] = {}
        
        # Set up logging based on config
        logging_level = getattr(logging, self.config.log_level, logging.INFO)
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Get API key for LLM access
        self.api_key = os.environ.get(
            "OPENAI_API_KEY",
            config.get("api_key", "") if config else ""
        )
        
        if not self.api_key:
            logger.warning("No API key provided for LLM. CrewAI functionality will be limited.")
        
        # Initialize the crews
        self._init_crews()
        
        logger.info("Control Center initialized")
    
    def _init_crews(self) -> None:
        """Initialize CrewAI crews for different system functions."""
        # Only initialize crews if we have an API key
        if not self.api_key:
            self.admin_crew = None
            self.monitoring_crew = None
            logger.warning("CrewAI crews not initialized due to missing API key")
            return
        
        # Create the admin crew
        self.admin_crew = AdminCrew(
            api_key=self.api_key,
            control_center=self,
            config=self.config.crew_config.get("admin_crew", {})
        )
        
        # Create the monitoring crew
        self.monitoring_crew = MonitoringCrew(
            api_key=self.api_key,
            control_center=self,
            config=self.config.crew_config.get("monitoring_crew", {})
        )
        
        logger.info("CrewAI crews initialized")
    
    def register_component(self, name: str, status: SystemStatus = SystemStatus.UNKNOWN, description: str = "") -> None:
        """
        Register a system component with the Control Center.
        
        Args:
            name: Component name
            status: Initial component status
            description: Component description
        """
        self.components[name] = ComponentStatus(
            name=name,
            status=status,
            description=description,
            last_updated=datetime.now()
        )
        logger.info(f"Registered component: {name} with status {status}")
    
    def update_component_status(self, name: str, status: SystemStatus, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Update the status of a registered component.
        
        Args:
            name: Component name
            status: New component status
            details: Additional status details
        """
        if name not in self.components:
            logger.warning(f"Attempted to update unregistered component: {name}")
            self.register_component(name, status)
            
        self.components[name].status = status
        self.components[name].last_updated = datetime.now()
        
        if details:
            self.components[name].details.update(details)
        
        logger.info(f"Updated component status: {name} -> {status}")
    
    def get_component_status(self, name: str) -> Optional[ComponentStatus]:
        """
        Get the status of a component.
        
        Args:
            name: Component name
            
        Returns:
            ComponentStatus if found, None otherwise
        """
        return self.components.get(name)
    
    def get_all_component_statuses(self) -> Dict[str, ComponentStatus]:
        """
        Get status information for all registered components.
        
        Returns:
            Dictionary of component statuses
        """
        return self.components
    
    def create_alert(
        self,
        level: AlertLevel,
        title: str,
        description: str,
        component: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Alert:
        """
        Create a new system alert.
        
        Args:
            level: Alert severity level
            title: Alert title
            description: Alert description
            component: Affected component
            details: Additional alert details
            
        Returns:
            The created Alert
        """
        alert_id = str(uuid.uuid4())
        alert = Alert(
            alert_id=alert_id,
            level=level,
            title=title,
            description=description,
            component=component,
            timestamp=datetime.now(),
            details=details or {}
        )
        
        self.alerts.append(alert)
        logger.info(f"Created alert: {alert_id} - {title} ({level})")
        
        # Auto-handle critical alerts if autonomous mode is enabled
        if level == AlertLevel.CRITICAL and self.config.enable_autonomous_mode:
            self._handle_critical_alert(alert)
        
        return alert
    
    def resolve_alert(self, alert_id: str, resolution: str) -> Optional[Alert]:
        """
        Mark an alert as resolved.
        
        Args:
            alert_id: ID of the alert to resolve
            resolution: Description of how the alert was resolved
            
        Returns:
            The updated Alert if found, None otherwise
        """
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                alert.resolution = resolution
                logger.info(f"Resolved alert: {alert_id}")
                return alert
        
        logger.warning(f"Attempted to resolve unknown or already resolved alert: {alert_id}")
        return None
    
    def get_active_alerts(self, component: Optional[str] = None, level: Optional[AlertLevel] = None) -> List[Alert]:
        """
        Get all active (unresolved) alerts.
        
        Args:
            component: Filter by component
            level: Filter by alert level
            
        Returns:
            List of active alerts matching the filters
        """
        active_alerts = [alert for alert in self.alerts if not alert.resolved]
        
        if component:
            active_alerts = [alert for alert in active_alerts if alert.component == component]
        
        if level:
            active_alerts = [alert for alert in active_alerts if alert.level == level]
        
        return active_alerts
    
    def record_metrics(self, metrics: SystemMetrics) -> None:
        """
        Record system performance metrics.
        
        Args:
            metrics: System metrics to record
        """
        self.metrics_history.append(metrics)
        
        # Cleanup old metrics based on retention policy
        self._cleanup_old_metrics()
        
        logger.debug("Recorded system metrics")
    
    def _cleanup_old_metrics(self) -> None:
        """Clean up metrics older than the configured retention period."""
        if not self.config.metrics_retention_days:
            return
            
        cutoff_date = datetime.now() - timedelta(days=self.config.metrics_retention_days)
        self.metrics_history = [m for m in self.metrics_history if m.timestamp > cutoff_date]
    
    def _cleanup_old_alerts(self) -> None:
        """Clean up alerts older than the configured retention period."""
        if not self.config.alert_retention_days:
            return
            
        cutoff_date = datetime.now() - timedelta(days=self.config.alert_retention_days)
        self.alerts = [
            a for a in self.alerts 
            if (a.resolved and a.resolved_at and a.resolved_at > cutoff_date) or 
               (not a.resolved and a.timestamp > cutoff_date)
        ]
    
    def get_recent_metrics(self, hours: int = 24) -> List[SystemMetrics]:
        """
        Get metrics from the recent past.
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of metrics from the specified period
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [m for m in self.metrics_history if m.timestamp > cutoff_time]
    
    def create_task(
        self,
        title: str,
        description: str,
        assigned_to: Optional[str] = None,
        priority: str = "medium",
        details: Optional[Dict[str, Any]] = None
    ) -> Task:
        """
        Create a new task.
        
        Args:
            title: Task title
            description: Task description
            assigned_to: Agent or entity assigned to the task
            priority: Task priority
            details: Additional task details
            
        Returns:
            The created Task
        """
        task_id = str(uuid.uuid4())
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            assigned_to=assigned_to,
            details=details or {}
        )
        
        self.tasks[task_id] = task
        logger.info(f"Created task: {task_id} - {title}")
        
        return task
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[Any] = None
    ) -> Optional[Task]:
        """
        Update the status of a task.
        
        Args:
            task_id: ID of the task to update
            status: New task status
            result: Task result (if completed)
            
        Returns:
            The updated Task if found, None otherwise
        """
        if task_id not in self.tasks:
            logger.warning(f"Attempted to update unknown task: {task_id}")
            return None
            
        task = self.tasks[task_id]
        task.status = status
        task.updated_at = datetime.now()
        
        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now()
            task.result = result
        
        logger.info(f"Updated task status: {task_id} -> {status}")
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task if found, None otherwise
        """
        return self.tasks.get(task_id)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """
        Get all tasks with a specific status.
        
        Args:
            status: Task status to filter by
            
        Returns:
            List of matching tasks
        """
        return [task for task in self.tasks.values() if task.status == status]
    
    def _handle_critical_alert(self, alert: Alert) -> None:
        """
        Handle a critical alert automatically.
        
        Args:
            alert: The critical alert to handle
        """
        if not self.admin_crew:
            logger.warning("Cannot auto-handle critical alert: Admin crew not initialized")
            return
            
        logger.info(f"Auto-handling critical alert: {alert.alert_id}")
        
        # Create incident details from the alert
        incident_details = {
            "title": alert.title,
            "component": alert.component,
            "description": alert.description,
            "alert_id": alert.alert_id,
            "details": alert.details
        }
        
        # Create a task to track this response
        task = self.create_task(
            title=f"Critical Alert Response: {alert.title}",
            description=f"Automatically respond to critical alert in component {alert.component}",
            assigned_to="AdminCrew",
            priority="high",
            details={"alert_id": alert.alert_id}
        )
        
        try:
            # Have the admin crew handle the incident
            response = self.admin_crew.handle_system_incident(incident_details)
            
            # Update the task with the results
            if "error" not in response:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.COMPLETED,
                    result=response.get("results")
                )
            else:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.FAILED,
                    result={"error": response.get("error")}
                )
        except Exception as e:
            logger.error(f"Error handling critical alert: {str(e)}")
            self.update_task_status(
                task.task_id,
                TaskStatus.FAILED,
                result={"error": str(e)}
            )
    
    def perform_system_health_check(self) -> Dict[str, Any]:
        """
        Perform a comprehensive system health check.
        
        Returns:
            Health check results
        """
        if not self.admin_crew:
            logger.warning("Cannot perform health check: Admin crew not initialized")
            return {"error": "Admin crew not initialized"}
        
        # Create a task to track this health check
        task = self.create_task(
            title="System Health Check",
            description="Comprehensive check of all system components",
            assigned_to="AdminCrew",
            priority="medium"
        )
        
        try:
            # Have the admin crew perform the health check
            response = self.admin_crew.perform_system_health_check()
            
            # Update the task with the results
            if "error" not in response:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.COMPLETED,
                    result=response.get("results")
                )
                return {"success": True, "results": response.get("results"), "task_id": task.task_id}
            else:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.FAILED,
                    result={"error": response.get("error")}
                )
                return {"error": response.get("error"), "task_id": task.task_id}
        except Exception as e:
            logger.error(f"Error performing health check: {str(e)}")
            self.update_task_status(
                task.task_id,
                TaskStatus.FAILED,
                result={"error": str(e)}
            )
            return {"error": str(e), "task_id": task.task_id}
    
    def analyze_ai_behavior(self, behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze AI behavior patterns.
        
        Args:
            behavior_data: Data about AI behavior to analyze
            
        Returns:
            Behavior analysis results
        """
        if not self.monitoring_crew:
            logger.warning("Cannot analyze AI behavior: Monitoring crew not initialized")
            return {"error": "Monitoring crew not initialized"}
        
        # Create a task to track this analysis
        task = self.create_task(
            title="AI Behavior Analysis",
            description="Analysis of AI agent behavior patterns",
            assigned_to="MonitoringCrew",
            priority="medium",
            details={"data_summary": f"Analyzing {len(behavior_data)} behavior records"}
        )
        
        try:
            # Have the monitoring crew analyze the behavior data
            response = self.monitoring_crew.analyze_ai_behavior(behavior_data)
            
            # Update the task with the results
            if "error" not in response:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.COMPLETED,
                    result=response.get("results")
                )
                return {"success": True, "results": response.get("results"), "task_id": task.task_id}
            else:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.FAILED,
                    result={"error": response.get("error")}
                )
                return {"error": response.get("error"), "task_id": task.task_id}
        except Exception as e:
            logger.error(f"Error analyzing AI behavior: {str(e)}")
            self.update_task_status(
                task.task_id,
                TaskStatus.FAILED,
                result={"error": str(e)}
            )
            return {"error": str(e), "task_id": task.task_id}
    
    def optimize_operation_mode(self, mode: str, usage_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize a specific operation mode.
        
        Args:
            mode: The mode to optimize (archivist, orchestrator, godfather, entity)
            usage_data: Data about mode usage patterns
            
        Returns:
            Mode optimization results
        """
        if not self.monitoring_crew:
            logger.warning("Cannot optimize operation mode: Monitoring crew not initialized")
            return {"error": "Monitoring crew not initialized"}
        
        # Create a task to track this optimization
        task = self.create_task(
            title=f"Optimize '{mode}' Operation Mode",
            description=f"Optimize the configuration and behavior of the '{mode}' operation mode",
            assigned_to="MonitoringCrew",
            priority="high",
            details={"mode": mode, "data_points": len(usage_data) if isinstance(usage_data, list) else "N/A"}
        )
        
        try:
            # Have the monitoring crew optimize the operation mode
            response = self.monitoring_crew.optimize_operation_mode(mode, usage_data)
            
            # Update the task with the results
            if "error" not in response:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.COMPLETED,
                    result=response.get("results")
                )
                return {"success": True, "results": response.get("results"), "task_id": task.task_id}
            else:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.FAILED,
                    result={"error": response.get("error")}
                )
                return {"error": response.get("error"), "task_id": task.task_id}
        except Exception as e:
            logger.error(f"Error optimizing operation mode: {str(e)}")
            self.update_task_status(
                task.task_id,
                TaskStatus.FAILED,
                result={"error": str(e)}
            )
            return {"error": str(e), "task_id": task.task_id}
    
    def review_mode_elevation_request(
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
        if not self.admin_crew:
            logger.warning("Cannot review mode elevation: Admin crew not initialized")
            return {"error": "Admin crew not initialized"}
        
        # Create a task to track this review
        task = self.create_task(
            title=f"Mode Elevation Request: {current_mode} → {requested_mode}",
            description=f"Review mode elevation request from user {user_id}",
            assigned_to="AdminCrew",
            priority="high",
            details={
                "user_id": user_id,
                "current_mode": current_mode,
                "requested_mode": requested_mode
            }
        )
        
        try:
            # Have the admin crew review the mode elevation request
            response = self.admin_crew.review_mode_elevation(
                user_id=user_id,
                current_mode=current_mode,
                requested_mode=requested_mode,
                justification=justification
            )
            
            # Update the task with the results
            if "error" not in response:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.COMPLETED,
                    result=response.get("results")
                )
                return {"success": True, "results": response.get("results"), "task_id": task.task_id}
            else:
                self.update_task_status(
                    task.task_id,
                    TaskStatus.FAILED,
                    result={"error": response.get("error")}
                )
                return {"error": response.get("error"), "task_id": task.task_id}
        except Exception as e:
            logger.error(f"Error reviewing mode elevation request: {str(e)}")
            self.update_task_status(
                task.task_id,
                TaskStatus.FAILED,
                result={"error": str(e)}
            )
            return {"error": str(e), "task_id": task.task_id}