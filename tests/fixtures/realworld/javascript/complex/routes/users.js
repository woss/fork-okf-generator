/**
 * User route handler for the API server.
 * @module routes/users
 */

/**
 * In-memory user store (replaces a real database).
 * @type {Array<object>}
 */
const users = [
  { id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'admin' },
  { id: 2, name: 'Bob Smith', email: 'bob@example.com', role: 'user' },
];

/**
 * Handle GET /api/users requests.
 * Supports optional ?role= query parameter filtering.
 * @param {object} req - Extended request object with parsed body and user.
 * @param {object} req.query - URL query parameters.
 * @param {string} [req.query.role] - Filter by user role.
 * @param {object} req.user - Authenticated user from middleware.
 * @returns {Promise<{statusCode: number, data: object}>} API response.
 */
async function handleUsersRoute(req) {
  const { role } = req.query || {};
  let result = users;
  if (role) {
    result = users.filter((u) => u.role === role);
  }
  return {
    statusCode: 200,
    data: {
      count: result.length,
      users: result.map(({ id, name, email, role }) => ({
        id, name, email, role,
      })),
    },
  };
}

/**
 * Add a new user to the in-memory store.
 * @param {object} userData - User fields (name, email, role).
 * @param {string} userData.name - Full name.
 * @param {string} userData.email - Email address.
 * @param {string} [userData.role='user'] - User role.
 * @returns {{id: number, name: string, email: string, role: string}} The created user.
 */
function addUser(userData) {
  const { name, email, role = 'user' } = userData;
  const newUser = {
    id: users.length + 1,
    name,
    email,
    role,
  };
  users.push(newUser);
  return newUser;
}

module.exports = { handleUsersRoute, addUser };
