/**
 * engine_adapter.js
 * 
 * Adapter to connect the Engine system with the Integration Layer
 */

const path = require('path');
const logger = require('../../utils/logger');

class EngineAdapter {
    /**
     * @param {Object} integrationLayer - Reference to the parent integration layer
     * @param {Object} options - Configuration options
     */
    constructor(integrationLayer, options = {}) {
        this.integrationLayer = integrationLayer;
        this.options = options;
        this.engineControl = null; // Will be set in connect()
        this.isInitialized = false;
        this.activeRequests = new Map();
        this.requestCounter = 0;
        this.currentMode = integrationLayer.currentMode || 'STANDARD';
        logger.info('Engine Adapter created');
    }

    /**
     * Connect the adapter to the Engine Control system
     * @param {Object} engineControl - The Engine Control instance to adapt
     */
    async connect(engineControl) {
        if (this.isInitialized) return;
        this.engineControl = engineControl;
        try {
            if (this.engineControl.on) {
                this.engineControl.on('request-complete', this.handleRequestComplete.bind(this));
                this.engineControl.on('engine-status-change', this.handleEngineStatusChange.bind(this));
            }
            this.isInitialized = true;
            logger.info('Engine Adapter initialized');
            return true;
        } catch (error) {
            logger.error(`Failed to initialize Engine Adapter: ${error.message}`);
            this.integrationLayer.emit('engine-error', { error: error.message });
            throw error;
        }
    }

    /**
     * Handle mode change event from Integration Layer
     */
    handleModeChange(mode) {
        this.currentMode = mode;
        logger.info(`Engine Adapter: Mode changed to ${mode}`);
        // Optionally, update engine routing/logic based on mode
        // Emit event for observability
        this.integrationLayer.emit('engine-mode-change', { mode });
    }

    /**
     * Receive and process requests from the Integration Layer
     */
    async handleRequest(request) {
        const { action, payload, sourceId, options = {} } = request;
        switch (action) {
            case 'process-request':
                return this.handleProcessRequest(sourceId, payload, options);
            case 'cancel-request':
                return this.handleCancelRequest(sourceId, payload, options);
            case 'status-request':
                return this.handleStatusRequest(sourceId, payload, options);
            default:
                logger.warn(`Unknown engine action: ${action}`);
                return { success: false, error: 'Unknown engine action' };
        }
    }

    /**
     * Handle a process request for the Engine system
     * @private
     */
    async handleProcessRequest(sourceId, request, options) {
        const requestId = `req-${++this.requestCounter}-${Date.now()}`;
        logger.info(`Process request received from ${sourceId} (ID: ${requestId})`);
        try {
            this.activeRequests.set(requestId, {
                sourceId,
                startTime: Date.now(),
                status: 'processing',
                request
            });
            const tier = this.determineEngineTier(request);
            const processingPromise = this.engineControl.processRequest(tier, request.data, request.options);
            processingPromise.then(result => {
                const requestInfo = this.activeRequests.get(requestId);
                if (requestInfo) {
                    requestInfo.status = 'completed';
                    requestInfo.completionTime = Date.now();
                    requestInfo.result = result;
                    if (options.onComplete) {
                        options.onComplete(requestId, result);
                    }
                    // Emit event to Integration Layer
                    this.integrationLayer.emit('engine-request-complete', { requestId, result, sourceId });
                }
                setTimeout(() => {
                    this.activeRequests.delete(requestId);
                }, 30 * 60 * 1000); // Keep for 30 minutes
            }).catch(error => {
                const requestInfo = this.activeRequests.get(requestId);
                if (requestInfo) {
                    requestInfo.status = 'error';
                    requestInfo.completionTime = Date.now();
                    requestInfo.error = error.message;
                }
                logger.error(`Error processing request ${requestId}: ${error.message}`);
                this.integrationLayer.emit('engine-request-error', { requestId, error: error.message, sourceId });
            });
            return { success: true, requestId };
        } catch (error) {
            logger.error(`Error handling process request from ${sourceId}: ${error.message}`);
            this.integrationLayer.emit('engine-request-error', { error: error.message, sourceId });
            return { success: false, error: error.message };
        }
    }

