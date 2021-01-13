#!/usr/bin/env python
# coding: utf-8

# # NumPy

#  NumPy is a useful package that can help store and wrangle homogeneous data. This means data that the data are of the same [data type](https://jakevdp.github.io/PythonDataScienceHandbook/02.01-understanding-data-types.html) such as all **floats** or all **integers**.
# 
# We strongly recommend working through the ["NumPy Quickstart Tutorial"](https://numpy.org/doc/stable/user/quickstart.html) for a more comprehensive introduction to NumPy. Here, we'll introduce some useful tools using the *NumPy* package to analyze large datasets.

# Before we can use NumPy, we need to import the package. We can also nickname the modules when we import them. The convention is to import `numpy` as `np`. 

# In[1]:


# Import packages
import numpy as np

# Use whos 'magic command' to see available modules
get_ipython().run_line_magic('whos', '')


# ## NumPy Arrays

# The basis of the NumPy package is the **array**. A NumPy array is similar to a list of lists or a grid of values. You can create a [NumPy array](https://numpy.org/doc/stable/reference/generated/numpy.array.html) from a list using `np.array()`, by reading in a file, or through functions built into the NumPy package such as such as `arange`, `linspace`, `empty`, which we will discuss later. 

# In[2]:


# Create a random list 
list1 = [2, 4, 6, 8, 10, 12]

# Store list as a numpy array 
array1 = np.array(list1)
print(array1)


# What we have created is a one-dimensional array which is similar to a normal list. NumPy arrays however, can be multidimensional. If we input a list of lists into `np.array()`, the output would be a multidimensional array (i.e a grid/matrix).

# In[3]:


# Create a 2nd random list 
list2 = [1, 3, 5, 7, 9, 11]

# Store list of lists as a NumPy array 
array1 = np.array([list1, list2])
print(array1)


# ## Accessing attributes of NumPy arrays

# We can return the shape and size of an arry either by looking at the attribute of the array, or by using the `shape()` and `size()` functions. The `shape` attribute returns a tuple for the number of rows and columns of an array. The `size` attribute returns the total number of values stored within an array. 

# In[4]:


print('Array1 has a shape of:')
print(array1.shape)

print('\nArray1 has a size of:')
print(array1.size)


# Other attributes that might be of interest are `ndim` and `dtype` which  respectively return the number of dimensions of the array and the data types stored in the array. You can see the full list of ndarray attributes in the <a href = "https://numpy.org/doc/stable/reference/arrays.ndarray.html#array-attributes"> NumPy ndarray documentation</a>.

# In[5]:


print('Array1 dimensions:')
print(array1.ndim)

print('\nArray1 contains values of data type:')
print(array1.dtype)


# ## Indexing & Slicing Arrays

# You can index NumPy arrays using `array_name[row,column]` to select a single value. If you omit the column, it will give you the entire row. You can also use `:` for either row or column and it will return all of those values. We will demonstrate by indexing into `array1`. 

# In[6]:


# Select the number 6 from our array 
print('The value stored in row 1, column 3 is:')
print(array1[0,2])

# Select the 2nd row from our array 
print('The values stored in row 2 are:')
print(array1[1])


# You may want to look at a slice of columns or a slice of rows. You can do so using `array(start_index:stop_index)` for either row or columns to select your slice.

# In[7]:


# Print the first 3 columns of each row 
print(array1[: ,0:3])


# You can also select multiple specifc columns by inputing a `list` as your `columns`. Lets try to index the first, third, and last column in `array1`.

# In[8]:


# Choose your columns of interest 
columns = [0, 2, -1]
print(array1[:, columns])


# We can also change values in an array similar to how we would change values in a list. The syntax we use is `array[row,column] = new_desired_value`.

# In[9]:


# Change the entire first row of array1 to 100
array1[0,:] = 100
print(array1)


# For further explanation of how to index Numpy arrays, please visit the <a href = "https://numpy.org/doc/stable/reference/arrays.indexing.html"> NumPy indexing documentation</a>.

# ## Subsetting 

