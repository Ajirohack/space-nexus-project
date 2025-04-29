from typing import Dict, List, Any, Optional, Union, Callable
import logging
import uuid
from .schemas import ToolManifest, ToolExecutionRequest, ToolExecutionResponse
from .tool_registry import ToolRegistry
from .tool_executor import ToolExecutor
from .access_control import AccessControl

# Configure logger
logger = logging.getLogger("tools_system")

class ToolsSystem:
    """Main entry point for the Tools/Packages System."""
    
    def __init__(self):
        """Initialize the Tools/Packages system."""
        self.registry = ToolRegistry()
        self.access_control = AccessControl()
        self.executor = ToolExecutor(self.registry, self.access_control)
        self._register_core_tools()
    
    def _register_core_tools(self):
        """Register core tools that are always available."""
        
        # System information tool
        @self.register_tool(
            name="system_info",
            description="Get information about the tools system",
            required_permissions=["basic_tools"]
        )
        def system_info() -> Dict[str, Any]:
            """Get information about the current system configuration."""
            available_tools = len(self.registry.list_tools())
            available_modes = self.access_control.list_modes()
            
            return {
                "available_tools": available_tools,
                "available_modes": available_modes,
                "status": "operational"
            }
        
        # Echo tool for testing
        @self.register_tool(
            name="echo",
            description="Echo back the input",
            required_permissions=["basic_tools"]
        )
        def echo(message: str) -> str:
            """Echo back the input message."""
            return message
    
    def register_tool(self, 
                     name: str, 
                     description: str, 
                     required_permissions: List[str] = None, 
                     version: str = "0.1.0",
                     tags: List[str] = None):
        """Decorator to register a tool function."""
        def decorator(func):
            self.registry.register_from_function(
                func=func,
                name=name,
                description=description,
                version=version,
                required_permissions=required_permissions or [],
                tags=tags or []
            )
            return func
        return decorator
    
    def execute_tool(self, 
                    tool_id: str, 
                    parameters: Dict[str, Any],
                    mode: Optional[str] = None,
                    user_id: Optional[str] = None,
                    request_id: Optional[str] = None) -> ToolExecutionResponse:
        """Execute a tool with the given parameters."""
        # Create the request
        request = ToolExecutionRequest(
            tool_id=tool_id,
            parameters=parameters,
            mode=mode,
            user_id=user_id,
            request_id=request_id or str(uuid.uuid4())
        )
        
        # Log the request
        logger.info(f"Executing tool: {tool_id}, Request ID: {request.request_id}")
        
        # Execute the tool
        return self.executor.execute(request)
    
    def get_available_tools(self, mode: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get available tools, optionally filtered by mode permissions."""
        if not mode:
            # If no mode specified, return all tools
            tools = self.registry.list_tools()
        else:
            # Get permissions for the specified mode
            permissions = self.access_control.get_permissions(mode)
            
            # Get tools filtered by permissions
            tools = self.registry.list_tools(permissions=permissions)
        
        # Convert to simplified dict format for API response
        result = []
        for tool in tools:
            result.append({
                "id": tool.id,
                "name": tool.name,
                "description": tool.description,
                "version": tool.version,
                "parameters": {name: param.dict() for name, param in tool.parameters.items()},
                "required_permissions": tool.required_permissions,
                "tags": tool.tags
            })
        
        return result
    
    def register_external_tool(self, manifest: Dict[str, Any], implementation: Callable) -> str:
        """Register an external tool with the system."""
        # Convert dict to ToolManifest
        tool_manifest = ToolManifest(**manifest)
        
        # Register the tool
        return self.registry.register_tool(tool_manifest, implementation)
    
    def get_modes(self) -> List[Dict[str, Any]]:
        """Get all available access modes."""
        result = []
        
        for mode_name in self.access_control.list_modes():
            mode_details = self.access_control.get_mode_details(mode_name)
            if mode_details:
                result.append(mode_details)
        
        return result