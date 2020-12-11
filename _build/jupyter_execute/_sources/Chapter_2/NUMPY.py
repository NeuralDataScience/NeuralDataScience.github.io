#!/usr/bin/env python
# coding: utf-8

# # NUMPY 

# In this chapter we will be discussing the advatages to using the *numpy* package to analyze large datasets. Numpy is a python module that contains many funtions and methods that can be used to wrangle large datasets in order to make them easier to visualize, simpler to work with, and easier to extract information out o the data. 

# In order to work with the funtions in pandas, you must first import the pandas module to your local computer as so:

# In[1]:


import numpy as np


# In the cell below, three lists have been created: a list of even numbers, a list of prime numbers, and a third list which is a list of lists (lol). 

# In[2]:


list1 = [2, 4, 6, 8]
list2 = [1, 3, 5, 7]
list3 = [list1, list2]
print(list1)
print(list2)
print(list3)


# The list of lists format is not wrong per say, but it makes working with the data more difficult. For example, if you were trying to add the numbers of the two lists together, simply adding the lists would only append the two lists together. 

# In[3]:


print(list1 + list2)


# Instead you would have to create a loop that loops through each variable in each list. This gets even more tideous and harder to visualize when you have a large amount of data/lists.

# In[4]:


for a,b in zip(list1, list2):
    print(a+b)


# ## Numpy Arrays

# In[5]:


array1 = np.array([list1, list2])
array1


# In[6]:


print(array1.sum())
print(array1.sum(axis = 0))
print(array1.sum(axis = 1))

