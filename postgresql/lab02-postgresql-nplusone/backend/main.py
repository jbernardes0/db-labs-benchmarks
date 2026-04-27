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
    "row_factory": psycopg.rows.dict_row,
}

def get_conn():
    return psycopg.connect(**DB_CONFIG)

# -------------------------------------------------------------------
# Endpoint ERRADO – N+1 proposital
# -------------------------------------------------------------------

@app.get("/customers/{customer_id}/products/nplus1")
def customer_products_nplus1(customer_id: int):
    conn = get_conn()
    products = []

    with conn.cursor() as cur:
        # 1 query: pedidos do cliente
        cur.execute(
            """
            SELECT 
                o.id as order_id, 
                c.name as customer_name
            FROM orders o
            JOIN customers c ON c.id = o.customer_id
            WHERE c.id = %s
            """,
            (customer_id,),
        )
        orders = cur.fetchall()

        for order in orders:
            # N queries: itens por pedido
            cur.execute(
                """
                SELECT product_name, count(*) as bought
                FROM order_items
                WHERE order_id = %s
                GROUP BY product_name
                """,
                (order['order_id'],),
            )
            items = cur.fetchall()

            for item in items:
                products.append({
                    "name": item['product_name'],
                    "quantity_bought": item['bought'],
                })

    conn.close()
    return {
        "strategy": "N+1 (intencionalmente ineficiente)",
        "customer_name": orders[0]['customer_name'] if orders else None,
        "products_purchased": len(products),
        "products": products,
    }


# -------------------------------------------------------------------
# Endpoint CORRETO – set-based
# -------------------------------------------------------------------


@app.get("/customers/{customer_id}/products/join")
def customer_products_join(customer_id: int):
    conn = get_conn()
    products = []

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                c.name AS customer_name,
                oi.product_name,
                COUNT(*) AS quantity_bought
            FROM customers c
            JOIN orders o
              ON o.customer_id = c.id
            JOIN order_items oi
              ON oi.order_id = o.id
            WHERE c.id = %s
            GROUP BY
                c.name,
                oi.product_name
            ORDER BY
                oi.product_name
            """,
            (customer_id,),
        )

        rows = cur.fetchall()

        for row in rows:
            products.append({
                "name": row["product_name"],
                "quantity_bought": row["quantity_bought"],
            })

    conn.close()

    return {
        "strategy": "JOIN (set-based)",
        "customer_name": rows[0]["customer_name"] if rows else None,
        "products_purchased": len(products),
        "products": products,
    }
