/**
 * Logger Utility
 *
 * Provides consistent logging functionality throughout the Space-WH system
 */

const winston = require("winston");
const path = require("path");
const fs = require("fs");
const config = require("../config/environment");

// Ensure log directory exists
if (config.logging.enableFile) {
  const logDir = path.dirname(config.logging.logFilePath);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
}

// Define log format
const logFormat = winston.format.combine(
  winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.printf(({ level, message, timestamp, label, ...meta }) => {
    const moduleName = label ? `[${label}]` : "";
    const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : "";
    return `${timestamp} ${level.toUpperCase()} ${moduleName}: ${message} ${metaStr}`;
  })
);

// Define transports
const transports = [];

// Console transport
if (config.logging.enableConsole) {
  transports.push(
    new winston.transports.Console({
      format: winston.format.combine(winston.format.colorize(), logFormat),
    })
  );
}

// File transport
if (config.logging.enableFile) {
  transports.push(
    new winston.transports.File({
      filename: config.logging.logFilePath,
      format: logFormat,
      maxsize: 5242880, // 5MB
      maxFiles: 5,
    })
  );
}

// Create base logger
const logger = winston.createLogger({
  level: config.logging.level,
  defaultMeta: { service: "space-wh" },
  transports,
  exitOnError: false,
});

/**
 * Creates a logger for a specific module
 *
 * @param {string} moduleName - Name of the module for which to create a logger
 * @returns {object} - Winston logger instance with module context
 */
function createLogger(moduleName) {
  return logger.child({ label: moduleName });
}

module.exports = {
  createLogger,
  logger,
};
