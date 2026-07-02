namespace OkfGen.Service.Models;

/// <summary>Order status lifecycle.</summary>
public enum OrderStatus
{
    Pending,
    Confirmed,
    Shipped,
    Delivered,
    Cancelled
}

/// <summary>Represents a customer order.</summary>
[Serializable]
public class Order
{
    /// <summary>Unique order identifier.</summary>
    public string Id { get; init; }

    /// <summary>Customer who placed the order.</summary>
    public string CustomerId { get; init; }

    /// <summary>Line items in this order.</summary>
    public List<OrderItem> Items { get; set; } = new();

    /// <summary>Current order status.</summary>
    public OrderStatus Status { get; set; } = OrderStatus.Pending;

    /// <summary>Order creation timestamp.</summary>
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;

    /// <summary>Last modification timestamp.</summary>
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    /// <summary>Calculates the total value of all items.</summary>
    public decimal GetTotal() => Items.Sum(i => i.UnitPrice * i.Quantity);

    /// <summary>Confirms the order.</summary>
    public void Confirm()
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException("Only pending orders can be confirmed.");
        Status = OrderStatus.Confirmed;
        UpdatedAt = DateTime.UtcNow;
    }
}

/// <summary>A single line item within an order.</summary>
[Serializable]
public class OrderItem
{
    public string ProductId { get; init; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; init; }
}
