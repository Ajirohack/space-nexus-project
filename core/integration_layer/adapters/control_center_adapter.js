/**
 * control_center_adapter.js
 *
 * Adapter to connect the Control Center with the Integration Layer
 */

const path = require("path");
const logger = require("../../utils/logger");

class ControlCenterAdapter {
  /**
   * @param {Object} controlCenter - The Control Center instance to adapt
   * @param {Object} options - Configuration options
   */
  constructor(controlCenter, options = {}) {
    this.controlCenter = controlCenter;
    this.options = options;
    this.isInitialized = false;

    logger.info("Control Center Adapter created");
  }

  /**
   * Initialize the adapter and establish connections
   */
  async initialize() {
    if (this.isInitialized) {
      return;
    }

    try {
      // Subscribe to Control Center events
      this.controlCenter.on("alert", this.handleAlert.bind(this));
      this.controlCenter.on(
        "status-change",
        this.handleStatusChange.bind(this)
      );
      this.controlCenter.on(
        "task-complete",
        this.handleTaskComplete.bind(this)
      );

      this.isInitialized = true;
      logger.info("Control Center Adapter initialized");
    } catch (error) {
      logger.error(
        `Failed to initialize Control Center Adapter: ${error.message}`
      );
      throw error;
    }
  }

  /**
   * Receive data from the Integration Layer and forward to the Control Center
   * @param {string} sourceId - Source component ID
   * @param {Object} data - Data being sent
   * @param {Object} options - Options for handling the data
   */
  receiveData(sourceId, data, options = {}) {
    const { type, payload } = data;

    switch (type) {
      case "command":
        return this.handleCommand(sourceId, payload, options);
      case "status-request":
        return this.handleStatusRequest(sourceId, payload, options);
      case "task":
        return this.handleTask(sourceId, payload, options);
      default:
        logger.warn(`Unknown data type from ${sourceId}: ${type}`);
        return { success: false, error: "Unknown data type" };
    }
  }

  /**
   * Handle a command sent to the Control Center
   * @private
   */
  handleCommand(sourceId, command, options) {
    logger.info(`Command received from ${sourceId}: ${command.action}`);

    try {
      switch (command.action) {
        case "start-crew":
          return this.controlCenter.startCrew(
            command.crewId,
            command.parameters
          );
        case "stop-crew":
          return this.controlCenter.stopCrew(command.crewId);
        case "register-component":
          return this.controlCenter.registerComponent(
            command.componentId,
            command.metadata
          );
        default:
          logger.warn(`Unknown command action: ${command.action}`);
          return { success: false, error: "Unknown command action" };
      }
    } catch (error) {
      logger.error(`Error handling command from ${sourceId}: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Handle a status request for the Control Center
   * @private
   */
  handleStatusRequest(sourceId, request, options) {
    logger.info(`Status request from ${sourceId}`);

    try {
      const status = {
        components: this.controlCenter.getComponentsStatus(),
        crews: this.controlCenter.getCrewsStatus(),
        tasks: this.controlCenter.getActiveTasks(),
        alerts: this.controlCenter.getActiveAlerts(),
      };

      return { success: true, data: status };
    } catch (error) {
      logger.error(
        `Error handling status request from ${sourceId}: ${error.message}`
      );
      return { success: false, error: error.message };
    }
  }

  /**
   * Handle a task sent to the Control Center
   * @private
   */
  handleTask(sourceId, task, options) {
    logger.info(`Task received from ${sourceId}: ${task.type}`);

    try {
      const taskId = this.controlCenter.createTask(task);
      return { success: true, taskId };
    } catch (error) {
      logger.error(`Error handling task from ${sourceId}: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Handle an alert from the Control Center
   * @private
   */
  handleAlert(alert) {
    // This will be called when the Control Center emits an alert event
    if (this.options.onAlert) {
      this.options.onAlert(alert);
    }
  }

  /**
   * Handle a status change from the Control Center
   * @private
   */
  handleStatusChange(status) {
    // This will be called when the Control Center emits a status change event
    if (this.options.onStatusChange) {
      this.options.onStatusChange(status);
    }
  }

  /**
   * Handle a task completion from the Control Center
   * @private
   */
  handleTaskComplete(task) {
    // This will be called when the Control Center emits a task complete event
    if (this.options.onTaskComplete) {
      this.options.onTaskComplete(task);
    }
  }
}

module.exports = ControlCenterAdapter;
