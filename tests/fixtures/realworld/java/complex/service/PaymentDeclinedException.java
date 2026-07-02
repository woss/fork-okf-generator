package com.okfgen.payment.service;

/**
 * Thrown when the payment gateway rejects a transaction.
 */
public class PaymentDeclinedException extends Exception {

    public PaymentDeclinedException(String message) {
        super(message);
    }

    public PaymentDeclinedException(String message, Throwable cause) {
        super(message, cause);
    }
}
