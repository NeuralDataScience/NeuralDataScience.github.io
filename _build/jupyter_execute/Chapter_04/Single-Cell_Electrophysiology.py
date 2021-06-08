#!/usr/bin/env python
# coding: utf-8

# # Single-Cell Electrophysiology

# Electrophysiology is the study of the electrical activity created by neurons. There are three main ways of collecting electrophysiology data: 
#  1. Extracellular Recordings: electrode outside of the cell
#  2. Intracellular Recordings: electrode inside of the cell 
#  3. Patch Clamp Recordings: electrode continuous with cell membrane
#  
# ![](https://www.researchgate.net/publication/349446871/figure/fig1/AS:993163909025795@1613800136978/Overview-of-the-patch-clamp-method-a-Comparison-between-extracellular-and.ppm)
#  
# The data in the Allen Cell Types Database was collected through the Whole Cell Patch Clamp method. Patch clamp allows for very precise measurements of either whole-cell activity or specific ion channels. The video below shows what patch clamping looks like. 

# In[1]:


from IPython.display import YouTubeVideo
YouTubeVideo('mF7Vd5olw18')


# **About the Allen Brain Cell Types DataBase** 
# 
# The Allen Brain Cell Types Dataset utilizes Whole-Cell Patch Clamp recordings while injecting different current waveforms into to the cells. The dataset also includes many computed neuron metrics such as adaptivity, interspike interval, and spike rate, and interacelluar characteristics including like resting membrane potential, rheobase, and more. 
# 
# The Allen Brain Cell Types Dataset uses the Cre/LoxP system to target specific cells in mice. The Cre/LoxP system enables conditional knockouts of genes of interest by crossing a Driver mouse with a Reporter mouse, where the Driver mouse contains genes expressing Cre recombinase and the Reporter mouse express LoxP binding sites around the gene of interest. Crossing Cre-driver mouse lines with fluorescent reporter lines mark specific subsets of cells and allow researchers to target specific cells for recording.
# 
# In this chapter, you learn how to downlaod single cell electophysiology data from the Allen Brain Cell Types Database, access and plot pre-computed features, plot the morphology of single cells, and compare different types of cells (i.e. spiny vs aspiny dendritic cells).

# **Additional Resources**
# 
# * The Allen Brain Cell Types Dataset uses hundreds of different Cre-driver lines. For a list of all the available lines, please visit the <a href = 'http://connectivity.brain-map.org/transgenic'> Transgenic Characterization</a> section of the Allen Mouse Connectivity site. 
