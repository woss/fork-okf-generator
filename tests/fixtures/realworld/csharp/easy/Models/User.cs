namespace OkfGen.Utils.Models;

/// <summary>
/// Represents a user entity in the system.
/// </summary>
public class User
{
    /// <summary>Unique identifier.</summary>
    public string Id { get; init; }

    /// <summary>Email address.</summary>
    public string Email { get; set; }

    /// <summary>Display name.</summary>
    public string? DisplayName { get; set; }

    /// <summary>Whether the account is active.</summary>
    public bool IsActive { get; set; } = true;

    /// <summary>Timestamp of account creation.</summary>
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;

    /// <summary>
    /// Returns a display-friendly representation of the user.
    /// </summary>
    public string GetDisplayText() => DisplayName ?? Email;

    /// <summary>
    /// Deactivates the user account.
    /// </summary>
    public void Deactivate() => IsActive = false;
}
