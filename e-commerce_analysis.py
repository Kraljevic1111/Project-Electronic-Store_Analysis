import pandas as pd 

customers = [
    {"customer_id": 1, "name": "Ana", "city": "Beograd"},
    {"customer_id": 2, "name": "Marko", "city": None},
    {"customer_id": 3, "name": "Jelena", "city": "Niš"},
    {"customer_id": 4, "name": "Petar", "city": "Novi Sad"},
]

orders = [
    {"order_id": 101, "customer_id": 1, "category": "Laptop", "price": 900, "quantity": 1, "date": "2024-01-05"},
    {"order_id": 102, "customer_id": 2, "category": "Phone", "price": None, "quantity": 1, "date": "2024-01-10"},
    {"order_id": 103, "customer_id": 1, "category": "Accessories", "price": 50, "quantity": 2, "date": "2024-02-01"},
    {"order_id": 104, "customer_id": 3, "category": None, "price": 700, "quantity": 1, "date": "2024-02-15"},
    {"order_id": 105, "customer_id": 4, "category": "Laptop", "price": 1100, "quantity": None, "date": "2024-03-01"},
    {"order_id": 105, "customer_id": 4, "category": "Laptop", "price": 1100, "quantity": None, "date": "2024-03-01"},
    {"order_id": 106, "customer_id": 2, "category": "Accessories", "price": 40, "quantity": 3, "date": "2024-03-10"},
]

df_customers = pd.DataFrame(customers)
df_orders = pd.DataFrame(orders)

df = pd.merge(df_customers,df_orders,on = "customer_id")
print(df)

#popunjavanje nedostajucih vrednosti 

df['quantity'] = df['quantity'].fillna(1)

avg_price = df['price'].mean()

df['price'] = df['price'].fillna(avg_price)

df['category'] = df['category'].fillna('Unknown')

df['city'] = df['city'].fillna("Unknown")

# uklannjane duplikata 

df = df.drop_duplicates()

print(df)

#konvertovanje date u datetime i dodavanje kolone month

df['date'] = pd.to_datetime(df['date'])

df['month'] = df['date'].dt.month



#dodavanje kolone revenue
df['revenue'] = df['price'] * df['quantity']

print(df)

#ukupan revenue 

total_revenue = df['revenue'].sum()
print("Total revenue:", "$",total_revenue)

#revenue po kategoriji

revenue_per_category = df.groupby('category')['revenue'].sum().reset_index()
print('Revenue per category:',revenue_per_category)

#revenue po gradu

revenue_per_city = df.groupby('city')['revenue'].sum().reset_index()
print('Revenue per city:',revenue_per_city)


# top customer

top_customer = df.groupby('name')['revenue'].sum().sort_values(ascending = False).head(1)
print('Top customer:',top_customer)

#revenue po mesecu

revenue_per_month = df.groupby('month')['revenue'].sum().reset_index()
print("Revenue per month:",revenue_per_month)

#bar chart revenue po kategoriji 

import matplotlib.pyplot as plt
import seaborn as sns 

plt.figure(figsize=(10,6))
sns.barplot(data = revenue_per_category,x = "revenue",y = "category",hue = 'category')
plt.title('Revenue per category')
plt.xlabel('Revenue')
plt.ylabel('Category')
plt.tight_layout()
plt.show()

#revenue po mesecima 

plt.figure(figsize = (10,6))
sns.lineplot(data = revenue_per_month,x = 'month',y = 'revenue',color = "blue")
plt.title('Revenue per month')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.tight_layout()
plt.grid()
plt.show()

#revenu po gradu pie chart 

plt.figure(figsize = (9,6))
plt.pie(revenue_per_city['revenue'],labels = revenue_per_city['city'],autopct="%1.1f%%",startangle=90)
plt.title('Revene per city')
plt.show()