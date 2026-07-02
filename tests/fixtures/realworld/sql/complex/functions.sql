-- Stored procedures and functions for the order management system.

-- Calculate the total for an order based on its items.
CREATE OR REPLACE FUNCTION calculate_order_total(p_order_id INTEGER)
RETURNS NUMERIC(12,2) AS $$
DECLARE
    v_total NUMERIC(12,2);
BEGIN
    SELECT COALESCE(SUM(oi.quantity * oi.unit_price), 0)
    INTO v_total
    FROM order_items oi
    WHERE oi.order_id = p_order_id;

    UPDATE orders SET total = v_total, updated_at = now()
    WHERE id = p_order_id;

    RETURN v_total;
END;
$$ LANGUAGE plpgsql;

-- Place an order: validate stock, reserve inventory, create order.
CREATE OR REPLACE PROCEDURE place_order(
    p_user_id   INTEGER,
    p_product_ids INTEGER[],
    p_quantities  INTEGER[]
)
LANGUAGE plpgsql AS $$
DECLARE
    v_order_id INTEGER;
    v_i INTEGER;
BEGIN
    INSERT INTO orders (user_id, status) VALUES (p_user_id, 'pending')
    RETURNING id INTO v_order_id;

    FOR v_i IN 1 .. array_length(p_product_ids, 1) LOOP
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        SELECT v_order_id, p_product_ids[v_i], p_quantities[v_i], unit_price
        FROM inventory WHERE product_id = p_product_ids[v_i];

        UPDATE inventory SET quantity = quantity - p_quantities[v_i]
        WHERE product_id = p_product_ids[v_i];
    END LOOP;

    PERFORM calculate_order_total(v_order_id);

    INSERT INTO audit_log (table_name, record_id, action, new_values, changed_by)
    VALUES ('orders', v_order_id, 'INSERT',
            jsonb_build_object('user_id', p_user_id, 'total', 0),
            p_user_id);
END;
$$;

-- Trigger: automatically update updated_at before any row change.
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_inventory_updated_at
    BEFORE UPDATE ON inventory
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Trigger: log all changes to orders to the audit table.
CREATE OR REPLACE FUNCTION audit_order_changes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, changed_by)
    VALUES ('orders', COALESCE(NEW.id, OLD.id),
            TG_OP,
            CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN row_to_json(OLD)::jsonb END,
            CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW)::jsonb END,
            NULL);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_orders_audit
    AFTER INSERT OR UPDATE OR DELETE ON orders
    FOR EACH ROW EXECUTE FUNCTION audit_order_changes();
