/**
 * Express-like HTTP server for the user management API.
 * @module server
 */

const http = require('http');
const { handleUsersRoute } = require('./routes/users');
const { authenticate } = require('./middleware/auth');

const PORT = process.env.PORT || 3000;

/**
 * Simple request router that dispatches to route handlers.
 * @extends http.Server
 */
class ApiServer {
  /**
   * Create a new ApiServer instance.
   * @param {object} [options] - Server configuration.
   * @param {number} [options.port=3000] - Listening port.
   * @param {string} [options.host='0.0.0.0'] - Binding address.
   */
  constructor(options = {}) {
    this.port = options.port || PORT;
    this.host = options.host || '0.0.0.0';
    this.routes = new Map();
    this.server = null;
    this._registerRoutes();
  }

  /** Register the default API routes. */
  _registerRoutes() {
    this.routes.set('GET /api/users', handleUsersRoute);
  }

  /**
   * Parse the incoming HTTP request body as JSON.
   * @param {http.IncomingMessage} req - The request object.
   * @returns {Promise<object>} Parsed JSON body.
   */
  _parseBody(req) {
    return new Promise((resolve, reject) => {
      let body = '';
      req.on('data', (chunk) => {
        body += chunk.toString();
      });
      req.on('end', () => {
        try {
          resolve(body ? JSON.parse(body) : {});
        } catch (err) {
          reject(new Error('Invalid JSON in request body'));
        }
      });
      req.on('error', reject);
    });
  }

  /**
   * Start the HTTP server.
   * @returns {Promise<void>}
   */
  async start() {
    return new Promise((resolve, reject) => {
      this.server = http.createServer(async (req, res) => {
        res.setHeader('Content-Type', 'application/json');
        try {
          const authResult = authenticate(req);
          if (!authResult.ok) {
            res.statusCode = 401;
            res.end(JSON.stringify({ error: authResult.error }));
            return;
          }
          const routeKey = `${req.method} ${req.url.split('?')[0]}`;
          const handler = this.routes.get(routeKey);
          if (!handler) {
            res.statusCode = 404;
            res.end(JSON.stringify({ error: 'Not found' }));
            return;
          }
          const body = await this._parseBody(req);
          const result = await handler({ ...req, body, user: authResult.user });
          res.statusCode = result.statusCode || 200;
          res.end(JSON.stringify(result.data || {}));
        } catch (err) {
          res.statusCode = 500;
          res.end(JSON.stringify({ error: err.message || 'Internal server error' }));
        }
      });
      this.server.listen(this.port, this.host, () => {
        console.log(`Server listening on ${this.host}:${this.port}`);
        resolve();
      });
      this.server.on('error', reject);
    });
  }

  /**
   * Gracefully stop the server.
   * @returns {Promise<void>}
   */
  async stop() {
    return new Promise((resolve, reject) => {
      if (!this.server) {
        resolve();
        return;
      }
      this.server.close((err) => {
        if (err) return reject(err);
        this.server = null;
        resolve();
      });
    });
  }
}

module.exports = { ApiServer };
