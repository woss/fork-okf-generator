<?php

namespace App\Math;

/**
 * A simple calculator class.
 */
class Calculator {
    private float $result = 0.0;

    public function __construct() {
        $this->result = 0.0;
    }

    /**
     * Add a number to the current result.
     */
    public function add(float $value): float {
        $this->result += $value;
        return $this->result;
    }

    public function reset(): void {
        $this->result = 0.0;
    }

    public static function version(): string {
        return '1.0.0';
    }
}
