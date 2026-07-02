-- E-commerce schema with categories, products, and customer tables.

CREATE TABLE categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    sku         TEXT    NOT NULL UNIQUE,
    name        TEXT    NOT NULL,
    price       REAL    NOT NULL CHECK (price > 0),
    stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    active      INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(active) WHERE active = 1;

CREATE TABLE customers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT    NOT NULL UNIQUE,
    first_name  TEXT    NOT NULL,
    last_name   TEXT    NOT NULL,
    phone       TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE VIEW active_products AS
SELECT p.id, p.name, p.price, c.name AS category
FROM products p
JOIN categories c ON c.id = p.category_id
WHERE p.active = 1;

-- Products available in stock with pricing info.
CREATE VIEW available_inventory AS
SELECT p.id, p.sku, p.name, p.price, p.stock, c.name AS category
FROM products p
JOIN categories c ON c.id = p.category_id
WHERE p.active = 1 AND p.stock > 0;
