#!/usr/bin/env python
# coding: utf-8

# # Pandas 

# In this chapter we will be discussing the advatages to using the *Pandas* package to analyze large datasets. While NumPy is a useful package, it can only be used with data of the same datatype. [Pandas](https://pandas.pydata.org/docs/user_guide/index.html#user-guide), however, is a package that helps us manipulate and analyze heterogenous data.
# 
# We strongly recommend looking at ["10 minutes to pandas"](https://pandas.pydata.org/docs/user_guide/10min.html) for a broader overview, but here we'll introduce the main concepts needed for the activities in this textbook.

# Before we can use pandas, we need to import it. We can also nickname the modules when we import them. The convention is to import `pandas` as `pd`. 

# In[1]:


# Import packages
import pandas as pd

# Use whos 'magic command' to see available modules
get_ipython().run_line_magic('whos', '')


# ## Create and Manipulate Dataframes 
# The two data structures of Pandas are the `Series` and the `DataFrame`. A `Series` is a one-dimensional onject similar to a list. A `DataFrame` can be thought of as a two-dimensional numpy array or a collection of `Series` objects. Series and dataframes can contain multiple different data types such as integers, strings, and floats, similar to an Excel spreadsheet. Pandas also supports `string` lables unlike numpy arrays which only have numeric labels for their rows and columns. For a more in depth explanation, please visit the [Introduction to Data Structures](https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html) section in the Pandas User Guide. 
# 
# You can create a Pandas dataframe by inputting dictionaries into the Pandas function `pd.DataFrame()`, by reading files, or through functions built into the Pandas package. The function [`pd.read_csv()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) reads a comma-seperated file and returns it as a `dataframe`.
# 
# 
# ### DataFrame example
# Below we will create a dataframe by reading the file `brainarea_vs_genes_exp_w_reannotations.tsv` which contains information on gene expression accross multiple brain areas. 
# 
# >**About this dataset:**
# This dataset was created by Derek Howard and Abigail Mayes for the purpose of accelerating advances in data mining of open brain transcriptome data for polygenetic brain disorders. The data comes from normalized microarray datasets of gene expression from 6 adult human brains that was released by the Allen Brain Institute and then processed into the dataframe we will see below. For more information on this dataset please visit the <a href = "https://github.com/derekhoward/HBAsets"> HBAsets repository</a>. 

# In[2]:


# Read in the list of lists as a data frame
file_name = 'brainarea_vs_genes_exp_w_reannotations.tsv'
gene_df = pd.read_csv(file_name, sep='\t')

# '.head()' returns the first 5 rows in the dataframe
gene_df.head()


# At the moment, our rows and columns don't have any useful information -- they're simply a list of indices. We can reassign the row values by using the method `set_index()`. We can choose any column in our present dataframe to be the row values. Let's assign the row lables to be the `gene_symbol` and reassign the dataframe. 

# In[3]:


row_index = 'gene_symbol'
gene_df = gene_df.set_index(row_index)
gene_df.head()


# It would help to know what information is in our dataset. In other words, what is across the columns at the top? We can get a list by accessing the `columns` attribute. 

# In[4]:


# Access the columns of our dataframe 
gene_df_columns = gene_df.columns 
gene_df_columns


# ## Indexing Dataframes

# Indexing in Pandas works slightly different than in NumPy. Similar to a dictionary, we can index dataframes by their names. 
# 
# The syntax for indexing single locations in a dataframe is `dataframe.loc[row_label,column_label]`. To index an individual column, we use the shorthand syntax `dataframe.[column_label]`. To index an individual row, we use the syntax `dataframe.loc[row_label]`. To index by index #, we use the syntax `dataframe.iloc[index_number]`. Below are some examples on how to access rows, columns, and single values in our dataframe. For more information on indexing dataframes, visit the <a href = "https://pandas.pydata.org/docs/user_guide/indexing.html#indexing"> "Indexing and selecting data"</a> section in the Pandas User Guide.

# In[5]:


# Select a single column
column = 'CA1 field'
print('Gene expression values in CA1 field:')
gene_df[column]


# In[6]:


# Select a single row
row = 'A1BG'
print('Gene expression of ', row, ' across brain regions:')
gene_df.loc[row]


# In[7]:


