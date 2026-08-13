# TechScale: Data access layer
# Owns the database connection pool and all SQL queries.
# The service layer and routes must not import sqlalchemy or pyodbc directly.
#
# Cloud database behaviour to account for when configuring the pool:
#   pool_size     — persistent connections kept open at all times
#   max_overflow  — extra connections allowed above pool_size during traffic spikes
#   pool_pre_ping — verifies a pooled connection is still alive before using it;
#                   silently replaces any that Azure closed during an idle period
#   pool_recycle  — retires a connection after N seconds to prevent Azure's
#                   idle timeout from closing it underneath the pool

import urllib
from sqlalchemy import create_engine, text


# Database credentials (do not modify)
_params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=mentorskool.database.windows.net;"
    "DATABASE=mskl-masterclass;"
    "UID=mskllearnlogin;"
    "PWD=!@#sw2aq1;"
    "Encrypt=yes;TrustServerCertificate=no;"
)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={_params}"


# Connection pool configured for high-concurrency cloud workloads.
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
)


# Verify database connectivity after creating the engine.
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(f"[DB] Connection pool ready: {result.fetchone()}")


def get_top_orders():
    """Return the top 5 orders ranked by total payment value."""

    query = text(
        """
        SELECT TOP 5
            o.order_id,
            c.customer_name,
            SUM(op.payment_value) AS total_value
        FROM ORDERS o
        JOIN CUSTOMERS c
            ON o.customer_id = c.customer_id
        JOIN ORDER_PAYMENTS op
            ON o.order_id = op.order_id
        GROUP BY
            o.order_id,
            c.customer_name
        ORDER BY total_value DESC
        """
    )

    with engine.connect() as connection:
        rows = connection.execute(query).fetchall()

    return [
        {
            "order_id": row.order_id,
            "customer_name": row.customer_name,
            "total_value": round(float(row.total_value), 2),
        }
        for row in rows
    ]


# Entry point

if __name__ == "__main__":
    print("=== Connection pool test ===")
    # TODO 1 should print: [DB] Connection pool ready: (1,)

    print("\n=== Top orders query ===")
    orders = get_top_orders()
    for o in orders:
        print(f"  {o['order_id']} | {o['customer_name']} | ${o['total_value']:.2f}")