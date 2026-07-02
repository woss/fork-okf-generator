-- Enterprise order management schema with audit trail.

CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled');

CREATE TABLE users (
    id          INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email       TEXT        NOT NULL UNIQUE,
    password_hash TEXT      NOT NULL,
    display_name TEXT,
    is_active   BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE inventory (
    product_id  INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sku         TEXT        NOT NULL UNIQUE,
    name        TEXT        NOT NULL,
    unit_price  NUMERIC(10,2) NOT NULL CHECK (unit_price > 0),
    quantity    INTEGER     NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reorder_at  INTEGER     NOT NULL DEFAULT 10,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_inventory_low_stock ON inventory(quantity) WHERE quantity <= reorder_at;

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id     INTEGER     NOT NULL REFERENCES users(id),
    status      order_status NOT NULL DEFAULT 'pending',
    total       NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
    order_id    INTEGER     NOT NULL REFERENCES orders(id),
    product_id  INTEGER     NOT NULL REFERENCES inventory(product_id),
    quantity    INTEGER     NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE audit_log (
    id          INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    table_name  TEXT        NOT NULL,
    record_id   INTEGER     NOT NULL,
    action      TEXT        NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values  JSONB,
    new_values  JSONB,
    changed_by  INTEGER     REFERENCES users(id),
    changed_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_log_table ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_time ON audit_log(changed_at);