# Select an individual value 
print('Gene expression of A1BG in CA1 field:')
gene_df.loc[row, column]


# To select multiple different columns, you can use a `list` of all your columns of interest as so:

# In[8]:


# Select multiple columns
print('Gene expression values in multiple regions :')
columns = ['CA1 field', 'CA3 field', 'Crus I, lateral hemisphere']
gene_df[columns]


# ## Subsetting 

# Like NumPy arrays, we can subset our original dataframe to only include data that meets our criteria. Our dataframe has data on multiple different brain areas with many gene expression values. You can filter this dataframe using the following syntax:
# ```
# new_df = original_df[original_df['Column of Interest'] == 'Desired Value']
# ```
# In plain english, what this is saying is: save a dataframe from the original dataframe, where the original dataframe values in my Column of Interest are equal to my Desired Value. For more information on subsetting,  visit the <a href = "https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html"> "How do I select a subset of a DataFrame"</a> section in the Pandas documentation. 
# 
# Below we will demonstrate how to execute this by taking a look at the `CA1 field` column in `gene_df`. We will create a dataframe from `gene_df` that only contains genes that showed a certain level of gene expression. 

# In[9]:


# Create a dataframe with only genes that have an expression 
# value greater than 1.7 in 'CA1 field' 
desired_column = 'CA1 field'
desired_value = 1.7
new_gene_df = gene_df[gene_df[desired_column] > desired_value]
new_gene_df.head()


# ## DataFrame Methods

# Pandas has many useful methods that you can use on your data, including `describe`, `mean`, and more. To learn more about all the different methods that can be used to manipulate and analyze dataframes, please visit the <a href = "https://pandas.pydata.org/docs/user_guide/index.html"> Pandas User Guide </a>. We will demonstrate some of these methods below. 

# The `describe` method returns descriptive statistics of all the columns in our dataframe. 

# In[10]:


gene_df.describe()


# The `mean` and `std` method return the mean and standard deviation of each column in the dataframe, respectfully. 

# In[11]:


gene_df.mean()


# In[12]:


gene_df.std()


# Let's say we have two different dataframes and we would like to combine the two into one single dataframe. We can use either the `merge` or `join` Pandas methods in order to pull all of this data into one dataframe. 
# 
# ![](http://www.datasciencemadesimple.com/wp-content/uploads/2017/09/join-or-merge-in-python-pandas-1.png)
# 
# There are different types of joins/merges you can do in Pandas, illustrated <a href="http://www.datasciencemadesimple.com/join-merge-data-frames-pandas-python/">above</a>. Here, we want to do an **inner** merge, where we're only keeping entries with indices that are in both dataframes. We could do this merge based on columns, alternatively.
# 
# **Inner** is the default kind of join, so we do not need to specify it. And by default, join will use the 'left' dataframe, in other words, the dataframe that is executing the `join` method.
# 
# If you need more information, look at the <a href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html">join</a> and <a href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html">merge</a> documentation: you can use either of these to unite your dataframes, though join will be simpler!

# Below is an example of how to join two separate dataframe into one, unified dataframe. We start with one dataframe with only entries from the *temporal pole* and another dataframe with only entries from the CA fields of the hippocampus. We can then join the two dataframes together using the syntax `unified_df = df_1.join(df_2)`

# In[13]:


# Dataframe w/ only Temporal Pole entries 
temporal_pole_df = gene_df[['temporal pole, inferior aspect', 
                            'temporal pole, medial aspect', 
                            'temporal pole, superior aspect']]
temporal_pole_df.head()


# In[14]:


# Dataframe w/ only CA field entries 
CA_field_df = gene_df[['CA1 field', 
                       'CA2 field', 
                       'CA3 field', 
                       'CA4 field']]
CA_field_df.head()


# In[17]:


#Join the two dataframes
df_1 = temporal_pole_df
df_2 = CA_field_df

unified_df = df_1.join(df_2)
unified_df.head()


# Those are the basics of working with Pandas dataframes! Circle back to this page or the resources linked within if you ever need a refresher. Next, we'll talk about the power of SciPy for scientific analysis in Python.
# 
# ## Additional resources
# See the [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/03.00-introduction-to-pandas.html) for a more in depth exploration of Pandas, and of course, the [Pandas documentation](https://pandas.pydata.org/docs/user_guide/index.html).
