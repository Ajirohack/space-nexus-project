/**
 * rag_system_adapter.js
 *
 * Adapter to connect the RAG (Retrieval-Augmented Generation) system with the Integration Layer
 */

const path = require("path");
const logger = require("../../utils/logger");

class RAGSystemAdapter {
  /**
   * @param {Object} ragSystem - The RAG system instance to adapt
   * @param {Object} options - Configuration options
   */
  constructor(ragSystem, options = {}) {
    this.ragSystem = ragSystem;
    this.options = options;
    this.isInitialized = false;
    this.queryCache = new Map();

    logger.info("RAG System Adapter created");
  }

  /**
   * Initialize the adapter and establish connections
   */
  async initialize() {
    if (this.isInitialized) {
      return;
    }

    try {
      // Subscribe to RAG system events if they exist
      if (this.ragSystem.on) {
        this.ragSystem.on("index-updated", this.handleIndexUpdate.bind(this));
        this.ragSystem.on(
          "query-processed",
          this.handleQueryProcessed.bind(this)
        );
      }

      this.isInitialized = true;
      logger.info("RAG System Adapter initialized");

      return true;
    } catch (error) {
      logger.error(`Failed to initialize RAG System Adapter: ${error.message}`);
      throw error;
    }
  }

  /**
   * Receive data from the Integration Layer and forward to the RAG system
   * @param {string} sourceId - Source component ID
   * @param {Object} data - Data being sent
   * @param {Object} options - Options for handling the data
   */
  receiveData(sourceId, data, options = {}) {
    const { type, payload } = data;

    switch (type) {
      case "query":
        return this.handleQuery(sourceId, payload, options);
      case "update-index":
        return this.handleUpdateIndex(sourceId, payload, options);
      case "status-request":
        return this.handleStatusRequest(sourceId, payload, options);
      default:
        logger.warn(`Unknown data type from ${sourceId}: ${type}`);
        return { success: false, error: "Unknown data type" };
    }
  }

  /**
   * Handle a query request for the RAG system
   * @private
   */
  async handleQuery(sourceId, query, options) {
    logger.info(
      `Query received from ${sourceId}: "${query.text.substring(0, 50)}..."`
    );

    try {
      // Generate a cache key for the query
      const cacheKey = `${query.text}-${JSON.stringify(query.options || {})}`;

      // Check if we have a cached result
      if (this.queryCache.has(cacheKey) && options.useCache !== false) {
        logger.info(`Using cached result for query from ${sourceId}`);
        return this.queryCache.get(cacheKey);
      }

      // Process the query
      const result = await this.ragSystem.query(query.text, query.options);

      // Cache the result
      if (options.useCache !== false) {
        this.queryCache.set(cacheKey, { success: true, data: result });
      }

      return { success: true, data: result };
    } catch (error) {
      logger.error(`Error handling query from ${sourceId}: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Handle an index update request for the RAG system
   * @private
   */
  async handleUpdateIndex(sourceId, updateData, options) {
    logger.info(`Index update received from ${sourceId}`);

    try {
      let result;

      if (updateData.documents) {
        // Add documents to the index
        result = await this.ragSystem.addDocuments(
          updateData.documents,
          updateData.options
        );
      } else if (updateData.documentIds) {
        // Remove documents from the index
        result = await this.ragSystem.removeDocuments(updateData.documentIds);
      } else {
        // Rebuild the index
        result = await this.ragSystem.rebuildIndex(updateData.options);
      }

      // Clear the query cache after an index update
      this.queryCache.clear();

      return { success: true, data: result };
    } catch (error) {
      logger.error(
        `Error handling index update from ${sourceId}: ${error.message}`
      );
      return { success: false, error: error.message };
    }
  }

  /**
   * Handle a status request for the RAG system
   * @private
   */
  async handleStatusRequest(sourceId, request, options) {
    logger.info(`Status request from ${sourceId}`);

    try {
      const status = await this.ragSystem.getStatus();
      return { success: true, data: status };
    } catch (error) {
      logger.error(
        `Error handling status request from ${sourceId}: ${error.message}`
      );
      return { success: false, error: error.message };
    }
  }

  /**
   * Handle index update events from the RAG system
   * @private
   */
  handleIndexUpdate(updateInfo) {
    // Clear the query cache when the index is updated
    this.queryCache.clear();

    // Forward the event if handler is provided
    if (this.options.onIndexUpdated) {
      this.options.onIndexUpdated(updateInfo);
    }
  }

  /**
   * Handle query processed events from the RAG system
   * @private
   */
  handleQueryProcessed(queryInfo) {
    // Forward the event if handler is provided
    if (this.options.onQueryProcessed) {
      this.options.onQueryProcessed(queryInfo);
    }
  }
}

module.exports = RAGSystemAdapter;
