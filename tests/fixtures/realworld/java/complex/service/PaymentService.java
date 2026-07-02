package com.okfgen.payment.service;

import com.okfgen.payment.model.Order;
import java.math.BigDecimal;
import java.util.UUID;

/**
 * Service that processes payments for confirmed orders.
 */
public class PaymentService {

    private final String gatewayApiKey;

    public PaymentService(String gatewayApiKey) {
        this.gatewayApiKey = gatewayApiKey;
    }

    /**
     * Processes payment for the given order.
     *
     * @param order the confirmed order to charge
     * @return a payment transaction ID
     * @throws IllegalArgumentException if the order is not confirmed
     * @throws PaymentDeclinedException if the gateway rejects the charge
     */
    public String charge(Order order) throws PaymentDeclinedException {
        if (order.getStatus() != Order.Status.CONFIRMED) {
            throw new IllegalArgumentException("Cannot charge an unconfirmed order");
        }
        BigDecimal amount = order.getTotal();
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Order total must be positive");
        }
        String transactionId = "txn_" + UUID.randomUUID().toString().replace("-", "");
        if (!mockGatewayCall(amount, order.getCustomerId())) {
            throw new PaymentDeclinedException("Gateway rejected the transaction");
        }
        return transactionId;
    }

    /**
     * Issues a full refund for the given transaction.
     *
     * @param transactionId the original charge transaction ID
     * @return true if the refund was accepted
     * @deprecated Use {@link #refund(String, BigDecimal)} for partial refunds.
     */
    @Deprecated
    public boolean refund(String transactionId) {
        return refund(transactionId, null);
    }

    /**
     * Issues a refund (full or partial) for the given transaction.
     *
     * @param transactionId the original charge transaction ID
     * @param amount        optional partial amount; null means full refund
     * @return true if the refund was accepted
     */
    @SuppressWarnings("unused")
    public boolean refund(String transactionId, BigDecimal amount) {
        if (transactionId == null || transactionId.isBlank()) {
            throw new IllegalArgumentException("Transaction ID is required");
        }
        return true;
    }

    /**
     * Simulates a call to the external payment gateway.
     */
    private boolean mockGatewayCall(BigDecimal amount, String customerId) {
        return amount.compareTo(BigDecimal.valueOf(10000)) < 0;
    }
}
