/**
 * Environment Configuration
 *
 * Loads and manages environment variables for the Space-WH system
 */

require("dotenv").config();

// Define environment constants
const NODE_ENV = process.env.NODE_ENV || "development";
const isProd = NODE_ENV === "production";
const isDev = NODE_ENV === "development";
const isTest = NODE_ENV === "test";

/**
 * Centralized configuration object
 */
const config = {
  // Environment
  env: NODE_ENV,
  isProd,
  isDev,
  isTest,

  // Server settings
  server: {
    port: parseInt(process.env.PORT || "3000", 10),
    host: process.env.HOST || "localhost",
    apiBase: "/api/v1",
  },

  // AI models configuration
  models: {
    openaiApiKey: process.env.OPENAI_API_KEY,
    defaultModel: process.env.DEFAULT_MODEL || "gpt-3.5-turbo",
    advancedModel: process.env.ADVANCED_MODEL || "gpt-4",
  },

  // Engine settings
  engines: {
    engine1Model: process.env.ENGINE1_MODEL || "gpt-3.5-turbo",
    engine2Model: process.env.ENGINE2_MODEL || "gpt-4",
    engine3Model: process.env.ENGINE3_MODEL || "gpt-4",
    engine4Model: process.env.ENGINE4_MODEL || "gpt-4-turbo",
  },

  // Mode configuration
  modes: {
    archivist: {
      level: 1,
      maxTokens: 2000,
      timeoutSeconds: 30,
    },
    orchestrator: {
      level: 2,
      maxTokens: 4000,
      timeoutSeconds: 60,
    },
    godfather: {
      level: 3,
      maxTokens: 8000,
      timeoutSeconds: 120,
    },
    entity: {
      level: 4,
      maxTokens: 16000,
      timeoutSeconds: 300,
    },
  },

  // RAG system
  rag: {
    vectorDbPath: process.env.VECTOR_DB_PATH || "./data/vector_db",
    documentStorePath: process.env.DOCUMENT_STORE_PATH || "./data/documents",
    embeddingModel: process.env.EMBEDDING_MODEL || "text-embedding-3-small",
    chunkSize: parseInt(process.env.CHUNK_SIZE || "1000", 10),
    chunkOverlap: parseInt(process.env.CHUNK_OVERLAP || "200", 10),
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || (isProd ? "info" : "debug"),
    enableConsole: process.env.ENABLE_CONSOLE_LOG !== "false",
    enableFile: process.env.ENABLE_FILE_LOG === "true",
    logFilePath: process.env.LOG_FILE_PATH || "./logs/space-wh.log",
  },
};

/**
 * Validates critical configuration settings
 */
function validateConfig() {
  const errors = [];

  // Validate required configuration
  if (!config.models.openaiApiKey) {
    errors.push("Missing OPENAI_API_KEY in environment");
  }

  // Report configuration issues
  if (errors.length > 0) {
    console.error("Configuration Errors:");
    errors.forEach((error) => console.error(` - ${error}`));

    if (isProd) {
      throw new Error("Invalid configuration, cannot start in production mode");
    }
  }
}

// Run validation if not in test mode
if (!isTest) {
  validateConfig();
}

module.exports = config;
