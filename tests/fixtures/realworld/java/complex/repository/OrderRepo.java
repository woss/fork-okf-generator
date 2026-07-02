package com.okfgen.payment.repository;

import com.okfgen.payment.model.Order;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/**
 * Generic repository interface for entities with string IDs.
 *
 * @param <T> entity type, must extend {@link Comparable}
 */
public interface Repository<T extends Comparable<T>> {
    T save(T entity);
    Optional<T> findById(String id);
    List<T> findAll();
    void deleteById(String id);
    long count();
}

/**
 * In-memory implementation of {@link Repository} for Order entities.
 */
public class OrderRepo implements Repository<Order> {

    private final Map<String, Order> store = new ConcurrentHashMap<>();

    @Override
    public Order save(Order order) {
        Objects.requireNonNull(order, "Order must not be null");
        store.put(order.getId(), order);
        return order;
    }

    @Override
    public Optional<Order> findById(String id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public List<Order> findAll() {
        return new ArrayList<>(store.values());
    }

    @Override
    public void deleteById(String id) {
        store.remove(id);
    }

    @Override
    public long count() {
        return store.size();
    }

    /**
     * Finds all orders belonging to a specific customer.
     *
     * @param customerId the customer identifier
     * @return list of orders for that customer
     */
    public List<Order> findByCustomerId(String customerId) {
        return store.values().stream()
                .filter(o -> o.getCustomerId().equals(customerId))
                .sorted()
                .collect(Collectors.toList());
    }
}
