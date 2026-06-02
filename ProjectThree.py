import pandas as pd
import sqlite3
import os
df = pd.read_csv('file/Dataset for Data Analytics.csv')
# Display basic info
print(f" Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f" Date range: {df['Date'].min()} to {df['Date'].max()}\n")

conn = sqlite3.connect(':memory:')
df.to_sql('orders', conn, index=False, if_exists='replace')
print(" SQLite in-memory database created with table 'orders'\n")


print("=" * 50)
print("1. OVERALL STATISTICS")
print("=" * 50)
total_stats = pd.read_sql_query("""
    SELECT 
        COUNT(*) AS total_orders,
        SUM(TotalPrice) AS total_revenue,
        ROUND(AVG(TotalPrice), 2) AS avg_order_value,
        MIN(TotalPrice) AS min_order_value,
        MAX(TotalPrice) AS max_order_value
    FROM orders
""", conn)
print(total_stats.to_string(index=False))
print()

print("=" * 50)
print("2. REVENUE BY PRODUCT")
print("=" * 50)
product_rev = pd.read_sql_query("""
    SELECT 
        Product,
        SUM(Quantity) AS units_sold,
        SUM(TotalPrice) AS revenue,
        ROUND(AVG(UnitPrice), 2) AS avg_unit_price,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY Product
    ORDER BY revenue DESC
""", conn)
print(product_rev.to_string(index=False))
print()

print("=" * 50)
print("3. ORDER STATUS DISTRIBUTION")
print("=" * 50)
status_dist = pd.read_sql_query("""
    SELECT 
        OrderStatus,
        COUNT(*) AS num_orders,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 2) AS percentage
    FROM orders
    GROUP BY OrderStatus
    ORDER BY num_orders DESC
""", conn)
print(status_dist.to_string(index=False))
print()

print("=" * 50)
print("4. HIGH-VALUE DELIVERED ORDERS (WHERE TotalPrice > 1000)")
print("=" * 50)
high_value = pd.read_sql_query("""
    SELECT 
        OrderID,
        Date,
        Product,
        Quantity,
        TotalPrice,
        PaymentMethod
    FROM orders
    WHERE OrderStatus = 'Delivered' AND TotalPrice > 1000
    ORDER BY TotalPrice DESC
    LIMIT 10
""", conn)
print(high_value.to_string(index=False))
print()

print("=" * 50)
print("5. MONTHLY SALES TREND (2023-2025)")
print("=" * 50)
monthly_trend = pd.read_sql_query("""
    SELECT 
        strftime('%Y-%m', Date) AS month,
        COUNT(*) AS num_orders,
        SUM(TotalPrice) AS revenue,
        ROUND(AVG(TotalPrice), 2) AS avg_order_value
    FROM orders
    GROUP BY month
    ORDER BY month
""", conn)
print(monthly_trend.to_string(index=False))
print()

print("=" * 50)
print("6. PAYMENT METHOD BREAKDOWN")
print("=" * 50)
payment_stats = pd.read_sql_query("""
    SELECT 
        PaymentMethod,
        COUNT(*) AS usage_count,
        SUM(TotalPrice) AS total_revenue,
        ROUND(AVG(TotalPrice), 2) AS avg_order_value
    FROM orders
    GROUP BY PaymentMethod
    ORDER BY total_revenue DESC
""", conn)
print(payment_stats.to_string(index=False))
print()
