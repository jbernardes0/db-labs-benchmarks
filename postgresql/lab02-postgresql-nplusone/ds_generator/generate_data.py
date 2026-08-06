import os
import time
import random
import argparse
from faker import Faker
import psycopg

# -------------------------------------------------------------------
# CLI arguments
# -------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description="Generate customers, orders and order_items with skew (N+1 lab)"
)

parser.add_argument("--customers", type=int, default=100, help="Total customers")
parser.add_argument("--orders", type=int, default=1_000, help="Total orders")
parser.add_argument("--days", type=int, default=90, help="Date range in days")

# customer skew
parser.add_argument("--heavy-customers-pct", type=float, default=0.10)
parser.add_argument("--medium-customers-pct", type=float, default=0.30)
parser.add_argument("--light-customers-pct", type=float, default=0.60)

args = parser.parse_args()

# -------------------------------------------------------------------
# Sanity checks
# -------------------------------------------------------------------
if abs(
    (args.heavy_customers_pct +
     args.medium_customers_pct +
     args.light_customers_pct) - 1.0
) > 0.0001:
    raise ValueError("Customer percentages must sum to 1.0")

# -------------------------------------------------------------------
# Dataset rules
# -------------------------------------------------------------------
ITEMS_PER_ORDER = {
    "heavy": (50, 100),
    "medium": (10, 30),
    "light": (1, 5),
}

# -------------------------------------------------------------------
# Random / Faker
# -------------------------------------------------------------------
random.seed(42)
Faker.seed(42)
fake = Faker("pt_BR")

# -------------------------------------------------------------------
# Database connection info
# -------------------------------------------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nplusone")
DB_USER = os.getenv("DB_USER", "lab")
DB_PASSWORD = os.getenv("DB_PASSWORD", "lab")

# -------------------------------------------------------------------
# Wait for database
# -------------------------------------------------------------------
print("🔄 Waiting for database...")

conn = None
for attempt in range(10):
    try:
        conn = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=True,
        )
        print("✅ Connected to database")
        break
    except Exception:
        print(f"⏳ DB not ready ({attempt + 1}/10)")
        time.sleep(2)
else:
    raise RuntimeError("Database not available")

# -------------------------------------------------------------------
# Customer distribution (VERY IMPORTANT)
# -------------------------------------------------------------------
print("🧠 Preparing customer distribution")

customer_ids = list(range(1, args.customers + 1))
random.shuffle(customer_ids)

heavy_cut = int(args.customers * args.heavy_customers_pct)
medium_cut = heavy_cut + int(args.customers * args.medium_customers_pct)

HEAVY_CUSTOMERS = customer_ids[:heavy_cut]
MEDIUM_CUSTOMERS = customer_ids[heavy_cut:medium_cut]
LIGHT_CUSTOMERS = customer_ids[medium_cut:]

def choose_customer_id():
    r = random.random()
    if r < 0.60:
        return random.choice(HEAVY_CUSTOMERS)
    elif r < 0.90:
        return random.choice(MEDIUM_CUSTOMERS)
    else:
        return random.choice(LIGHT_CUSTOMERS)

# -------------------------------------------------------------------
# Order skew (by size)
# -------------------------------------------------------------------
def choose_order_size():
    r = random.random()
    if r < 0.05:
        return "heavy"
    elif r < 0.25:
        return "medium"
    else:
        return "light"

# -------------------------------------------------------------------
# Data generation
# -------------------------------------------------------------------
print("🚀 Deploying dataset...")
print(f"   Customers: {args.customers}")
print(f"   Orders:    {args.orders}")

order_id = 1
item_id = 1

with conn.cursor() as cur:
    # ---------------------------------------------------------------
    # Customers
    # ---------------------------------------------------------------
    print("👤 Inserting customers")

    for cid in range(1, args.customers + 1):
        cur.execute(
            """
            INSERT INTO customers (id, name)
            VALUES (%s, %s)
            """,
            (cid, fake.name()),
        )

    # ---------------------------------------------------------------
    # Orders + Order Items
    # ---------------------------------------------------------------
    print("📦 Inserting orders and order_items")

    for i in range(args.orders):
        order_size = choose_order_size()
        min_items, max_items = ITEMS_PER_ORDER[order_size]
        items_count = random.randint(min_items, max_items)

        customer_id = choose_customer_id()
        created_at = fake.date_time_between(
            start_date=f"-{args.days}d",
            end_date="now"
        )

        order_total = 0.0
        current_order_id = order_id
        order_id += 1

        cur.execute(
            """
            INSERT INTO orders (id, customer_id, created_at)
            VALUES (%s, %s, %s)
            """,
            (current_order_id, customer_id, created_at),
        )

        for _ in range(items_count):
            qty = random.randint(1, 5)
            price = round(random.uniform(10, 500), 2)
            order_total += qty * price

            cur.execute(
                """
                INSERT INTO order_items
                  (id, order_id, product_name, quantity, unit_price)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    item_id,
                    current_order_id,
                    fake.word(),
                    qty,
                    price,
                ),
            )
            item_id += 1

        if (i + 1) % 100 == 0:
            print(f"✅ {i + 1}/{args.orders} orders generated")

print("🎉 Dataset generation finished!")

# -------------------------------------------------------------------
# Keep container alive (didatic mode)
# -------------------------------------------------------------------
print("")
print("📌 Dataset ready.")
print("📌 You can now run your N+1 workload.")
print("📌 Press ENTER to terminate this container.")
input()