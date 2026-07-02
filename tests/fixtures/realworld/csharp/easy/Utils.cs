namespace OkfGen.Utils;

/// <summary>
/// Static utility methods for common data transformations.
/// </summary>
public static class Utils
{
    /// <summary>
    /// Computes the SHA-256 hash of a string as a lowercase hex string.
    /// </summary>
    /// <param name="input">The input string.</param>
    /// <returns>Hex-encoded SHA-256 digest.</returns>
    public static string Sha256Hex(string input)
    {
        var bytes = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(input));
        return Convert.ToHexStringLower(bytes);
    }

    /// <summary>
    /// Checks whether a string is a valid email address using a simple regex.
    /// </summary>
    /// <param name="email">Email address to validate.</param>
    /// <returns>True if the format is valid.</returns>
    public static bool IsValidEmail(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
            return false;
        var atIndex = email.IndexOf('@');
        if (atIndex <= 0 || atIndex == email.Length - 1)
            return false;
        var dotIndex = email.LastIndexOf('.');
        return dotIndex > atIndex + 1 && dotIndex < email.Length - 1;
    }

    /// <summary>
    /// Truncates a string to the specified maximum length.
    /// </summary>
    /// <param name="text">Input text.</param>
    /// <param name="maxLength">Maximum allowed length.</param>
    /// <returns>Truncated string with "..." if shortened.</returns>
    public static string Truncate(string text, int maxLength)
    {
        if (string.IsNullOrEmpty(text) || text.Length <= maxLength)
            return text;
        return text[..(maxLength - 3)] + "...";
    }
}
