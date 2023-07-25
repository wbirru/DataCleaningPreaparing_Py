#!/usr/bin/env python
# coding: utf-8

# # Task 1: Data Preparation
# 

# In[1]:


# Import pandas library
import pandas as pd


# In[2]:


import matplotlib.pyplot as plt


# In[3]:


# Load the data from the file NBA_players_stats.csv using pandas library.
NBA_players_P = "NBA_players_stats.csv"


# In[4]:


NBA_players = pd.read_csv(NBA_players_P, sep=',', decimal='.')


# In[5]:


# Checking whether the loaded data is equivalent to the data in the source CSV file
NBA_players.shape


# In[6]:


NBA_players.head(10)


# In[7]:


#Sanity Check 1
NBA_players.dropna().boxplot(column='PTS', by='Pos')
plt.show()


# In[8]:


#Sanity Check 2
NBA_players.dropna().boxplot(column='Age')
plt.show()


# In[9]:


# Sanity Check 3
NBA_players['PTS'].plot(kind='box')
plt.show()


# In[10]:


# Clean the data
# Removing white spaces
for column in NBA_players.columns: 
    NBA_players['Player'] = NBA_players['Player'].apply(lambda x: str(x).replace(' ', ''))
    NBA_players['Pos'] = NBA_players['Pos'].apply(lambda x: str(x).replace(' ', ''))
    NBA_players['Tm'] = NBA_players['Tm'].apply(lambda x: str(x).replace(' ', ''))


# In[11]:


# Rounding to three decimal places
NBA_players_rounded = NBA_players.round(decimals=3)


# In[12]:


# Displaying information about the NBA players dataframe
NBA_players_rounded.info()


# In[13]:


# Cheking how many null values available in the NBA players dataframe
NBA_players_rounded.isnull().sum()


# In[14]:


# Fill all the empty/null values with 0 
NBA_players_Fill = NBA_players_rounded.fillna(0)


# In[15]:


# Cheking whether tha null values are replaced by 0 values
NBA_players_Fill.isnull().sum()


# In[16]:


# Replacing typos with correct column names 
NBA_players_Fill['Pos'] = NBA_players_Fill['Pos'].replace(['SGa', 'SF.', 'PFa', 'sf', 'Sf', 'pg', 'sg', 'Pg'], ['SG', 'SF', 'PF', 'SF', 'SF', 'PG', 'SG', 'PG'])
NBA_players_Fill['Pos'].str.upper()


# In[17]:


# Replacing impossible value in Age column
NBA_players_Fill['Age'] = NBA_players_Fill['Age'].replace([-19], 19)


# In[18]:


# Checking whether the error is fixed on not on index number 197
Y = NBA_players_Fill['Age']
Y [197]


# In[19]:


# Replacing impossible values in PTS as they are greater than 2000
NBA_players_Fill['PTS'] = NBA_players_Fill['PTS'].replace([20000, 28800], 0)


# In[20]:


#Checking the dataframe
NBA_players_Fill.head(10)


# In[21]:


#Saving the cleaned csv file into a new file
NBA_players_Fill.to_csv('cleaned_NBA_players_stats.csv', index=False)


# # Task 2: Data Exploration

# ## Task 2.1 
# Explore the players' total points: Please analyze the composition of the total points of the top five players with the most points.

# In[23]:


# Code goes after this line by adding cells


# In[24]:


# Analyzing the total points of the top five players
sorted_NBA_players = NBA_players_Fill.sort_values(by='PTS', ascending = False)


# In[25]:


sorted_NBA_players.head(10)


# In[26]:


# Composition of the total points of the top five players with the most points
Top_5_Most_PTS = sorted_NBA_players[0:5][['Player','2P','3P', '2PA', '3PA']]
Top_5_Most_PTS.reset_index(drop=True, inplace=True)


# In[27]:


Top_5_Most_PTS


# In[28]:


# Bar plot showing the composition of the total points of the top five players with the most points
Top_5_Most_PTS.plot.bar(stacked = True, title = 'The composition of the total points of the top five players with the most points', 
                    figsize = (8,6))


# ## Task 2.2 
# Assuming that the data collector makes an entry error when collecting data, it can be ensured that the error occurred in the 3P, 3PA and 3P% columns, but it is not sure which player's information the error lies on. Please try to explore the error by visualization to identify how many errors there are and try to fix it.
# 

# In[29]:


# Code goes after this line by adding cells


# In[30]:


# Ploting box plot for 3P column and checking outliers or impossible values
NBA_players_Fill['3P'].plot(kind='box')
plt.show()


# In[31]:


# Ploting box plot for 3PA column and checking outliers or impossible values
NBA_players_Fill['3PA'].plot(kind='box')
plt.show()


# In[32]:


# Ploting box plot for 3P% column and checking outliers or impossible values
NBA_players_Fill['3P%'].plot(kind='box')
plt.show()


# In[33]:


# Sorting the 3PA values to check the outliers 
sorted_3P_NBA_players = NBA_players.sort_values(by='3PA', ascending = False)


# In[34]:


# Displaying the three columns only to see thier sorted values 
sorted_3P_NBA_players[['3P', '3PA', '3P%']]


# In[35]:


# Replacing the 3P outliers with the mean value after calculating the mean
mean3P = sorted_3P_NBA_players['3P'].mean()


# In[36]:


mean3P


# In[37]:


sorted_3P_NBA_players['3P'] = sorted_3P_NBA_players['3P'].replace([169, 146, 140], mean3P)


# In[38]:


# Replacing the 3PA outliers with the mean value after calculating the mean
mean3PA = sorted_3P_NBA_players['3P'].mean()


# In[39]:


mean3PA


# In[40]:


sorted_3P_NBA_players['3PA'] = sorted_3P_NBA_players['3PA'].replace([411, 380, 370], mean3PA)


# In[41]:


# Cheking whether it is replaced by the meann value or not
sorted_3P_NBA_players[['3P', '3PA', '3P%']]


# ## Task 2.3 
# Please analyze the relationship between the player's total points and the rest features (columns). Please use at least three other columns.
# 

# In[42]:


# Code goes after this line by adding cells


# In[43]:


# Using the scatter matrix code to quickly observe the relationship between the features 
from pandas.plotting import scatter_matrix


# In[44]:


scatter_matrix(NBA_players_Fill,alpha=0.2,figsize=(29,29),diagonal='hist')
plt.show()


# In[45]:


# The relationship between PTS and Field Goals (FT) using scattered plot
NBA_players_Fill.plot(kind='scatter', x='PTS', y="FG")
plt.title ('Players Total Points (PTS) vs Feild Goals (FG)')
plt.xlabel('PTS')
plt.show()


# In[46]:


# The relationship between PTS and Feild Goals Attempts (FTG) using scattered plot
NBA_players_Fill.plot(kind='scatter', x='PTS', y="FGA")
plt.title ('Players Total Points (PTS) vs Feild Goals Attempts (FGA)')
plt.xlabel('PTS')
plt.show()


# In[47]:


# The relationship between PTS and Minutes Played (MP) using scattered plot
NBA_players_Fill.plot(kind='scatter', x='PTS', y="MP")
plt.title ('Players Total Points (PTS) vs Minutes Played (MP)')
plt.xlabel('PTS')
plt.show()


# In[ ]:




