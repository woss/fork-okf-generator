<?php

/**
 * Greet a user by name.
 */
function greet(string $name): string {
    return "Hello, " . $name;
}

/**
 * Format a number as currency.
 */
function format_currency(float $amount, string $currency = 'USD'): string {
    return $currency . ' ' . number_format($amount, 2);
}
