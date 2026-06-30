/**
 * Express API server entry point.
 * @module server
 */

const express = require("express");

/**
 * Creates and configures an Express app.
 * @param {number} port - Server port number.
 * @returns {object} Configured Express application.
 */
function createApp(port = 3000) {
  const app = express();
  app.use(express.json());
  return app;
}

/**
 * Health check handler.
 * @param {object} req - Express request.
 * @param {object} res - Express response.
 */
function healthCheck(req, res) {
  res.json({ status: "ok", timestamp: Date.now() });
}

module.exports = { createApp, healthCheck };
