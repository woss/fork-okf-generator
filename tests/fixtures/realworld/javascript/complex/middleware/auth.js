/**
 * Authentication middleware for the API server.
 * @module middleware/auth
 */

const VALID_TOKENS = new Set([
  'Bearer token-admin-001',
  'Bearer token-user-002',
]);

/**
 * Authenticate an incoming HTTP request using the Authorization header.
 * @param {object} req - The HTTP request object.
 * @param {string} [req.headers.authorization] - Bearer token.
 * @returns {{ok: boolean, user?: object, error?: string}} Auth result.
 */
function authenticate(req) {
  const authHeader = req.headers && req.headers.authorization;
  if (!authHeader) {
    return { ok: false, error: 'Missing Authorization header' };
  }
  if (!VALID_TOKENS.has(authHeader)) {
    return { ok: false, error: 'Invalid or expired token' };
  }
  const role = authHeader.includes('admin') ? 'admin' : 'user';
  return {
    ok: true,
    user: {
      id: authHeader === 'Bearer token-admin-001' ? 1 : 2,
      role,
    },
  };
}

/**
 * Verify that the authenticated user has a specific role.
 * @param {object} user - The authenticated user object.
 * @param {string} requiredRole - The role to check for.
 * @returns {boolean} True if the user has the required role.
 */
function requireRole(user, requiredRole) {
  return user && user.role === requiredRole;
}

module.exports = { authenticate, requireRole };
