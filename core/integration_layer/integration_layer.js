/**
 * Integration Layer - Central Hub
 *
 * This module serves as the central integration point for all Space-WH system components:
 * - Control Center with its AI crews
 * - RAG system
 * - System engines
 * - Tools and packages
 * - External interfaces (API Gateway, Frontend)
 *
 * The Integration Layer provides a unified communication interface between components,
 * handles event propagation, manages state transitions, and enforces security policies.
 */

const logger = require("../../utils/logger");
const { OperationalModes } = require("../../utils/mode-permissions");
const { SpaceWHError, IntegrationError } = require("../../utils/errors");

// Import adapters for each major component
const ControlCenterAdapter = require("./adapters/control_center_adapter");
const RAGSystemAdapter = require("./adapters/rag_system_adapter");
const EngineAdapter = require("./adapters/engine_adapter");
const ToolsAdapter = require("./adapters/tools_adapter");
const AICouncilAdapter = require("./adapters/ai_council_adapter");
const APIGatewayAdapter = require("./adapters/api_gateway_adapter");

class IntegrationLayer {
  constructor(config = {}) {
    this.config = config;
    this.currentMode = OperationalModes.STANDARD;

    // Initialize all component adapters
    this.controlCenter = new ControlCenterAdapter(this);
    this.ragSystem = new RAGSystemAdapter(this);
    this.engines = new EngineAdapter(this);
    this.tools = new ToolsAdapter(this);
    this.aiCouncil = new AICouncilAdapter(this);
    this.apiGateway = new APIGatewayAdapter(this);

    this.eventBus = new Map(); // Simple event bus implementation
    this.systemState = {}; // Global system state

    logger.info("Integration Layer initialized successfully");
  }

  /**
   * Start the Integration Layer and connect all components
   */
  async start() {
    try {
      logger.info("Starting Integration Layer...");

      // Connect all components in the correct order based on dependencies
      await this.controlCenter.connect();
      await this.ragSystem.connect();
      await this.engines.connect();
      await this.tools.connect();
      await this.aiCouncil.connect();
      await this.apiGateway.connect();

      logger.info("Integration Layer started successfully");
      return true;
    } catch (error) {
      logger.error(`Failed to start Integration Layer: ${error.message}`);
      throw new IntegrationError("Integration Layer startup failed", error);
    }
  }

  /**
   * Stop the Integration Layer and disconnect all components
   */
  async stop() {
    try {
      logger.info("Stopping Integration Layer...");

      // Disconnect components in reverse order
      await this.apiGateway.disconnect();
      await this.aiCouncil.disconnect();
      await this.tools.disconnect();
      await this.engines.disconnect();
      await this.ragSystem.disconnect();
      await this.controlCenter.disconnect();

      logger.info("Integration Layer stopped successfully");
      return true;
    } catch (error) {
      logger.error(`Error stopping Integration Layer: ${error.message}`);
      throw new IntegrationError("Integration Layer shutdown failed", error);
    }
  }

  /**
   * Register an event handler
   */
  on(eventName, handler) {
    if (!this.eventBus.has(eventName)) {
      this.eventBus.set(eventName, []);
    }
    this.eventBus.get(eventName).push(handler);
  }

  /**
   * Emit an event to all registered handlers
   */
  emit(eventName, data) {
    logger.debug(`Event emitted: ${eventName}`);
    if (this.eventBus.has(eventName)) {
      for (const handler of this.eventBus.get(eventName)) {
        try {
          handler(data);
        } catch (error) {
          logger.error(
            `Error in event handler for ${eventName}: ${error.message}`
          );
        }
      }
    }
  }

  /**
   * Change the system's operational mode
   */
  setOperationalMode(mode) {
    if (!Object.values(OperationalModes).includes(mode)) {
      throw new IntegrationError(`Invalid operational mode: ${mode}`);
    }

    this.currentMode = mode;
    logger.info(`Operational mode changed to: ${mode}`);
    this.emit("mode-change", { mode });

    // Propagate mode change to all components
    this.controlCenter.handleModeChange(mode);
    this.engines.handleModeChange(mode);
    this.ragSystem.handleModeChange(mode);
    this.tools.handleModeChange(mode);
    this.aiCouncil.handleModeChange(mode);
  }

  /**
   * Process a system-wide request
   */
  async processRequest(request) {
    try {
      logger.debug(`Processing request: ${request.type}`);

      // Route the request to the appropriate component
      switch (request.target) {
        case "control-center":
          return await this.controlCenter.handleRequest(request);
        case "rag-system":
          return await this.ragSystem.handleRequest(request);
        case "engines":
          return await this.engines.handleRequest(request);
        case "tools":
          return await this.tools.handleRequest(request);
        case "ai-council":
          return await this.aiCouncil.handleRequest(request);
        default:
          throw new IntegrationError(
            `Unknown request target: ${request.target}`
          );
      }
    } catch (error) {
      logger.error(`Error processing request: ${error.message}`);
      throw new IntegrationError("Request processing failed", error);
    }
  }

  /**
   * Update the global system state
   */
  updateSystemState(partialState) {
    this.systemState = { ...this.systemState, ...partialState };
    this.emit("state-change", { state: this.systemState });
  }

  /**
   * Get the current system state
   */
  getSystemState() {
    return { ...this.systemState };
  }
}

module.exports = IntegrationLayer;
