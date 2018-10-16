#!/usr/bin/env python
# coding: utf-8

# # Capstone Project 1: MuscleHub AB Test

# ## Step 1: Get started with SQL

# In[2]:


from codecademySQL import sql_query


# ## Step 2: Get your dataset

# In[3]:


sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[4]:


sql_query('''
SELECT *
FROM fitness_tests
LIMIT 5
''')


# In[5]:


sql_query('''
SELECT *
FROM applications
LIMIT 5
''')


# In[6]:


sql_query('''
SELECT *
FROM purchases
LIMIT 5
''')


# In[7]:


df = sql_query('''
SELECT visits.first_name,
    visits.last_name,
    visits.gender,
    visits.email,
    visits.visit_date,
    fitness_tests.fitness_test_date,
    applications.application_date,
    purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests
    ON visits.first_name = fitness_tests.first_name AND
    visits.last_name = fitness_tests.last_name AND
    visits.email = fitness_tests.email
LEFT JOIN applications 
    ON visits.first_name = applications.first_name AND
    visits.last_name = applications.last_name AND
    visits.email = applications.email
LEFT JOIN purchases
    ON visits.first_name = purchases.first_name AND
    visits.last_name = purchases.last_name AND
    visits.email = purchases.email
WHERE visit_date >= '7-1-17'
''')


# In[8]:


print (df)

#df.head(10)


# ## Step 3: Investigate the A and B groups

# In[9]:


import pandas as pd
from matplotlib import pyplot as plt


# In[10]:


df['ab_test_group'] = df.fitness_test_date.apply(lambda x:
                                                'A' if pd.notnull(x) else 'B')


# In[30]:


ab_counts = df.groupby('ab_test_group').first_name.count()
#print (ab_counts)
plt.figure()
plt.figure(figsize=(7,3))
plt.pie(ab_counts, autopct='%0.2f%%')
plt.legend(['Group A', ' Group B'])
plt.axis('equal')
plt.title('Division of individuals per sample. Total: 5004')
plt.show()
plt.savefig('ab_test_pie_chart.png')


# ## Step 4: Who picks up an application?

# In[12]:


df['is_application'] = df.application_date.apply(lambda x:
                                                'Application' if pd.notnull(x) else 'No Application')


# In[13]:


df.head(10)


# In[14]:


app_counts = df.groupby(['is_application', 'ab_test_group']).first_name.count().reset_index()
print app_counts


# In[15]:


app_pivot = app_counts.pivot(
    columns = 'is_application',
    index = 'ab_test_group',
    values = 'first_name'
).reset_index()
app_pivot


# In[16]:


app_pivot['Total'] = app_pivot.Application + app_pivot['No Application']
app_pivot


# In[17]:


app_pivot['Percent with Application'] = app_pivot.Application / app_pivot.Total
                                     
app_pivot


# In[18]:


#performing a Chi Square Test
from scipy.stats import chi2_contingency


# In[19]:


X = [[250, 2254],
     [325, 2175]]

chi2, pval, dof, expected = chi2_contingency(X)
print pval
#if pval > 0.05 the difference is significant


# ## Step 4: Who purchases a membership?

# In[20]:


df['is_member'] = df.purchase_date.apply(lambda x:
                                                'Member' if pd.notnull(x) else 'Not Member')


# In[21]:


#df.head(10)


# In[22]:


just_apps = df[df.is_application == 'Application']


# Great! Now, let's do a `groupby` to find out how many people in `just_apps` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `member_pivot`.

# In[23]:


member_counts = just_apps.groupby(['is_member', 'ab_test_group']).first_name.count().reset_index()

#turnig it to a pivot table
member_pivot = member_counts.pivot(
    columns = 'is_member',
    index = 'ab_test_group',
    values = 'first_name'
).reset_index()

#adding Total
member_pivot['Total'] = member_pivot.Member + member_pivot['Not Member']

#adding Percent Purchase
member_pivot['Percent Purchase'] = member_pivot.Member / member_pivot.Total

member_pivot


# In[24]:


X = [[200, 50],
     [250, 75]]

chi2, pval, dof, expected = chi2_contingency(X)
print pval
#if pval > 0.05 the difference is significant


# In[25]:


final_member = df.groupby(['is_member', 'ab_test_group']).first_name.count().reset_index()

#turnig it to a pivot table
final_member_pivot = final_member.pivot(
    columns = 'is_member',
    index = 'ab_test_group',
    values = 'first_name'
).reset_index()

#adding Total
final_member_pivot['Total'] = final_member_pivot.Member + final_member_pivot['Not Member']

#adding Percent Purchase
final_member_pivot['Percent Purchase'] = final_member_pivot.Member / final_member_pivot.Total

final_member_pivot


# In[26]:


X = [[200, 2304],
     [250, 2250]]

chi2, pval, dof, expected = chi2_contingency(X)
print pval
#if pval > 0.05 the difference is significant


# ## Step 5: Summarize the acquisition funel with a chart

# We'd like to make a bar chart for Janet that shows the difference between Group A (people who were given the fitness test) and Group B (people who were not given the fitness test) at each state of the process:
# 
# Percent of visitors who apply
# Percent of applicants who purchase a membership
# Percent of visitors who purchase a membership
# Create one plot for each of the three sets of percentages that you calculated in app_pivot, member_pivot and final_member_pivot. Each plot should:
# 
# Label the two bars as Fitness Test and No Fitness Test
# Make sure that the y-axis ticks are expressed as percents (i.e., 5%)
# Have a title

# ### Percent of visitors who apply

# In[27]:


labels = ['Fitness Test', 'No Fitness Test']
visitors_apply = [0.09984, 0.13000]
ax = plt.subplot()
plt.bar(range(len(visitors_apply)), visitors_apply)
ax.set_xticks(range(len(visitors_apply)))
ax.set_xticklabels(labels)
plt.title("Percent of visitors who apply")
ax.set_yticks([0, 0.05, 0.10, 0.15])
ax.set_yticklabels(['0','5%', '10%', '15%'])
plt.show()
plt.savefig('visitors_apply.png')


# ### Percent of applicants who become members

# In[28]:


app_purchase = [0.800000, 0.769231]
ax = plt.subplot()
plt.bar(range(len(app_purchase)), app_purchase)
ax.set_xticks(range(len(app_purchase)))
ax.set_xticklabels(labels)
plt.title("Percent of applicants who become members")
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
ax.set_yticklabels(['0', '25%', '50%', '75%', '100%'])
plt.show()
plt.savefig('apps_purchase.png')


# ### Percent of visitors who become members

# In[29]:


visitors_apply = [0.079872, 0.100000]
ax = plt.subplot()
plt.bar(range(len(visitors_apply)), visitors_apply)
ax.set_xticks(range(len(visitors_apply)))
ax.set_xticklabels(labels)
plt.title("Percent of overall visitors who become members")
ax.set_yticks([0, 0.05 , 0.1, 0.15])
ax.set_yticklabels(['0', '5%' , '10%', '15%'])
plt.show()
plt.savefig('visitors_members.png')

