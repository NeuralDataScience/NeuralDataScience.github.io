#!/usr/bin/env python
# coding: utf-8

# ## Chapter 2 Problem Set
# 
# 1. In [Chapter 2.1](https://neuraldatascience.github.io/Chapter_02/Obtaining_Datasets_with_DANDI.html), we demonstrated how to download a particular DANDIset. Modify this code to download another dataset, and dig in to see what's there.
# 
# 2. In [2.3](https://neuraldatascience.github.io/Chapter_02/Working_with_NWB_format_in_Python.html), we created two functions. One of these functions plots binned firing rates over time. Modify this function to accept a NumPy array that is neurons x spike times, and to plot an average firing rate over time. Bonus: add a shaded standard deviation around your average firing rate.
# 
# 3. In [2.2](https://neuraldatascience.github.io/Chapter_02/Sample_Visualizations.html), we looked at the Economo & Svoboda (2018) extracellular data and produced a table of trial times. In 2.2, we showed how to plot a PSTH for single neurons. Use the `interval_trial` table we created in 2.2 to find trials where the mouse either had a "correct" or "incorrect" response. Take an average of firing rates across all neurons in the incorrect and correct, and plot. Is there a difference?
# 
# 
