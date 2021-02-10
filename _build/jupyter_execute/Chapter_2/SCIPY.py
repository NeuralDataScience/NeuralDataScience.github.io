#!/usr/bin/env python
# coding: utf-8

# # SciPy

# ## What is SciPy

# SciPy stands for (Sci)entific (Py)thon. It is an open-source Python library that contains modules for scientific computing such as linear algrbra, optimization, image/signal processing,, statistics, and many more. SciPy uses the NumPy `array` as it's base data struture, but also builds upon `Pandas`, `Matplotlib`, and `SymPy`.

# In[1]:


import numpy as np 
import pandas as pd 
from allensdk.core.cell_types_cache import CellTypesCache
from allensdk.api.queries.cell_types_api import CellTypesApi
import matplotlib.pyplot as plt
from scipy import stats 
from scipy import linalg
ctc = CellTypesCache(manifest_file='cell_types/manifest.json')


# We will be demonstrating SciPy using the Allen Cell Types Dataset. We will discuss what this dataset contains and how to navigate through it in a later chapter. 

# In[2]:


# Download meatadata for only human cells 
human_cells = pd.DataFrame(ctc.get_cells(species=[CellTypesApi.HUMAN])).set_index('id')

# Download electrophysiology data 
ephys_df = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')

# Combine our ephys data with our metadata for human cells 
human_ephys_df = human_cells.join(ephys_df)
human_ephys_df.head()


# ## SciPy for two-sample statistics

# In[3]:


# Set up our two samples 
spiny_df = human_ephys_df[human_ephys_df['dendrite_type']== 'spiny']
aspiny_df = human_ephys_df[human_ephys_df['dendrite_type']== 'aspiny']


# Most often, the goal of our hypothesis testing is to test whether or not two distributions are different, or if a distribution has a different mean than the underlying population distribution.
# 
# If we know our distributions are normal (i.e. they're generated from a normal distribution!) we could use parametric statistics to test our hypothesis. To test for differences between normal populations, we can use the independent t-test in our stats package: `stats.ttest_ind()`. If we had paired samples, we would use a dependent t-test: `stats.ttest_rel()`.
# 
# 
# If one of our populations is skewed, however, we cannot use a t-test. A t-test assumes that the populations are normally distributed. For skewed populations, we can use either the Mann-Whitney U (for independent samples: `stats.mannwhitneyu()`) or the Wilcoxon Signed Rank Test (for dependent/paired samples: `stats.wilcoxon()`).

# Below we will run a statistical test that compares `aspiny_df['tau']` to `spiny_df['tau']`. Before we decide what test to run, we must first check the skewness of our data. To test for skewness, we can use `stats.skewtest()`. **If the skew test gives us a p-value of less than 0.05, the population is skewed.**

# In[4]:


# Subselect our samples 
sample_1 = spiny_df['tau']
sample_2 = aspiny_df['tau']

# Run the skew test
stats_1, pvalue_1 = stats.skewtest(sample_1) 
stats_2, pvalue_2 = stats.skewtest(sample_2)

# Print the p-value of both skew tests
print('Spiny skew test pvalue: ' + str(pvalue_1))
print('Aspiny skew test pvalue: ' + str(pvalue_2))

# Plot our distributions 
plt.hist(sample_1)
plt.show()
plt.hist(sample_2)
plt.show()


# Our pvalues indicate that both of our samples are skewed, therefore we will continure with the Mann-Whitney U test. 

# In[5]:


print(stats.mannwhitneyu(sample_1, sample_2))


# ## SciPy for Linear Algebra

# SciPy can be used to find solutions to mathematical algorithms as well. The package has a module with many tools that are helpful with linear algebra. The funtions availabe can help with solving the determinant of a matrix, solve for eigen values, and other liniar algebra problems. After importing the linear algebra module, `linalg` from the SciPy package, it is important to use the syntax `linalg.function()` when executing a function from the module. 

# The `linalg.det()` method is used to solve for the the determinant of a matrix. This function only takes in square matrices as an argument, inputting a non-square matrix will result in an error. Please visit <a href = 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.det.html'> here</a> for the original documentation. 

# In[6]:


# Assign our square matrix
matrix = np.array([[1,3,5,2], [6,3,9,7], [2,7,8,5], [9,4,1,8]])
print(matrix)


# In[7]:


print(linalg.det(matrix))


# The `linalg.lu()` method is used to solve the LU decomposition of a matrix. It will return the  permutation matrix, p, the lower triangular matrix with unit diagonal elements, l,  and the upper triangular, u. You can look at the <a href = 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lu.html' > original documentation</a> for more information. 

# In[8]:


# Assign our matrix 
p, l, u = linalg.lu(matrix)
print('Permutation matrix:')
print(p)
print('\n')
print('Lower triangular:')
print(l)
print('\n')
print('Upper Triangle')
print(u)


# Now that we have p, l, and u, we can used a funtion from numpy, `np.dot()` to execute the dot product of l and u to return our matrix. 

# In[9]:


print(np.dot(l,u))


# You can also find the eigen values and eigen vectors with SciPy. The method `linalg.eig()` takes in a complex or real matrix and returns its eigenvalues. Please visit <a href = 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eig.html'> here</a> for the orignal documentation.

# In[10]:


eigen_values, eigen_vectors = linalg.eig(matrix) 
print(eigen_values)
print('\n')
print(eigen_vectors) 


# Lastly, SciPy can be used to solve linear systems of equations. Please visit <a href = 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve.html'> here</a> for the orignal documentation.

# In[11]:


array = [[2],[4],[6],[8]]
print(linalg.solve(matrix, array))


# ## SciPy for FFT

# Let's first generate a sine wave. We'll then generate a second sine wave and add these together to understand what a fourier transform of this data would look like. Sine waves are defined by their frequency, ampltitude, and and phase. 

# In[12]:


sampling_freq = 1024 # Sampling frequency 
duration = 0.3 # 0.3 seconds of signal
freq1 = 7 # 7 Hz signal
freq2 = 130 # 130 Hz signal

# Generate a time vector
time_vector = np.arange(0, duration, 1/sampling_freq)

# Generate a sine wave
signal_1 = np.sin(2 * np.pi * freq1 * time_vector) 
# Generate another sine wave, with double the power
signal_2 = np.sin(2 * np.pi * freq2 * time_vector) * 2 
                                                       
# Add the signals we created above into one signal
combined_signal = signal_1 + signal_2

print('You\'ve created a complex signal with two sin waves, it looks like this:')
print(combined_signal)


# What we have are the signal values for our complex signal composed of the two sin waves. To see our `combined_signal` we must plot it using `plt.plot()`.

# In[13]:


# Set up our figure
fig = plt.figure(figsize=(12, 4))

# Plot 0.5 seconds of data
plt.plot(time_vector, combined_signal) 
plt.ylabel('Signal',fontsize=14)
plt.xlabel('Time',fontsize=14)
plt.show()


# In[14]:


# plt.plot(time_vector, signal_1)
# plt.show()
# plt.plot(time_vector, signal_2)
# plt.show()


# Below, we'll calculate the **Fourier Transform**, which will determine the frequencies that are in our sample. We'll implement this with Welch's Method, which consists in averaging consecutive Fourier transform of small windows of the signal, with or without overlapping. Basically, we calculate the fourier transform of a signal across a few sliding windows, and then calculate the mean PSD from all the sliding windows.
# 
# The freqs vector contains the x-axis (frequency bins) and the psd vector contains the y-axis values (power spectral density). The units of the power spectral density, when working with EEG data, is usually $\mu$V^2 per Hz.

# In[15]:


# Import signal processing module 
from scipy import signal

# Define sliding window length (4 seconds, which will give us 2 full cycles at 0.5 Hz)
win = 4 * sampling_freq
freqs, psd = signal.welch(combined_signal, sampling_freq, nperseg=win)

# Plot our data
plt.plot(freqs,psd) # Plot a select range of frequencies
plt.ylabel('Power')
plt.xlabel('Frequency (Hz)')
plt.title('FFT of a complex signal')
plt.show()


# The Fourier Transformation shows us the signal frequencies that make up our combined signal. 

# ***Possible section on the Nyquist Theory***

# In[ ]:





# In[ ]:





# In[ ]:





# ## Additional Resources

# 

# In[ ]:




