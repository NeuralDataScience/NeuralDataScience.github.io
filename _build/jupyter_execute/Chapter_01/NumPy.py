#!/usr/bin/env python
# coding: utf-8

# # NumPy

# **NumPy** is a useful package that can help store and wrangle homogeneous data. "Homogenous" means that all data points within the data are of the same [data type](https://jakevdp.github.io/PythonDataScienceHandbook/02.01-understanding-data-types.html).
# 
# We strongly recommend working through the ["NumPy Quickstart Tutorial"](https://numpy.org/doc/stable/user/quickstart.html) for a more comprehensive introduction to NumPy. Here, we'll introduce some useful tools using the *NumPy* package to analyze large datasets.

# Before we can use NumPy, we need to import the package. We can also nickname the modules when we import them. The convention is to import `numpy` as `np`. 

# In[1]:


# Import packages
import numpy as np

# Use whos to see available modules
get_ipython().run_line_magic('whos', '')


# ## NumPy Arrays

# The basis of the NumPy package is the **array**. A NumPy array is similar to a list of lists or a grid of values. You can create a [NumPy array](https://numpy.org/doc/stable/reference/generated/numpy.array.html) from a list using `np.array()`, by reading in a file, or through functions built into the NumPy package such as such as `arange`, `linspace`, `empty`, etc.

# In[2]:


# Create a list 
list_1 = [2, 4, 6, 8, 10, 12]

# Store list as a numpy array 
array1 = np.array(list_1)
print(array1)


# What we have created is a one-dimensional array which is similar to a normal list. NumPy arrays however, can be multidimensional. If we input a list of lists into `np.array()`, the output would be a multidimensional array (i.e a grid/matrix).

# In[3]:


# Create a 2nd list 
list_2 = [1, 3, 5, 7, 9, 11]

# Store list of lists as a NumPy array 
my_array = np.array([list_1, list_2])
print(my_array)


# ## Accessing attributes of NumPy arrays

# We can return the shape and size of an array by using the attributes `size` and `shape`. The `shape` attribute returns a tuple for the number of rows and columns of an array. The `size` attribute returns the total number of values stored within an array. 

# In[4]:


print('My array has a shape of:')
print(my_array.shape)

print('\nMy array has a size of:')
print(my_array.size)


# Other attributes that might be of interest are `ndim` and `dtype` which  respectively return the number of dimensions of the array and the data types stored in the array. You can see the full list of ndarray attributes in the <a href = "https://numpy.org/doc/stable/reference/arrays.ndarray.html#array-attributes"> NumPy ndarray documentation</a>.

# In[5]:


print('My array dimensions:')
print(my_array.ndim)

print('\nMy array contains values of data type:')
print(my_array.dtype)


# ## Indexing & Slicing Arrays

# You can index NumPy arrays using `array_name[row,column]` to select a single value. If you omit the column, it will give you the entire row. You can also use `:` in place of either `row` or `column` to indicate you want to return all those values. We will demonstrate by indexing `my_array`. 

# In[6]:


# Select the number 6 from our array 
print('The value stored in row 1, column 3 is:')
print(my_array[0,2])

# Select the 2nd row from our array 
print('The values stored in row 2 are:')
print(my_array[1])


# You may want to look at a slice of columns or a slice of rows. You can slice your array like the following: `array(start_row:stop_row, start_col:end_col)`. 

# In[7]:


# Print the first 3 columns of each row 
print(my_array[: ,0:3])


# You can also select multiple, nonsequential columns by inputing a `list` as your `columns`. Lets try to index the first, third, and last column in `array1`.

# In[8]:


# Choose your columns of interest 
columns = [0, 2, -1]
print(my_array[:, columns])


# We can also change values in an array similar to how we would change values in a list. The syntax we use is `array[row,column] = new_desired_value`.

# In[9]:


# Change the entire first row of array1 to 100
my_array[0,:] = 100
print(my_array)


# For further explanation of how to index NumPy arrays, please visit the <a href = "https://numpy.org/doc/stable/reference/arrays.indexing.html"> NumPy indexing documentation</a>.

# ## Subsetting 

# We can also subet our original array to only include data that meets our criteria. We can think of this as *subsetting* the array by applying a condition to our array. The syntax for this would be `new_array = original_array[condition]`.

# In[10]:


# Reassign our original array 
my_array = np.array([list_1, list_2])

# Return only values greater than 5 from our array 
condition = (my_array > 5)
filtered_array = my_array[condition]
print(filtered_array)


# ## Benefits of Using Arrays 

# If you were trying to add the numbers of the two lists together, simply adding the lists would only append one list at the end of the other. However, if you add two NumPy arrays together, the values of both arrays will be summed. 

# In[11]:


# Add two lists together 
list_3 = [10, 20, 30, 40]
list_4 = [20, 40, 60, 80]
print(list_3 + list_4)
print('\n')

# Add two arrays together 
array_1 = np.array([10, 20, 30, 40])
array_2 = np.array([20, 40, 60, 80])
print(array_1 + array_2)


# Alternatively, you can use the `sum()` method to add all values in an array together. You can also specify whether you want to sum the values across rows or columns in a grid/matrix. If you specify you want to sum values in rows or columns, the output will be an array of the sums. 

# In[12]:


# Create a 2 by 3 array 
array_3 = np.array([[5, 10], [15, 20], [25, 30]])
print('Original array:\n', array_3)

# Sum all values in array 
print('\nArray sum: ', array_3.sum())

# Sum the values across columns
print('\nColumn sums: ', array_3.sum(axis = 0))

# Sum the values across rows
print('\nRow sums: ', array_3.sum(axis = 1))


# For a full list of array methods, please visit the <a href = "https://numpy.org/doc/stable/reference/arrays.ndarray.html#array-methods"> NumPy array methods documentation</a>. You can also visit the <a href = ""> NumPy Reference</a> for more information on functions, modules, and objects in NumPy. 

# ## NumPy also includes some very useful array generating functions:
# 
# * `arange`: like `range` but gives you a useful NumPy array, instead of an interator, and can use more than just integers)
# * `linspace` creates an array with given start and end points, and a desired number of points
# * `logspace` same as linspace, but in log.
# * `random` can create a random list (there are <a href="https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html">many different ways to use this</a>)
# * `concatenate` which can concatenate two arrays along an existing axis [<a href="https://docs.scipy.org/doc/numpy/reference/generated/numpy.concatenate.html">documentation</a>]
# * `hstack` and `vstack` which can horizontally or vertically stack arrays
# * `save` and `load` can allow you to store and load your arrays
# 
# Whenever we call these, we need to use whatever name we imported `numpy` as (here, `np`). We will demonstrate some of these functions below. For a full list of funtions used to create arrays, please visit the <a href = "https://numpy.org/doc/stable/reference/routines.array-creation.html"> NumPy array creation documentaion</a>.

# In[13]:


# When using linspace, both end points are included
print(np.linspace(0,147,10))


# In[14]:


# First array is  a list of 10 numbers that are evenly spaced, 
# and range from exactly 1 to 100
lin_array = np.linspace(1,100, 10)

# Second row is a list of 10 numbers that begin 
# at 0 and are exactly 10 apart
range_array = np.arange(0,100,10)

print('Linspace array: ', lin_array)
print('Range array: ', range_array)


# In[15]:


# Create an array that has two rows using np.vstack
# First row should be 'first_array'
# Second row should be 'second_array'
big_array = np.vstack([lin_array, range_array])
print(big_array)


# NumPy also has built in methods to save and load arrays: `np.save()` and `np.load()`. Numpy files have a .npy extension. See full documentation <a href="https://docs.scipy.org/doc/numpy/reference/generated/numpy.save.html">here</a>.

# In[16]:


# Save method takes arguments 'filename' and then 'array':
np.save('big_array',big_array)


# In[17]:


my_new_matrix = np.load('big_array.npy')
print(my_new_matrix)


# ## Additional Resources
# See the [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/02.00-introduction-to-numpy.html) for a more in depth exploration of NumPy, and of course, <a href = "https://numpy.org/doc/stable/contents.html#numpy-docs-mainpage">the original documentation</a>.
