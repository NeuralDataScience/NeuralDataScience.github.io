#!/usr/bin/env python
# coding: utf-8

# # Single-Cell Electrophysiology

# Electrophysiology is the study of electrical activity inside neurons. There are three main ways of collecting electrophysiologucal data: 
#  1. Extracelluar Recordings 
#  2. Intracellular Recordings 
#  3. Patch Clamp Recordings
#  
# The data in the Allen Cell Types Database was collected through the Whole Cell Patch Clamp method. The Patch Clamp method allows very precise measuremnets for either whole-cell activity or specific ion channels. Patch Clamp recordings are also less inasive than intracelluar recodings becasue they do not pierce the neuon, but "patch" onto the membrane instead. They also provide a better signal-to-noise ratio than extracelluar recodrings.  

# In[1]:


from IPython.display import YouTubeVideo
YouTubeVideo('mF7Vd5olw18')


# **About the Allen Brain Cell Types DataBase** 
# 
# The Allen Brain Cell Types Dataset utilizes Whole-Cell Patch Clamp recordings while injecting differnt waveforms, such as long square, short square, and ramp, into to the cells. The data includes many computed neuron metrics such as adaptivity, interspike interval, and spike rate, and interacelluar characteristics including like resting membrane potential, rheobase, and more. 
# 
# The Allen Brain Cell Types Dataset uses the Cre/LoxP system to target specific cells in mice. The Cre/LoxP system enables conditional knockouts of genes of interest by crossing a Driver mouse with a Reporter mouse, where the Driver mouse contains genes expressing Cre recombinase and the Reporter mouse express LoxP binding sites around the gene of interest. Typically, scientists will knockout a stop codon in front of a GFP to enable GFP fluorescence. Crossing Cre-driver mouse lines with fluorescent reporter lines mark specific subsets of cells.
# 
# In this chapter, you learn how to downlaod single cell electophysiology data from the Allen Brain Cell Types Database, access and plot pre-computed features, plot the morphology of single cells, and compare different types of cells (i.e. spiny vs aspiny dendritic cells).

# **Additional Reosurces**
# 
# The Allen Brain Cell Types Dataset uses hundreds of differnt Cre-driver lines. For a list of all the availabe lines, please visit the <a href = 'http://connectivity.brain-map.org/transgenic'> Transgenic Characterization</a> section of the Allen Mouse Connectivity site. 

# In[ ]:





# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# Morphology_For_Single_Cells
# Plotting_A_Single_Sweep_of_Data
# Available_Pre-Computed_Features
# Comparing_Different_Types_of_Cells
# ```
# 
