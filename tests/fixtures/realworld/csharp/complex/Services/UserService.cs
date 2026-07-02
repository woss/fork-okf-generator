namespace OkfGen.Service.Services;

using OkfGen.Service.Models;

/// <summary>Service for managing user accounts and authentication.</summary>
public class UserService
{
    private readonly List<User> _users = new();
    private int _nextId = 1;

    /// <summary>
    /// Registers a new user account.
    /// </summary>
    /// <param name="email">Email address.</param>
    /// <param name="password">Plain-text password (hashed before storage).</param>
    /// <returns>The created User.</returns>
    public User Register(string email, string password)
    {
        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentException("Email is required.");
        if (_users.Any(u => u.Email == email))
            throw new InvalidOperationException("Email already registered.");

        var user = new User
        {
            Id = $"u_{_nextId++}",
            Email = email,
            PasswordHash = HashPassword(password),
            CreatedAt = DateTime.UtcNow
        };
        _users.Add(user);
        return user;
    }

    /// <summary>
    /// Authenticates a user by email and password.
    /// </summary>
    /// <param name="email">User's email.</param>
    /// <param name="password">Plain-text password.</param>
    /// <returns>The authenticated User, or null on failure.</returns>
    public User? Login(string email, string password)
    {
        var user = _users.FirstOrDefault(u => u.Email == email);
        if (user == null || !VerifyPassword(password, user.PasswordHash))
            return null;
        return user;
    }

    /// <summary>
    /// Returns all registered users.
    /// </summary>
    public IReadOnlyList<User> GetAllUsers() => _users.AsReadOnly();

    private static string HashPassword(string password)
    {
        return Convert.ToHexString(
            System.Security.Cryptography.SHA256.HashData(
                System.Text.Encoding.UTF8.GetBytes(password)));
    }

    private static bool VerifyPassword(string password, string hash)
    {
        return HashPassword(password) == hash;
    }
}

/// <summary>Internal user entity for the service layer.</summary>
internal class User
{
    public string Id { get; init; }
    public string Email { get; init; }
    public string PasswordHash { get; set; }
    public DateTime CreatedAt { get; init; }
}
