"""
Tests for the Control Center module.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.control_center import ControlCenter
from src.schema import SystemStatus, AlertLevel, TaskStatus


class TestControlCenter(unittest.TestCase):
    """Test cases for the Control Center."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'mock-api-key'}):
            self.control_center = ControlCenter({
                'log_level': 'ERROR',
                'enable_autonomous_mode': False,
                'metrics_retention_days': 7,
                'alert_retention_days': 30
            })

    def test_register_component(self):
        """Test registering a component."""
        self.control_center.register_component(
            name="test-component",
            status=SystemStatus.OPERATIONAL,
            description="Test component"
        )

        component = self.control_center.get_component_status("test-component")
        self.assertIsNotNone(component)
        self.assertEqual(component.name, "test-component")
        self.assertEqual(component.status, SystemStatus.OPERATIONAL)
        self.assertEqual(component.description, "Test component")

    def test_update_component_status(self):
        """Test updating a component's status."""
        # Register a component first
        self.control_center.register_component(
            name="test-component",
            status=SystemStatus.OPERATIONAL
        )

        # Update the status
        self.control_center.update_component_status(
            name="test-component",
            status=SystemStatus.DEGRADED,
            details={"reason": "Test issue"}
        )

        # Check the updated status
        component = self.control_center.get_component_status("test-component")
        self.assertEqual(component.status, SystemStatus.DEGRADED)
        self.assertEqual(component.details.get("reason"), "Test issue")

    def test_create_alert(self):
        """Test creating an alert."""
        alert = self.control_center.create_alert(
            level=AlertLevel.WARNING,
            title="Test Alert",
            description="This is a test alert",
            component="test-component",
            details={"key": "value"}
        )

        self.assertIsNotNone(alert)
        self.assertEqual(alert.level, AlertLevel.WARNING)
        self.assertEqual(alert.title, "Test Alert")
        self.assertEqual(alert.description, "This is a test alert")
        self.assertEqual(alert.component, "test-component")
        self.assertEqual(alert.details.get("key"), "value")
        self.assertFalse(alert.resolved)

    def test_resolve_alert(self):
        """Test resolving an alert."""
        # Create an alert first
        alert = self.control_center.create_alert(
            level=AlertLevel.WARNING,
            title="Test Alert",
            description="This is a test alert",
            component="test-component"
        )

        # Resolve the alert
        updated_alert = self.control_center.resolve_alert(
            alert_id=alert.alert_id,
            resolution="The issue has been fixed"
        )

        self.assertIsNotNone(updated_alert)
        self.assertTrue(updated_alert.resolved)
        self.assertEqual(updated_alert.resolution, "The issue has been fixed")
        self.assertIsNotNone(updated_alert.resolved_at)

    def test_get_active_alerts(self):
        """Test getting active alerts."""
        # Create some alerts
        self.control_center.create_alert(
            level=AlertLevel.WARNING,
            title="Warning Alert",
            description="This is a warning",
            component="component-1"
        )
        self.control_center.create_alert(
            level=AlertLevel.CRITICAL,
            title="Critical Alert",
            description="This is critical",
            component="component-2"
        )
        alert3 = self.control_center.create_alert(
            level=AlertLevel.WARNING,
            title="Another Warning",
            description="Another warning",
            component="component-1"
        )

        # Resolve one alert
        self.control_center.resolve_alert(
            alert_id=alert3.alert_id,
            resolution="Fixed"
        )

        # Get all active alerts
        active_alerts = self.control_center.get_active_alerts()
        self.assertEqual(len(active_alerts), 2)

        # Get active alerts for a specific component
        component_alerts = self.control_center.get_active_alerts(component="component-1")
        self.assertEqual(len(component_alerts), 1)
        self.assertEqual(component_alerts[0].title, "Warning Alert")

        # Get active alerts of a specific level
        level_alerts = self.control_center.get_active_alerts(level=AlertLevel.CRITICAL)
        self.assertEqual(len(level_alerts), 1)
        self.assertEqual(level_alerts[0].title, "Critical Alert")

    def test_create_task(self):
        """Test creating a task."""
        task = self.control_center.create_task(
            title="Test Task",
            description="This is a test task",
            assigned_to="test-user",
            priority="high",
            details={"key": "value"}
        )

        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.assigned_to, "test-user")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.details.get("key"), "value")

    def test_update_task_status(self):
        """Test updating a task's status."""
        # Create a task first
        task = self.control_center.create_task(
            title="Test Task",
            description="This is a test task"
        )

        # Update the task status
        updated_task = self.control_center.update_task_status(
            task_id=task.task_id,
            status=TaskStatus.IN_PROGRESS
        )

        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.status, TaskStatus.IN_PROGRESS)

        # Complete the task
        completed_task = self.control_center.update_task_status(
            task_id=task.task_id,
            status=TaskStatus.COMPLETED,
            result={"output": "Task result"}
        )

        self.assertIsNotNone(completed_task)
        self.assertEqual(completed_task.status, TaskStatus.COMPLETED)
        self.assertEqual(completed_task.result.get("output"), "Task result")
        self.assertIsNotNone(completed_task.completed_at)

    def test_get_tasks_by_status(self):
        """Test getting tasks by status."""
        # Create some tasks
        self.control_center.create_task(
            title="Task 1",
            description="Pending task"
        )
        task2 = self.control_center.create_task(
            title="Task 2",
            description="In progress task"
        )
        task3 = self.control_center.create_task(
            title="Task 3",
            description="Completed task"
        )
        task4 = self.control_center.create_task(
            title="Task 4",
            description="Failed task"
        )

        # Update task statuses
        self.control_center.update_task_status(
            task_id=task2.task_id,
            status=TaskStatus.IN_PROGRESS
        )
        self.control_center.update_task_status(
            task_id=task3.task_id,
            status=TaskStatus.COMPLETED,
            result={"output": "Done"}
        )
        self.control_center.update_task_status(
            task_id=task4.task_id,
            status=TaskStatus.FAILED,
            result={"error": "Something went wrong"}
        )

        # Get tasks by status
        pending_tasks = self.control_center.get_tasks_by_status(TaskStatus.PENDING)
        in_progress_tasks = self.control_center.get_tasks_by_status(TaskStatus.IN_PROGRESS)
        completed_tasks = self.control_center.get_tasks_by_status(TaskStatus.COMPLETED)
        failed_tasks = self.control_center.get_tasks_by_status(TaskStatus.FAILED)

        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(in_progress_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(len(failed_tasks), 1)

        self.assertEqual(pending_tasks[0].title, "Task 1")
        self.assertEqual(in_progress_tasks[0].title, "Task 2")
        self.assertEqual(completed_tasks[0].title, "Task 3")
        self.assertEqual(failed_tasks[0].title, "Task 4")

    @patch('src.crews.AdminCrew')
    def test_handle_critical_alert(self, mock_admin_crew):
        """Test handling a critical alert."""
        # Set up mock
        mock_instance = MagicMock()
        mock_instance.handle_system_incident.return_value = {"results": "Alert handled"}
        mock_admin_crew.return_value = mock_instance
        
        # Create control center with autonomous mode enabled
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'mock-api-key'}):
            cc = ControlCenter({
                'enable_autonomous_mode': True
            })
            
        # Create a critical alert
        alert = cc.create_alert(
            level=AlertLevel.CRITICAL,
            title="Critical System Issue",
            description="Something is very wrong",
            component="important-component"
        )
        
        # Verify the admin crew was called
        mock_instance.handle_system_incident.assert_called_once()
        
        # Verify a task was created
        tasks = cc.get_tasks_by_status(TaskStatus.COMPLETED)
        self.assertEqual(len(tasks), 1)
        self.assertTrue("Critical Alert Response" in tasks[0].title)


if __name__ == '__main__':
    unittest.main()