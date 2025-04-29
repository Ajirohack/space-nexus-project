/**
 * Error Handling Utility
 *
 * Provides consistent error handling and custom error classes for the Space-WH system
 */

const { createLogger } = require("./logger");
const logger = createLogger("ErrorHandler");

/**
 * Base error class for the Space-WH system
 */
class SpaceError extends Error {
  constructor(message, options = {}) {
    super(message);
    this.name = this.constructor.name;
    this.code = options.code || "SPACE_ERROR";
    this.status = options.status || 500;
    this.details = options.details || {};

    // Log error automatically unless explicitly suppressed
    if (options.log !== false) {
      this.logError();
    }
  }

  /**
   * Log the error with appropriate level and details
   */
  logError() {
    const errorData = {
      code: this.code,
      name: this.name,
      status: this.status,
      ...this.details,
    };

    if (this.status >= 500) {
      logger.error(`${this.message}`, errorData);
    } else {
      logger.warn(`${this.message}`, errorData);
    }
  }

  /**
   * Convert the error to a JSON representation for API responses
   */
  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        details: this.details,
        status: this.status,
      },
    };
  }
}

/**
 * Error classes for validation errors
 */
class ValidationError extends SpaceError {
  constructor(message, details = {}) {
    super(message, {
      code: "VALIDATION_ERROR",
      status: 400,
      details,
    });
  }
}

/**
 * Error classes for authentication errors
 */
class AuthenticationError extends SpaceError {
  constructor(message, details = {}) {
    super(message, {
      code: "AUTHENTICATION_ERROR",
      status: 401,
      details,
    });
  }
}

/**
 * Error classes for authorization errors
 */
class AuthorizationError extends SpaceError {
  constructor(message, details = {}) {
    super(message, {
      code: "AUTHORIZATION_ERROR",
      status: 403,
      details,
    });
  }
}

/**
 * Error classes for not found errors
 */
class NotFoundError extends SpaceError {
  constructor(message, details = {}) {
    super(message, {
      code: "NOT_FOUND",
      status: 404,
      details,
    });
  }
}

/**
 * Error classes for rate limit errors
 */
class RateLimitError extends SpaceError {
  constructor(message, details = {}) {
    super(message, {
      code: "RATE_LIMIT_EXCEEDED",
      status: 429,
      details,
    });
  }
}

/**
 * Error classes for AI model errors
 */
class ModelError extends SpaceError {
  constructor(message, details = {}) {
    super(message, {
      code: "MODEL_ERROR",
      status: 500,
      details,
    });
  }
}

/**
 * Error classes for tool execution errors
 */
class ToolError extends SpaceError {
  constructor(message, details = {}) {
    super(message, {
      code: "TOOL_ERROR",
      status: 500,
      details,
    });
  }
}

/**
 * Express middleware for handling errors
 */
function errorHandler(err, req, res, next) {
  // Convert to SpaceError if it's not already one
  const error =
    err instanceof SpaceError
      ? err
      : new SpaceError(err.message, {
          code: err.code || "INTERNAL_ERROR",
          status: err.status || 500,
          details: {
            stack: err.stack,
          },
        });

  // Send error response
  res.status(error.status).json(error.toJSON());
}

module.exports = {
  SpaceError,
  ValidationError,
  AuthenticationError,
  AuthorizationError,
  NotFoundError,
  RateLimitError,
  ModelError,
  ToolError,
  errorHandler,
};
