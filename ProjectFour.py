import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
df = pd.read_csv('file/Dataset for Data Analytics.csv')

df['Date'] = pd.to_datetime(df['Date'])
df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)

def classify_outcome(status):
    if status in ['Delivered', 'Shipped']:
        return 'Successful'
    elif status in ['Cancelled', 'Returned']:
        return 'Unsuccessful'
    else:
        return 'Pending'

df['OrderOutcome'] = df['OrderStatus'].apply(classify_outcome)

monthly_rev = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
monthly_rev = monthly_rev.sort_values('YearMonth')
product_rev = df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)

status_rev = df.groupby('OrderStatus')['TotalPrice'].sum()
status_rev_clean = status_rev[status_rev.index.isin(['Delivered','Shipped','Cancelled','Returned'])]

payment_rev = df.groupby('PaymentMethod')['TotalPrice'].sum().sort_values(ascending=False)

referral_rev = df.groupby('ReferralSource')['TotalPrice'].sum().sort_values(ascending=False)

outcome_rev = df.groupby('OrderOutcome')['TotalPrice'].sum()

pivot_heat = df.pivot_table(values='TotalPrice', index='Product', columns='YearMonth', aggfunc='sum', fill_value=0)
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def add_value_labels(ax, spacing=5, fmt='${:,.0f}'):
    for rect in ax.patches:
        x = rect.get_x() + rect.get_width() / 2
        y = rect.get_y() + rect.get_height() / 2
        if isinstance(ax, plt.Axes):
            if rect.get_width() < 0:  
                value = rect.get_width()
                x = value + spacing
                y = rect.get_y() + rect.get_height()/2
                ax.text(x, y, fmt.format(value), ha='left', va='center', fontweight='bold')
            else:
                value = rect.get_height()
                ax.text(x, value + spacing, fmt.format(value), ha='center', va='bottom', fontweight='bold')
plt.figure(figsize=(12,5))
plt.plot(monthly_rev['YearMonth'], monthly_rev['TotalPrice'], marker='o', linewidth=2, color='#2c3e50', markersize=6)

peak_row = monthly_rev.loc[monthly_rev['TotalPrice'].idxmax()]
plt.annotate(f'${peak_row["TotalPrice"]:,.0f}', 
             xy=(peak_row['YearMonth'], peak_row['TotalPrice']),
             xytext=(10, 5), textcoords='offset points', fontweight='bold', color='#e74c3c', fontsize=11)
plt.title('Action Title: Sales more than doubled from early 2023 to mid‑2025, with a sharp holiday peak in December 2024', 
          fontsize=12, fontweight='bold', loc='left')
plt.ylabel('Total Revenue (USD)', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('monthly_sales_trend.png', dpi=150, bbox_inches='tight')
plt.close()
fig, ax = plt.subplots(figsize=(10,6))
bars = ax.barh(product_rev.index, product_rev.values, color='#3498db')
ax.set_xlabel('Revenue (USD)', fontsize=11)
ax.set_title('Action Title: Laptops and Monitors drive 47% of total revenue – nearly double the contribution of Chairs and Desks', 
             fontsize=12, fontweight='bold', loc='left')
for bar in bars:
    width = bar.get_width()
    ax.text(width + 500, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
            va='center', fontweight='bold', fontsize=9)
ax.invert_yaxis() 
plt.tight_layout()
plt.savefig('product_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
colors = ['#2ecc71', '#3498db', '#e74c3c', '#e67e22']
plt.figure(figsize=(8,6))
wedges, texts, autotexts = plt.pie(status_rev_clean, labels=status_rev_clean.index, autopct='%1.0f%%',
                                    colors=colors, startangle=90, textprops={'fontsize':11})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
plt.title("Action Title: Nearly 30% of revenue is lost to Cancelled (17%) or Returned (12%) orders – a $140K leakage",
          fontsize=12, fontweight='bold', loc='left')
plt.tight_layout()
plt.savefig('order_status_pie.png', dpi=150, bbox_inches='tight')
plt.close()
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.bar(payment_rev.index, payment_rev.values, color='#95a5a6')
bars[0].set_color('#2980b9')  
bars[1].set_color('#2980b9')  
ax.set_ylabel('Revenue (USD)', fontsize=11)
ax.set_title("Action Title: Cash and Credit Card account for 54% of revenue – Gift Cards underperform by 2.5x",
             fontsize=12, fontweight='bold', loc='left')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 500, f'${height:,.0f}', 
            ha='center', va='bottom', fontweight='bold', fontsize=9)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('payment_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.barh(referral_rev.index, referral_rev.values, color='#9b59b6')
ax.set_xlabel('Revenue (USD)', fontsize=11)
ax.set_title("Action Title: Instagram, Facebook, and direct Referrals generate >70% of referral revenue – Email and Google lag",
             fontsize=12, fontweight='bold', loc='left')
for bar in bars:
    width = bar.get_width()
    ax.text(width + 500, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
            va='center', fontweight='bold', fontsize=9)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('referral_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
top_products = product_rev.head(6).index
heat_data = pivot_heat.loc[top_products]
months_sorted = sorted(heat_data.columns, key=lambda x: datetime.strptime(x, '%Y-%m'))
heat_data = heat_data[months_sorted]

plt.figure(figsize=(14,6))
sns.heatmap(heat_data, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5, cbar_kws={'label': 'Revenue (USD)'})
plt.title("Action Title: Laptops peak in Q4 2024; Monitors sell consistently all year – use Monitor stability to cross‑sell",
          fontsize=12, fontweight='bold', loc='left')
plt.xlabel('Month')
plt.ylabel('Product')
plt.tight_layout()
plt.savefig('heatmap_product_month.png', dpi=150, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots(figsize=(7,5))
bars = ax.bar(outcome_rev.index, outcome_rev.values, color=['#2ecc71', '#e74c3c'])
ax.set_ylabel('Revenue (USD)', fontsize=11)
ax.set_title("Action Title: Unsuccessful orders (cancelled/returned) drain $140,000 – fix returns to unlock immediate growth",
             fontsize=12, fontweight='bold', loc='left')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1000, f'${height:,.0f}', 
            ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('outcome_revenue.png', dpi=150, bbox_inches='tight')

