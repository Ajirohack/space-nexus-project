/**
 * tools_adapter.js
 *
 * Adapter to connect the Tools & Packages system with the Integration Layer.
 * This adapter handles the discovery, registration, and invocation of tools
 * according to the current operational mode and permissions.
 */

const logger = require("../../../utils/logger");
const { OperationalModes } = require("../../../utils/mode-permissions");
const { IntegrationError } = require("../../../utils/errors");

class ToolsAdapter {
  /**
   * @param {Object} integrationLayer - Reference to the parent integration layer
   */
  constructor(integrationLayer) {
    this.integrationLayer = integrationLayer;
    this.isConnected = false;
    this.registeredTools = new Map();
    this.toolsCache = new Map();
    this.modePermissions = new Map();

    // Configure default mode permissions
    this.configureModePermissions();

    logger.info("Tools Adapter created");
  }

  /**
   * Connect to the Tools & Packages system
   */
  async connect() {
    if (this.isConnected) {
      return true;
    }

    try {
      logger.info("Connecting to Tools & Packages system...");

      // Initialize the tools registry
      await this.discoverTools();

      // Subscribe to relevant events from the integration layer
      this.integrationLayer.on(
        "tool-requested",
        this.handleToolRequest.bind(this)
      );

      this.isConnected = true;
      logger.info("Successfully connected to Tools & Packages system");
      return true;
    } catch (error) {
      logger.error(
        `Failed to connect to Tools & Packages system: ${error.message}`
      );
      throw new IntegrationError("Tools connection failed", error);
    }
  }

  /**
   * Disconnect from the Tools & Packages system
   */
  async disconnect() {
    if (!this.isConnected) {
      return true;
    }

    try {
      logger.info("Disconnecting from Tools & Packages system...");

      // Clean up tool resources
      for (const tool of this.registeredTools.values()) {
        if (tool.cleanup && typeof tool.cleanup === "function") {
          await tool.cleanup();
        }
      }

      this.registeredTools.clear();
      this.toolsCache.clear();

      this.isConnected = false;
      logger.info("Successfully disconnected from Tools & Packages system");
      return true;
    } catch (error) {
      logger.error(
        `Error disconnecting from Tools & Packages system: ${error.message}`
      );
      throw new IntegrationError("Tools disconnection failed", error);
    }
  }

  /**
   * Configure permissions for different operational modes
   * @private
   */
  configureModePermissions() {
    // STANDARD mode - Regular tools
    this.modePermissions.set(OperationalModes.STANDARD, [
      "utility",
      "information",
      "communication",
      "basic-ai",
    ]);

    // ENHANCED mode - Advanced tools
    this.modePermissions.set(OperationalModes.ENHANCED, [
      "utility",
      "information",
      "communication",
      "basic-ai",
      "advanced-ai",
      "system-access",
      "data-analysis",
    ]);

    // EXPERIMENTAL mode - All tools including experimental
    this.modePermissions.set(OperationalModes.EXPERIMENTAL, [
      "utility",
      "information",
      "communication",
      "basic-ai",
      "advanced-ai",
      "system-access",
      "data-analysis",
      "experimental",
      "administrator",
    ]);

    // MAINTENANCE mode - System and diagnostic tools
    this.modePermissions.set(OperationalModes.MAINTENANCE, [
      "utility",
      "system-access",
      "diagnostics",
      "administrator",
    ]);
  }

  /**
   * Discover and register available tools
   * @private
   */
  async discoverTools() {
    try {
      logger.info("Discovering available tools...");

      // Here we would typically scan the tools directory or query a registry
      // For now, we'll implement a simple discovery mechanism

      // Example tools that would be discovered
      const exampleTools = [
        {
          id: "file-manager",
          name: "File Manager",
          description: "Manages files and directories",
          category: "utility",
          invoke: (params) => {
            /* Tool implementation */
          },
          permissions: ["read", "write"],
        },
        {
          id: "data-analyzer",
          name: "Data Analyzer",
          description: "Analyzes data sets and generates insights",
          category: "data-analysis",
          invoke: (params) => {
            /* Tool implementation */
          },
          permissions: ["read"],
        },
        {
          id: "system-monitor",
          name: "System Monitor",
          description: "Monitors system resources and performance",
          category: "system-access",
          invoke: (params) => {
            /* Tool implementation */
          },
          permissions: ["read"],
        },
      ];

      // Register the discovered tools
      exampleTools.forEach((tool) => {
        this.registeredTools.set(tool.id, tool);
        logger.debug(`Registered tool: ${tool.id} (${tool.category})`);
      });

      logger.info(
        `Discovered and registered ${this.registeredTools.size} tools`
      );
    } catch (error) {
      logger.error(`Error discovering tools: ${error.message}`);
      throw error;
    }
  }

