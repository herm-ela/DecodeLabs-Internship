import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

df = pd.read_csv('file/Dataset for Data Analytics project 2.csv')

print("="*60)
print("="*60)
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