    /**
     * Handle a cancel request for the Engine system
     * @private
     */
    async handleCancelRequest(sourceId, cancelRequest, options) {
        const { requestId } = cancelRequest;
        logger.info(`Cancel request received from ${sourceId} for request ${requestId}`);
        try {
            const requestInfo = this.activeRequests.get(requestId);
            if (!requestInfo) {
                return { success: false, error: 'Request not found' };
            }
            if (requestInfo.sourceId !== sourceId && !options.adminOverride) {
                return { success: false, error: 'Not authorized to cancel this request' };
            }
            const result = await this.engineControl.cancelRequest(requestId);
            if (result.success) {
                requestInfo.status = 'cancelled';
                requestInfo.cancellationTime = Date.now();
                this.integrationLayer.emit('engine-request-cancelled', { requestId, sourceId });
            }
            return result;
        } catch (error) {
            logger.error(`Error handling cancel request from ${sourceId}: ${error.message}`);
            this.integrationLayer.emit('engine-request-error', { error: error.message, sourceId });
            return { success: false, error: error.message };
        }
    }

    /**
     * Handle a status request for the Engine system
     * @private
     */
    async handleStatusRequest(sourceId, statusRequest, options) {
        logger.info(`Status request received from ${sourceId}`);
        try {
            let status;
            if (statusRequest.requestId) {
                const requestInfo = this.activeRequests.get(statusRequest.requestId);
                if (!requestInfo) {
                    return { success: false, error: 'Request not found' };
                }
                status = {
                    requestId: statusRequest.requestId,
                    status: requestInfo.status,
                    startTime: requestInfo.startTime,
                    completionTime: requestInfo.completionTime,
                    result: requestInfo.status === 'completed' ? requestInfo.result : undefined,
                    error: requestInfo.error
                };
            } else {
                status = await this.engineControl.getStatus();
                status.activeRequests = Array.from(this.activeRequests.values())
                    .filter(req => req.status === 'processing')
                    .length;
            }
            return { success: true, data: status };
        } catch (error) {
            logger.error(`Error handling status request from ${sourceId}: ${error.message}`);
            this.integrationLayer.emit('engine-request-error', { error: error.message, sourceId });
            return { success: false, error: error.message };
        }
    }

    /**
     * Determine which engine tier to use for a request
     * @private
     */
    determineEngineTier(request) {
        if (request.tier) return request.tier;
        const { complexity, urgency, context } = request;
        if (complexity === 'high' || (context && context.length > 10000)) {
            return 'tier3'; // Most powerful
        } else if (complexity === 'medium' || urgency === 'high') {
            return 'tier2'; // Middle tier
        } else {
            return 'tier1'; // Basic tier
        }
    }

    /**
     * Handle request complete events from the Engine system
     * @private
     */
    handleRequestComplete(requestId, result) {
        const requestInfo = this.activeRequests.get(requestId);
        if (requestInfo) {
            requestInfo.status = 'completed';
            requestInfo.completionTime = Date.now();
            requestInfo.result = result;
            if (this.options.onRequestComplete) {
                this.options.onRequestComplete(requestId, result, requestInfo.sourceId);
            }
            // Emit event to Integration Layer
            this.integrationLayer.emit('engine-request-complete', { requestId, result, sourceId: requestInfo.sourceId });
        }
    }

    /**
     * Handle engine status change events from the Engine system
     * @private
     */
    handleEngineStatusChange(engineId, status) {
        if (this.options.onEngineStatusChange) {
            this.options.onEngineStatusChange(engineId, status);
        }
        // Emit event to Integration Layer
        this.integrationLayer.emit('engine-status-change', { engineId, status });
    }
}

module.exports = EngineAdapter;