  /**
   * Handle a request to access or execute a tool
   * @private
   */
  async handleToolRequest(request) {
    const { toolId, params, requester, context } = request;

    try {
      // Check if the tool exists
      if (!this.registeredTools.has(toolId)) {
        throw new Error(`Tool not found: ${toolId}`);
      }

      const tool = this.registeredTools.get(toolId);

      // Check if the tool is allowed in the current operational mode
      const currentMode = this.integrationLayer.currentMode;
      const allowedCategories = this.modePermissions.get(currentMode) || [];

      if (!allowedCategories.includes(tool.category)) {
        throw new Error(`Tool '${toolId}' not allowed in ${currentMode} mode`);
      }

      // Execute the tool
      logger.info(`Executing tool: ${toolId} (requested by: ${requester})`);
      const result = await tool.invoke(params);

      return {
        success: true,
        data: result,
      };
    } catch (error) {
      logger.error(`Tool execution error: ${error.message}`);
      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * Handle a mode change event from the integration layer
   */
  handleModeChange(mode) {
    logger.info(`Tools Adapter: Mode changed to ${mode}`);

    // Update available tools based on the new mode
    const availableTools = [];
    const allowedCategories = this.modePermissions.get(mode) || [];

    for (const [id, tool] of this.registeredTools) {
      if (allowedCategories.includes(tool.category)) {
        availableTools.push({
          id: tool.id,
          name: tool.name,
          description: tool.description,
          category: tool.category,
        });
      }
    }

    // Update the system state with the new available tools
    this.integrationLayer.updateSystemState({
      availableTools: availableTools,
    });

    logger.info(
      `Tools Adapter: ${availableTools.length} tools available in ${mode} mode`
    );
  }

  /**
   * Handle a request from the Integration Layer
   */
  async handleRequest(request) {
    const { action, payload } = request;

    switch (action) {
      case "get-tools":
        return this.getTools(payload);
      case "execute-tool":
        return this.executeTool(payload);
      case "register-tool":
        return this.registerTool(payload);
      default:
        logger.warn(`Unknown action: ${action}`);
        return {
          success: false,
          error: `Unknown action: ${action}`,
        };
    }
  }

  /**
   * Get available tools based on filters
   */
  getTools({ category, permissions } = {}) {
    try {
      const tools = [];
      const currentMode = this.integrationLayer.currentMode;
      const allowedCategories = this.modePermissions.get(currentMode) || [];

      for (const [id, tool] of this.registeredTools) {
        // Skip if not allowed in current mode
        if (!allowedCategories.includes(tool.category)) {
          continue;
        }

        // Filter by category if provided
        if (category && tool.category !== category) {
          continue;
        }

        // Filter by permissions if provided
        if (
          permissions &&
          !permissions.every((p) => tool.permissions.includes(p))
        ) {
          continue;
        }

        tools.push({
          id: tool.id,
          name: tool.name,
          description: tool.description,
          category: tool.category,
        });
      }

      return {
        success: true,
        data: tools,
      };
    } catch (error) {
      logger.error(`Error getting tools: ${error.message}`);
      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * Execute a specific tool with parameters
   */
  async executeTool({ toolId, params, requester, context }) {
    // Use the existing handleToolRequest method
    return this.handleToolRequest({ toolId, params, requester, context });
  }

  /**
   * Register a new custom tool
   */
  registerTool({ tool, requester }) {
    try {
      // Validate the tool definition
      if (!tool.id || !tool.name || !tool.category || !tool.invoke) {
        throw new Error("Invalid tool definition");
      }

      // Check if a tool with this ID already exists
      if (this.registeredTools.has(tool.id)) {
        throw new Error(`Tool with ID ${tool.id} already exists`);
      }

      // Register the tool
      this.registeredTools.set(tool.id, tool);

      logger.info(`Tool registered: ${tool.id} by ${requester}`);
      return {
        success: true,
        data: {
          id: tool.id,
          name: tool.name,
        },
      };
    } catch (error) {
      logger.error(`Error registering tool: ${error.message}`);
      return {
        success: false,
        error: error.message,
      };
    }
  }
}

module.exports = ToolsAdapter;
