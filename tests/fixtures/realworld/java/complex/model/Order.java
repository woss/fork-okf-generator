package com.okfgen.payment.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Represents a customer order in the payment processing system.
 */
public class Order implements Comparable<Order> {

    /** Possible states of an order lifecycle. */
    public enum Status {
        PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
    }

    private final String id;
    private final String customerId;
    private final List<OrderItem> items;
    private Status status;
    private final LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    /**
     * Constructs a new Order.
     *
     * @param id         unique identifier
     * @param customerId owning customer
     */
    public Order(String id, String customerId) {
        this.id = id;
        this.customerId = customerId;
        this.items = new ArrayList<>();
        this.status = Status.PENDING;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = this.createdAt;
    }

    /**
     * Adds an item to this order.
     *
     * @param item the item to add
     */
    public void addItem(OrderItem item) {
        this.items.add(item);
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Calculates the total value of all items in this order.
     *
     * @return total as BigDecimal
     */
    public BigDecimal getTotal() {
        return items.stream()
                .map(OrderItem::getSubtotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    /**
     * Confirms the order, transitioning from PENDING to CONFIRMED.
     *
     * @throws IllegalStateException if the order is not in PENDING status
     */
    public void confirm() {
        if (this.status != Status.PENDING) {
            throw new IllegalStateException("Only pending orders can be confirmed");
        }
        this.status = Status.CONFIRMED;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Cancels the order.
     */
    public void cancel() {
        this.status = Status.CANCELLED;
        this.updatedAt = LocalDateTime.now();
    }

    public String getId() { return id; }
    public String getCustomerId() { return customerId; }
    public List<OrderItem> getItems() { return new ArrayList<>(items); }
    public Status getStatus() { return status; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }

    @Override
    public int compareTo(Order other) {
        return this.createdAt.compareTo(other.createdAt);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Order order)) return false;
        return Objects.equals(id, order.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    /**
     * Immutable value object representing a single line item.
     */
    public static class OrderItem {
        private final String productId;
        private final int quantity;
        private final BigDecimal unitPrice;

        public OrderItem(String productId, int quantity, BigDecimal unitPrice) {
            this.productId = productId;
            this.quantity = quantity;
            this.unitPrice = unitPrice;
        }

        public BigDecimal getSubtotal() {
            return unitPrice.multiply(BigDecimal.valueOf(quantity));
        }

        public String getProductId() { return productId; }
        public int getQuantity() { return quantity; }
        public BigDecimal getUnitPrice() { return unitPrice; }
    }
}
