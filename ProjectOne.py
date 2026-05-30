import pandas as pd
df = pd.read_csv('file/Dataset for Data Analytics.csv')
print("\nMissing values per column:\n", df.isnull().sum())

change_log = []

df['CouponCode'] = df['CouponCode'].fillna("None")
df['CouponCode'] = df['CouponCode'].replace("", "None")
# Add this action to our change log
change_log.append(["CR001", "Fill missing CouponCode", "Replaced empty/NaN with 'None'", "Resolved"])

if df['TrackingNumber'].isnull().sum() > 0:
    df['TrackingNumber'].fillna("Unknown", inplace=True)
    change_log.append(["CR002", "Fill missing TrackingNumber", "Replaced NaN with 'Unknown'", "Resolved"])

if df['PaymentMethod'].isnull().sum() > 0:
    mode_pay = df['PaymentMethod'].mode()[0]
    df['PaymentMethod'].fillna(mode_pay, inplace=True)
    change_log.append(["CR003", "Fill missing PaymentMethod", f"Used mode: {mode_pay}", "Resolved"])
print("\nMissing values after fix:\n", df.isnull().sum())
duplicate_orders = df.duplicated(subset=['OrderID']).sum()
if duplicate_orders > 0:
    # Keep first occurrence, delete the rest
    df.drop_duplicates(subset=['OrderID'], keep='first', inplace=True)
    change_log.append(["CR004", "Remove duplicate OrderID", f"Removed {duplicate_orders} duplicates", "Resolved"])
full_dupes = df.duplicated().sum()
if full_dupes > 0:
    df.drop_duplicates(inplace=True)
    change_log.append(["CR005", "Remove full row duplicates", f"Removed {full_dupes} rows", "Resolved"])
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
change_log.append(["CR006", "Standardize date format", "Converted to YYYY-MM-DD", "Resolved"])
text_cols = ['CustomerID', 'Product', 'ShippingAddress', 'PaymentMethod',
             'OrderStatus', 'CouponCode', 'ReferralSource']
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()
change_log.append(["CR007", "Clean text columns", "Trimmed spaces & applied title case", "Resolved"])
df['UnitPrice'] = df['UnitPrice'].round(2)
df['TotalPrice'] = df['TotalPrice'].round(2)
change_log.append(["CR008", "Round prices to 2 decimals", "UnitPrice & TotalPrice", "Resolved"])
calculated_total = df['Quantity'] * df['UnitPrice']
mismatch = (df['TotalPrice'] - calculated_total).abs() > 0.01
if mismatch.any():
    df.loc[mismatch, 'TotalPrice'] = calculated_total[mismatch]
    change_log.append(["CR009", "Fix incorrect TotalPrice",
  f"Corrected {mismatch.sum()}" f" rows where TotalPrice != Quantity*UnitPrice", "Resolved"])

print("\nAfter cleaning:")
print(df.info())
print("\nAny duplicates left?", df.duplicated().sum())
print("\nAny missing values left?", df.isnull().sum().sum())

df.to_csv("cleaned_orders.csv", index=False)
print("\n Cleaned data saved as 'cleaned_orders.csv'")



