#!/usr/bin/env python
# coding: utf-8

# # Large Scale Electrophysiology

# A single neuron can not carry out tasks such as reading by itself -- it requires the surrounding, interconnected neurons to send and receive signals and accomplish the simplest of tasks. In modern large-scale electrophysiology, the activity of hundreds of neurons are recorded in an attempt to determine where neuron activity occurs and how these cells communicate with each other when presented with certain tasks.  

# **Neuropixels Probes**
# 
# The technological advancement of the Neuropixels probe has significantly propelled systems neuroscience research in recent years ([Jun et al., 2017](https://www.nature.com/articles/nature24636)). Each probe is approximately the size of a strand of hair and has 960 recording sites allowing for hundreds of neurons to be recorded simultaneously. The reduced size of these recording devices allows for mutliple probes to be inserted into the same brain, providing real time recordings of multiple brain areas.

# ![](https://brainmapportal-live-4cc80a57cd6e400d854-f7fdcae.divio-media.net/filer_public/88/00/8800429b-8811-471f-9f04-82d19b3851b0/neuropixels_visual_coding_cms_images-04.png)

# **The Allen Institute Neuropixels Dataset**
# 
# The Visual Coding - Neuropixels dataset from the Allen Institute of Brain Sciences records spiking activity in the visual system of the mouse brain. At the time of writing, this dataset contains a total of 58 experiment sessions from Neuropixels probes in the cortex, hippocampus, and thalamus. There are three different trangenic mouse lines used in the experiments alongside the wild-type mice, which mark three different inhibitory cell types. The stimuli presented in this dataset range from natural scenes to drifting gratings. 
# 
# In this chapter you will learn how to download and sort through the Neuropixels dataset. Once you learn the basics, you will learn how to perform possible analyses to explain the neural activity within, as well as how to use optogenetics to identify different cell types within the data. 

# **Additional Resources** 
# 
# * For more information on the Allen Institute's Neuropixels dataset, please visit <a href = 'https://portal.brain-map.org/explore/circuits/visual-coding-neuropixels'>the Allen Institute website</a>.
# * To read more about the potential of Neuropixels probes, read this [Simons Foundation article](https://www.simonsfoundation.org/2018/01/04/neuropixels-offer-new-ways-to-map-cells/).
# * For technical information about the Neuropixel probes or to learn how to obtain them, please visit <a href = 'https://www.neuropixels.org/'> neuropixels.org</a>.
