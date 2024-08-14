import streamlit as st
from matplotlib import pyplot as plt
from matplotlib import colors
import matplotlib
import time
import numpy as np
import random
import math

#create function to return the distance from 100% assay for a given set of parameters  

def blender2D(blenderSize, fillRatio,thiefSize, distribution, DL=20, particleSize=100, percentPurityOfDS=100, visualize=False, clumpiness = 0, clumpSize = 1000, verbose = True, numSamples = 3):
    volumeOfPowder = (blenderSize * fillRatio) #mL or cm3
    particleVolumeInCubicCm = particleSize / 100000 #cm 

    #number of particles that could fit in blender, assuming they are packed in a square
    xAxisSize = math.ceil(math.sqrt(volumeOfPowder/particleVolumeInCubicCm))
    yAxisSize = math.ceil(math.sqrt(volumeOfPowder/particleVolumeInCubicCm))

    #we'll assume that sample thief is square, this will tell us how many particles to average per sample
    xAxisSizeThief = math.ceil(math.sqrt(thiefSize/particleVolumeInCubicCm))
    yAxisSizeThief = math.ceil(math.sqrt(thiefSize/particleVolumeInCubicCm))

    placeholderArray = np.zeros((xAxisSize, yAxisSize)) # Create a 2D array of all 0's
    yAxisHalf = int(yAxisSize/2)

    if (xAxisSize**2) < ((xAxisSizeThief**2)*numSamples):
        st.write("Thief size too large in comparison to blender size or number of samples too high")
        return

    #Define distributions
    if distribution == "unmixed":
        if verbose == True:
            with st.spinner("loading..."):
                time.sleep(1)
        placeholderArray[yAxisHalf:,:] = percentPurityOfDS
        blenderArray = placeholderArray.copy()
        
    if distribution == "poor":
        if verbose == True:
            with st.spinner("loading..."):
                time.sleep(1)
        if clumpiness == 0:
            disitrbution = "random"
        else:
            #calculate number of clumps
            numberDSparticles = (xAxisSize**2) * (DL/100)
            clumpedParticles = numberDSparticles * (clumpiness/10)
            clumpSize = 1000 #um
            clumpVolumeInCubicCm = clumpSize / 10000
            numParticlesPerClump = int(clumpVolumeInCubicCm/ (particleVolumeInCubicCm))
            numClumps = int(clumpedParticles/numParticlesPerClump)
            if verbose == True:
                with st.spinner("number of clumps: " + str(numClumps)):
                    time.sleep(1)
            #disperse clumps in blender
            n = 0
            numParticlesInClumpAxis = int(clumpSize/particleSize)
            usableSpace = (yAxisSize-1) - (numParticlesInClumpAxis)
            while n < numClumps:
                random_row = random.randint(0, usableSpace)
                random_value = random.randint(0, usableSpace)
                section = placeholderArray[random_row:random_row+numParticlesInClumpAxis, random_value:random_value+numParticlesInClumpAxis]
                if any(percentPurityOfDS in sublist for sublist in section):
                    pass
                else:
                    placeholderArray[random_row:random_row+numParticlesInClumpAxis, random_value:random_value+numParticlesInClumpAxis] = percentPurityOfDS                    
                    n += 1
            if verbose == True:
                with st.spinner("Clumping Complete"):
                    time.sleep(1)
            blenderArray = placeholderArray.copy()
            i = clumpedParticles
            while i < numberDSparticles:
                random_row = random.randint(0, yAxisSize-1) 
                random_value = random.randint(0, xAxisSize-1)
                if blenderArray[random_row][random_value] == 0:
                    blenderArray[random_row][random_value] = percentPurityOfDS
                    i += 1
                else:
                    pass
            if verbose == True:        
                with st.spinner("remaining particles dispersed"):
                    time.sleep(1)
            
    if distribution == "random":
        if verbose == True:
            with st.spinner("loading..."):
                time.sleep(1)
        numberDSparticles = (xAxisSize**2) * (DL/100)
        if DL > 100:
            st.write("DL must be less than 100")
            return
        else:
            i = 0
            while i < numberDSparticles:
                random_row = random.randint(0, yAxisSize-1) 
                random_value = random.randint(0, xAxisSize-1)
                if placeholderArray[random_row][random_value] == 0:
                    placeholderArray[random_row][random_value] = percentPurityOfDS
                    i += 1
                else:
                    pass
            blenderArray = placeholderArray.copy()

    if distribution == "uniform":
        if verbose == True:
            with st.spinner("loading..."):
                time.sleep(1)
        numberDSparticles = (xAxisSize**2) * (DL/100)
        frequencyOfDS = int(100/DL)
        flattenedArray = placeholderArray.flatten()
        i = 0
        while i < len(flattenedArray):
            if i%frequencyOfDS == 0:
                flattenedArray[i] = percentPurityOfDS
                i +=1
            else:
                i += 1
        blenderArray = flattenedArray.reshape(xAxisSize, yAxisSize)

    #Sampling loops    
    samplingArray = np.zeros((xAxisSize, yAxisSize))
    toSample = {}
    samplingResults = []
    samplableSpace = (yAxisSize-1) - (xAxisSizeThief)
    currentSample = 1
    sampleProg = st.progress(0.0)
    while currentSample <= numSamples:
        random_row = random.randint(0, samplableSpace)
        random_value = random.randint(0, samplableSpace)
        section = samplingArray[random_row:random_row+yAxisSizeThief, random_value:random_value+xAxisSizeThief]
        if any(1 in sublist for sublist in section):
            pass
        else:
            sampleProg.progress(currentSample/numSamples, text = "sample " + str(currentSample) + " of " + str(numSamples))
            samplingArray[random_row:random_row+yAxisSizeThief, random_value:random_value+xAxisSizeThief] = 1  
            print("Sample " + str(currentSample) + " complete") 
            toSample[random_row] = random_value                 
            currentSample += 1
    sampleProg.empty()
    for row,value in toSample.items():
        samplingResults.append(np.mean(blenderArray[row:row+yAxisSizeThief,value:value+xAxisSizeThief]))
    
    #Visualize
    if visualize == True:
        figure, ax = plt.subplots(figsize=(10,10))
        for row,value in toSample.items():
            blenderArray[row:row+yAxisSizeThief,value:value+xAxisSizeThief] = np.nan
        cmap = matplotlib.cm.binary.copy()
        cmap.set_bad(color='cornflowerblue')
        viz = ax.imshow(blenderArray, interpolation='none', cmap=cmap) #draw 2D array
        colorbar = figure.colorbar(viz)
        plt.title("Simulated blender, distribution = " + str(distribution) + ", sampled locations shown in blue") 
        plt.xlabel("Particles size " + str(particleSize) +"μm")
        plt.ylabel("Particles size " + str(particleSize) +"μm")
        st.pyplot(figure)
    
    #Final Results
    meanAssays = []
    for result in samplingResults:
        meanAssay = (result/DL)*100
        meanAssays.append(round(meanAssay,2))

    return meanAssays
