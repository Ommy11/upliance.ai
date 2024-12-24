#!/usr/bin/env python
# coding: utf-8

# In[78]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[45]:


user_details = pd.read_csv("Users_details.csv")
cooking_session = pd.read_csv("CookingSessions.csv")
order_details = pd.read_csv("OrderDetails.csv")

user_details


# In[46]:


cooking_session


# In[47]:


order_details


# ### Data cleaning

# In[48]:


# checking the missing values

print("User_details : ", user_details.isnull().sum())

print("Cooking_Session : ", cooking_session.isnull().sum())

print("Order_details : ", order_details.isnull().sum())


# In[49]:


# handling the missing values in the order details file

order_details = order_details.fillna(0)


# In[50]:


order_details


# In[52]:


# Ensure consistent data formats (convert dates if present)
order_details['Order Date'] = pd.to_datetime(order_details['Order Date'])
cooking_session['Session Start'] = pd.to_datetime(cooking_session['Session Start'])
cooking_session['Session End'] = pd.to_datetime(cooking_session['Session End'])


# In[53]:


cooking_session


# In[56]:


## merging the all data to create a dataset

merged_data = cooking_session.merge(order_details, on=['User ID', 'Dish Name'], how='inner')\
    .merge(user_details, on='User ID', how='inner')


# In[63]:


print("merged_data : \n\n" , merged_data)


# In[64]:


merged_data.head()


# In[65]:


## Analysing the analyzing the relationship between
##cooking sessions and user orders, identifying popular dishes, and exploring
#demographic factors that influence user behavior.


# In[70]:


#Analysing and identifying the popular dishes

popular_dishes = merged_data.groupby('Dish Name').agg({'Total Orders': 'sum'}).reset_index()


# In[69]:


popular_dishes


# In[96]:


## Visualiizing the popular dishes through bar chart

plt.figure(figsize=(8, 6))

sns.barplot(
    data=popular_dishes, 
    x='Dish Name', 
    y='Total Orders', 
    palette='viridis'  
)
plt.title('Popular Dishes Based on Total Orders')
plt.xlabel('Dish Name')
plt.ylabel('Total Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[73]:


## Analysing based on locations

demographic_analysis = merged_data.groupby(['Location', 'Dish Name']).agg({'Total Orders': 'sum'}).reset_index()


# In[74]:


demographic_analysis


# In[95]:


# visualising the dishes based on locations

location_distribution = merged_data.groupby('Location')['Total Orders'].sum()
plt.figure(figsize=(8, 6))
plt.pie(location_distribution, labels=location_distribution.index, autopct='%1.1f%%', startangle=140, colors=['lightcoral', 'lightskyblue'])
plt.title('Order Distribution by location')
plt.show()


# In[94]:


# detailed analysis of dishes by locations 

location_dish_distribution = merged_data.groupby(['Location', 'Dish Name'])['Total Orders'].sum().reset_index()

# Generate a color palette for the dishes
dishes = location_dish_distribution['Dish Name'].unique()
colors = sns.color_palette("husl", len(dishes))

# Prepare data for the nested pie chart
locations = location_dish_distribution['Location'].unique()
inner_labels = locations
inner_sizes = location_dish_distribution.groupby('Location')['Total Orders'].sum()

outer_labels = location_dish_distribution['Dish Name']
outer_sizes = location_dish_distribution['Total Orders']

# Plot the nested pie chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(inner_sizes, labels=inner_labels, radius=1, colors=sns.color_palette("pastel"), 
       wedgeprops=dict(width=0.3, edgecolor='w'), autopct='%1.1f%%', startangle=140)

ax.pie(outer_sizes, labels=outer_labels, radius=0.7, colors=colors, 
       wedgeprops=dict(width=0.3, edgecolor='w'))

plt.title('Order Distribution by Location and Dishes', fontsize=14)
plt.tight_layout()
plt.show()


# In[103]:


# Scatter plot for cooking duration vs order quantity

plt.figure(figsize=(8, 5))
plt.scatter(merged_data['Duration (mins)'], merged_data['Total Orders'], color='green')
plt.title('Cooking Duration vs Order Quantity')
plt.xlabel('Cooking Duration (mins)')
plt.ylabel('Order Quantity')
plt.grid(True)
plt.tight_layout()
plt.show()


# In[104]:


# Order Trends Over Time

order_trends = merged_data.groupby('Order Date').agg({'Total Orders': 'sum'}).reset_index()
plt.figure(figsize=(8, 5))
sns.lineplot(data=order_trends, x='Order Date', y='Total Orders', marker='o', color='purple')
plt.title('Order Trends Over Time', fontsize=14)
plt.xlabel('Order Date', fontsize=10)
plt.ylabel('Total Orders', fontsize=10)
plt.xticks(rotation=45)
plt.grid()
plt.show()


# In[ ]:




