import os
from fastapi import FastAPI
import psycopg

app = FastAPI(title="N+1 Lab Backend")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "nplusone"),
    "user": os.getenv("DB_USER", "lab"),
    "password": os.getenv("DB_PASSWORD", "lab"),
}

def get_conn():
    return psycopg.connect(**DB_CONFIG)

# -------------------------------------------------------------------
# Endpoint ERRADO – N+1 proposital
# -------------------------------------------------------------------
@app.get("/orders/nplus1")
def list_orders_nplus1(limit: int = 100):
    conn = get_conn()
    orders = []

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, customer_id, created_at
            FROM orders
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cur.fetchall()

        for order_id, customer_id, created_at in rows:
            # Query 1+N: busca customer por order
            cur.execute(
                "SELECT name FROM customers WHERE id = %s",
                (customer_id,),
            )
            customer_name = cur.fetchone()[0]

            # Query 1+N: busca items por order
            cur.execute(
                """
                SELECT COUNT(*)
                FROM order_items
                WHERE order_id = %s
                """,
                (order_id,),
            )
            items_count = cur.fetchone()[0]

            orders.append({
                "order_id": order_id,
                "customer": customer_name,
                "items": items_count,
                "created_at": created_at,
            })

    conn.close()
    return {
        "strategy": "N+1 (intencional)",
        "orders_returned": len(orders),
        "orders": orders,
    }

# -------------------------------------------------------------------
# Endpoint CORRETO – set-based
# -------------------------------------------------------------------
@app.get("/orders/join")
def list_orders_join(limit: int = 100):
    conn = get_conn()
    orders = []

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                o.id,
                c.name AS customer_name,
                COUNT(oi.id) AS items_count,
                o.created_at
            FROM orders o
            JOIN customers c ON c.id = o.customer_id
            LEFT JOIN order_items oi ON oi.order_id = o.id
            GROUP BY o.id, c.name, o.created_at
            ORDER BY o.created_at DESC
            LIMIT %s
            """,
            (limit,),
        )

        for row in cur.fetchall():
            orders.append({
                "order_id": row[0],
                "customer": row[1],
                "items": row[2],
                "created_at": row[3],
            })

    conn.close()
    return {
        "strategy": "JOIN (set-based)",
        "orders_returned": len(orders),
        "orders": orders,
    }