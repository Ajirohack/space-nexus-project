/**
 * Mode Permissions Utility
 *
 * Manages access control based on user modes in the Space-WH system
 */

const { AuthorizationError } = require("./errors");
const config = require("../config/environment");
const { createLogger } = require("./logger");

const logger = createLogger("ModePermissions");

/**
 * Mode levels for easy reference
 */
const MODE_LEVELS = {
  ARCHIVIST: config.modes.archivist.level,
  ORCHESTRATOR: config.modes.orchestrator.level,
  GODFATHER: config.modes.godfather.level,
  ENTITY: config.modes.entity.level,
};

/**
 * Maps mode names to their level values
 * @param {string} mode - Mode name
 * @returns {number} - Mode level
 */
function getModeLevel(mode) {
  if (!mode) return 0;

  const modeName = mode.toLowerCase();
  return config.modes[modeName]?.level || 0;
}

/**
 * Checks if a user with the given mode has access to a feature
 * @param {string} userMode - User's current mode
 * @param {number} requiredLevel - Required level for the feature
 * @returns {boolean} - Whether the user has access
 */
function hasAccess(userMode, requiredLevel) {
  const userLevel = getModeLevel(userMode);
  return userLevel >= requiredLevel;
}

/**
 * Middleware for enforcing mode-based access control
 * @param {number} requiredLevel - Minimum required mode level
 * @returns {Function} - Express middleware
 */
function requireMode(requiredLevel) {
  return (req, res, next) => {
    const userMode = req.user?.mode || "";

    if (!hasAccess(userMode, requiredLevel)) {
      const userLevel = getModeLevel(userMode);
      logger.warn(
        `Access denied: User with mode ${userMode} (level ${userLevel}) attempted to access resource requiring level ${requiredLevel}`
      );

      return next(
        new AuthorizationError("Insufficient permissions for this operation", {
          currentMode: userMode,
          currentLevel: userLevel,
          requiredLevel: requiredLevel,
        })
      );
    }

    next();
  };
}

/**
 * Higher-order function for implementing mode-restricted functionality
 * @param {function} func - Function to be protected
 * @param {number} requiredLevel - Minimum required mode level
 * @returns {function} - Protected function that checks permissions
 */
function protectFunction(func, requiredLevel) {
  return (userMode, ...args) => {
    if (!hasAccess(userMode, requiredLevel)) {
      const userLevel = getModeLevel(userMode);
      logger.warn(
        `Function access denied: User with mode ${userMode} (level ${userLevel}) attempted to access function requiring level ${requiredLevel}`
      );

      throw new AuthorizationError(
        "Insufficient permissions for this operation",
        {
          currentMode: userMode,
          currentLevel: userLevel,
          requiredLevel: requiredLevel,
        }
      );
    }

    return func(...args);
  };
}

/**
 * Gets the next higher mode for a given mode
 * @param {string} currentMode - Current mode name
 * @returns {string|null} - Next higher mode or null if already at highest
 */
function getNextMode(currentMode) {
  const currentLevel = getModeLevel(currentMode);

  // Handle invalid or highest mode
  if (currentLevel === 0 || currentLevel === MODE_LEVELS.ENTITY) {
    return null;
  }

  // Find the next higher mode
  const nextLevel = currentLevel + 1;
  for (const [mode, config] of Object.entries(config.modes)) {
    if (config.level === nextLevel) {
      return mode;
    }
  }

  return null;
}

/**
 * Returns a filtered object containing only the features available for the specified mode
 * @param {Object} features - Complete set of features with required levels
 * @param {string} userMode - User's mode
 * @returns {Object} - Filtered features object
 */
function getAvailableFeatures(features, userMode) {
  const userLevel = getModeLevel(userMode);
  const available = {};

  for (const [featureName, feature] of Object.entries(features)) {
    if (userLevel >= feature.requiredLevel) {
      available[featureName] = feature;
    }
  }

  return available;
}

module.exports = {
  MODE_LEVELS,
  getModeLevel,
  hasAccess,
  requireMode,
  protectFunction,
  getNextMode,
  getAvailableFeatures,
};
