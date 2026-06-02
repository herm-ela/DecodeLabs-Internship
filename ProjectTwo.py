import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

possible_paths = [
    "Dataset for Data Analytics project 2.csv",
    "file/Dataset for Data Analytics project 2.csv",
    "Dataset for Data Analytics (1).xlsx",
    "file/Dataset for Data Analytics (1).xlsx"
]

df = None
used_path = None

for path in possible_paths:
    if os.path.exists(path):
        if path.endswith('.csv'):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path, sheet_name=0)
        used_path = path
        break

if df is None:
    print("ERROR: Data file not found. Current directory contents:")
    for f in os.listdir('.'):
        print("  -", f)
    exit(1)

print("="*60)
print("EXPLORATORY DATA ANALYSIS - PROJECT 2")
print("="*60)
print("Loaded from:", used_path)
print("Rows:", df.shape[0], " Columns:", df.shape[1])
print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())
df = df.dropna(subset=['TotalPrice'])

if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])


num_cols = ['Quantity', 'UnitPrice', 'TotalPrice']
num_cols = [c for c in num_cols if c in df.columns]

stats = df[num_cols].describe().T
stats['median'] = df[num_cols].median()
stats = stats[['count', 'mean', 'median', 'min', 'max']]

print("\n" + "="*60)
print("BASIC STATISTICS")
print("="*60)
print(stats.round(2))

def iqr_outliers(data, col):
    q1 = data[col].quantile(0.25)
    q3 = data[col].quantile(0.75)
    iqr = q3 - q1
    lb = q1 - 1.5*iqr
    ub = q3 + 1.5*iqr
    out = data[(data[col] < lb) | (data[col] > ub)]
    return out, lb, ub

outliers, lb, ub = iqr_outliers(df, 'TotalPrice')
print("\n" + "="*60)
print("OUTLIERS (IQR METHOD)")
print("="*60)
print("Lower bound: {:.2f}".format(lb))
print("Upper bound: {:.2f}".format(ub))
print("Number of outliers:", len(outliers))
if len(outliers) > 0:
    print("Sample outliers:")
    cols = ['OrderID', 'Product', 'Quantity', 'TotalPrice']
    cols = [c for c in cols if c in outliers.columns]
    print(outliers[cols].head())

if 'Product' in df.columns:
    prod_avg = df.groupby('Product')['TotalPrice'].mean().sort_values(ascending=False)
    print("\n" + "="*60)
    print("AVERAGE ORDER VALUE BY PRODUCT")
    print("="*60)
    print(prod_avg.round(2))

    plt.figure(figsize=(10,5))
    prod_avg.plot(kind='bar', color='skyblue')
    plt.title('Average Order Value by Product')
    plt.ylabel('Rupees')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('product_trend.png')
    plt.show()

corr_val = 0
if 'Quantity' in df.columns and 'TotalPrice' in df.columns:
    corr_val = df['Quantity'].corr(df['TotalPrice'])
    print("\nCorrelation Quantity vs TotalPrice: {:.3f}".format(corr_val))

    plt.figure(figsize=(8,6))
    plt.scatter(df['Quantity'], df['TotalPrice'], alpha=0.4)
    plt.title('Quantity vs TotalPrice (r = {:.2f})'.format(corr_val))
    plt.xlabel('Quantity')
    plt.ylabel('TotalPrice')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('scatter.png')
    plt.show()

plt.figure(figsize=(12,5))
plt.hist(df['TotalPrice'], bins=50, edgecolor='black', alpha=0.7, color='green')
plt.axvline(df['TotalPrice'].mean(), color='red', linestyle='--', label='Mean: {:.2f}'.format(df['TotalPrice'].mean()))
plt.axvline(df['TotalPrice'].median(), color='blue', linestyle='--', label='Median: {:.2f}'.format(df['TotalPrice'].median()))
plt.title('Distribution of TotalPrice')
plt.xlabel('TotalPrice')
plt.legend()
plt.tight_layout()
plt.savefig('histogram.png')
plt.show()

plt.figure(figsize=(10,4))
sns.boxplot(x=df['TotalPrice'], color='lightcoral')
plt.title('Boxplot of TotalPrice')
plt.tight_layout()
plt.savefig('boxplot.png')
plt.show()

if 'OrderStatus' in df.columns:
    status_counts = df['OrderStatus'].value_counts()
    print("\n" + "="*60)
    print("ORDER STATUS DISTRIBUTION")
    print("="*60)
    print(status_counts)

    plt.figure(figsize=(8,5))
    status_counts.plot(kind='bar', color='purple')
    plt.title('Orders by Status')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('order_status.png')
    plt.show()

mean_val = df['TotalPrice'].mean()
median_val = df['TotalPrice'].median()
out_count = len(outliers)
if 'Product' in df.columns and len(prod_avg) > 0:
    top_prod = prod_avg.index[0]
    top_val = prod_avg.iloc[0]
else:
    top_prod = "N/A"
    top_val = 0

print("\n" + "="*70)
print("EDA SUMMARY REPORT")
print("="*70)
print("1. PROBLEM STATEMENT")
print("   Understand order value patterns, detect outliers, find top products.")
print()
print("2. METHODOLOGY")
print("   - Loaded {} orders.".format(df.shape[0]))
print("   - Mean, median, min, max calculated.")
print("   - Outliers detected using IQR (1.5*IQR rule).")
print("   - Product-wise average order value computed.")
print("   - Pearson correlation between Quantity and TotalPrice.")
print()
print("3. KEY FINDINGS")
print("   - Average TotalPrice: Rs. {:.2f}".format(mean_val))
print("   - Median TotalPrice: Rs. {:.2f}".format(median_val))
print("   - Mean > Median -> right-skewed (few large orders).")
print("   - Number of outlier orders: {}".format(out_count))
print("   - Top product by avg order value: {} (Rs. {:.2f})".format(top_prod, top_val))
print("   - Correlation (Quantity vs TotalPrice): {:.3f}".format(corr_val))
print()
print("4. RECOMMENDATIONS")
print("   - Investigate outlier orders for errors or bulk buyers.")
print("   - Focus marketing on {}.".format(top_prod))
print("   - Monitor order status for high cancellation/return rates.")
print()
print("5. VISUALS GENERATED")
print("   - product_trend.png")
print("   - scatter.png")
print("   - histogram.png")
print("   - boxplot.png")
if 'OrderStatus' in df.columns:
    print("   - order_status.png")
print("="*70)
print("Plots saved as PNG files.")
print("="*60)