# We can also subet our original array to only include data that meets our criteria. We can think of this as *filtering* the array by applying a condition to our array. The syntax for this would be `new_array = original_array[condition]`.

# In[10]:


# Reassign our original array 
array1 = np.array([list1, list2])

# Return values greater than 5 from our array 
condition = (array1 > 5)
filtered_array = array1[condition]
print(filtered_array)


# ## Benefits of Using Arrays 

# The list of lists format is not wrong per say, but it makes working with the data more difficult. For example, if you were trying to add the numbers of the two lists together, simply adding the lists would only append one list at the end of the other. However, if you add two NumPy arrays together, the values of both arrays will be summed. 

# In[11]:


# Add two lists together 
list3 = [10, 20, 30, 40]
list4 = [20, 40, 60, 80]
print(list3 + list4)
print('\n')

# Add two arrays together 
array2 = np.array([10, 20, 30, 40])
array3 = np.array([20, 40, 60, 80])
print(array2 + array3)


# Alternitavely, you can use the `sum()` method to add all values in an array together. You can also specify whether you want to sum the values across rows or columns in a grid/matrix. If you specify you want to sum values in rows or columns, the output will be an array of the sums. 

# In[12]:


# Create a 2 by 3 array 
array4 = np.array([[5, 10], [15, 20], [25, 30]])
print('array4:')
print(array4)
print('\n')

# Sum all values in array 
print('Array sum')
print(array4.sum())
print('\n')

# Sum the values across columns
print('Column sums')
print(array4.sum(axis = 0))
print('\n')

# Sum the values across rows
print('Row sums')
print(array4.sum(axis = 1))


# For a full list of array methods, please visit the <a href = "https://numpy.org/doc/stable/reference/arrays.ndarray.html#array-methods"> NumPy array methods documentation</a>. You can also visit the <a href = ""> NumPy Reference</a> for more information on functions, modules, and objects in NumPy. 

# ## NumPy also includes some very useful array generating functions:
# 
# * `arange`: like `range` but gives you a useful NumPy array, instead of an interator, and can use more than just integers)
# * `linspace` creates an array with given start and end points, and a desired number of points
# * `logspace` same as linspace, but in log.
# * `random` can create a random list (there are <a href="https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html">many different ways to use this</a>)
# * `concatenate` which can concatenate two arrays along an existing axis [<a href="https://docs.scipy.org/doc/numpy/reference/generated/numpy.concatenate.html">documentation</a>]
# * `hstack` and `vstack` which can horizontally or vertically stack arrays
# 
# Whenever we call these, we need to use whatever name we imported `numpy` as (here, `np`). We will demonstrate some of these functions below. For a full list of funtions used to create arrays, please visit the <a href = "https://numpy.org/doc/stable/reference/routines.array-creation.html"> NumPy array creation documentaion</a>.

# In[13]:


# When using linspace, both end points are included
print(np.linspace(0,147,10))


# In[14]:


# First array is  a list of 10 numbers that are evenly spaced, 
# and range from exactly 1 to 100
first_array = np.linspace(1,100, 10)

# Second row is a list of 10 numbers that begin 
# at 0 and are exactly 10 apart
second_array = np.arange(0,100,10)

print(first_array)
print(second_array)


# In[15]:


# Create an array that has two rows 
# First row should be 'first_array'
# Second row should be 'second_array'
big_array = np.vstack([first_array, second_array])
print(big_array)


# Numpy also has built in methods to save and load arrays: `np.save()` and `np.load()`. Numpy files have a .npy extension. See full documentation <a href="https://docs.scipy.org/doc/numpy/reference/generated/numpy.save.html">here</a>.

# In[16]:


# Save method takes arguments 'filename' and then 'array':
np.save('big_array',big_array)


# In[17]:


my_new_matrix = np.load('big_array.npy')
print(my_new_matrix)


# ## Additional Resources
# See the [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/02.00-introduction-to-numpy.html) for a more in depth exploration of NumPy, and of course, <a href = "https://numpy.org/doc/stable/contents.html#numpy-docs-mainpage">the original documentation</a>.

# In[ ]:




