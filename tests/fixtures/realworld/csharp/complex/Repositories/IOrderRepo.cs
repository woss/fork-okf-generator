namespace OkfGen.Service.Repositories;

using OkfGen.Service.Models;

/// <summary>
/// Generic repository interface for CRUD operations.
/// </summary>
/// <typeparam name="T">Entity type.</typeparam>
public interface IRepository<T>
{
    T Save(T entity);
    T? FindById(string id);
    IReadOnlyList<T> FindAll();
    bool Delete(string id);
    long Count();
}

/// <summary>
/// In-memory implementation of IRepository for Order entities.
/// </summary>
public class OrderRepository : IRepository<Order>
{
    private readonly Dictionary<string, Order> _store = new();

    public Order Save(Order order)
    {
        _store[order.Id] = order;
        return order;
    }

    public Order? FindById(string id)
    {
        _store.TryGetValue(id, out var order);
        return order;
    }

    public IReadOnlyList<Order> FindAll()
    {
        return _store.Values.ToList().AsReadOnly();
    }

    public bool Delete(string id)
    {
        return _store.Remove(id);
    }

    public long Count() => _store.Count;

    /// <summary>
    /// Finds all orders for a given customer, ordered by creation date.
    /// </summary>
    public IEnumerable<Order> FindByCustomer(string customerId)
    {
        return _store.Values
            .Where(o => o.CustomerId == customerId)
            .OrderBy(o => o.CreatedAt);
    }

    /// <summary>
    /// Finds all orders in a given status.
    /// </summary>
    [Obsolete("Use FindByStatusAsync instead for better performance.")]
    public IEnumerable<Order> FindByStatus(OrderStatus status)
    {
        return _store.Values.Where(o => o.Status == status);
    }

    /// <summary>Async version of FindByStatus.</summary>
    public async Task<IEnumerable<Order>> FindByStatusAsync(OrderStatus status)
    {
        await Task.CompletedTask;
        return _store.Values.Where(o => o.Status == status);
    }
}
