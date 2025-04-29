"""
Schema definitions for the Control Center.
Defines data structures used throughout the Control Center component.
"""
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SystemStatus(str, Enum):
    """Enumeration of possible system statuses."""
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    DOWN = "down"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class AlertLevel(str, Enum):
    """Enumeration of possible alert levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ComponentStatus(BaseModel):
    """Status information for a system component."""
    name: str
    status: SystemStatus
    description: str = ""
    last_updated: datetime = Field(default_factory=datetime.now)
    details: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class SystemMetrics(BaseModel):
    """System performance metrics."""
    timestamp: datetime = Field(default_factory=datetime.now)
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    response_time_ms: int = 0
    active_users: int = 0
    requests_per_minute: int = 0
    errors_per_minute: int = 0
    component_metrics: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    custom_metrics: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class Alert(BaseModel):
    """System alert information."""
    alert_id: str
    level: AlertLevel
    title: str
    description: str
    component: str
    timestamp: datetime = Field(default_factory=datetime.now)
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class Task(BaseModel):
    """Task information for CrewAI agents."""
    task_id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: str = "medium"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    assigned_to: Optional[str] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    details: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class ControlCenterConfig(BaseModel):
    """Configuration for the Control Center."""
    enable_autonomous_mode: bool = False
    alert_retention_days: int = 30
    crew_config: Dict[str, Any] = Field(default_factory=dict)
    default_model: str = "gpt-4"
    log_level: str = "INFO"
    automated_tasks: Dict[str, bool] = Field(default_factory=dict)
    metrics_retention_days: int = 7
    default_task_priority: str = "medium"
    custom_settings: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True