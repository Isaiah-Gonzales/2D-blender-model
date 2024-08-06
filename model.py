import streamlit as st
from matplotlib import pyplot as plt
from matplotlib import colors
import time
import numpy as np
import random
import math

#create function to return the distance from 100% assay for a given set of parameters  

def blender2D(blenderSize, fillRatio,thiefSize, distribution, DL=20, particleSize=100, estimatorLoops=500, percentPurityOfDS=100, visualize=False, clumpiness = 0, clumpSize = 1000, verbose = True):
    amountOfPowder = blenderSize * fillRatio #mL or cm3
    particleSizeInCm = particleSize / 10000 #cm
    areaOfOneParticle = particleSizeInCm**2 

    #number of particles that could fit in blender, assuming they are packed in a square
    xAxisSize = math.ceil(math.sqrt(amountOfPowder/areaOfOneParticle))
    yAxisSize = math.ceil(math.sqrt(amountOfPowder/areaOfOneParticle))

    #we'll assume that sample thief is square, this will tell us how many particles to average per sample
    xAxisSizeThief = math.ceil(math.sqrt(thiefSize/areaOfOneParticle))
    yAxisSizeThief = math.ceil(math.sqrt(thiefSize/areaOfOneParticle))

    placeholderArray = np.zeros((xAxisSize, yAxisSize)) # Create a 2D array of all 0's
    yAxisHalf = int(yAxisSize/2)

    if (xAxisSize**2) < ((xAxisSizeThief**2)*3):
        st.write("Thief size too large in comparison to blender size")
        return

    #Define distributions
    if distribution == "unmixed":
        if verbose == True:
            st.write("loading...")
        placeholderArray[yAxisHalf:,:] = percentPurityOfDS
        blenderArray = placeholderArray.copy()
        
    if distribution == "poor":
        if verbose == True:
            st.write("loading...")
        if clumpiness == 0:
            disitrbution = "random"
        else:
            #calculate number of clumps
            numberDSparticles = (xAxisSize**2) * (DL/100)
            clumpedParticles = numberDSparticles * (clumpiness/10)
            clumpSize = 1000 #um
            clumpXaxis = clumpSize / 10000 #cm
            clumpYaxis = clumpSize / 10000 #cm
            clumpArea = clumpXaxis * clumpYaxis
            numParticlesPerClump = int(clumpArea/ (particleSizeInCm**2))
            numClumps = int(clumpedParticles/numParticlesPerClump)
            if verbose == True
                st.write("number of clumps: " + str(numClumps))
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
                st.write("Clumping Complete")
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
                st.write("remaining particles dispersed")
            
    if distribution == "random":
        if verbose == True:
            st.write("loading...")
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
            st.write("loading...")
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
    samplingResults = []
    names = {1:"top", int(yAxisHalf-(yAxisSizeThief/2)):"middle", int(yAxisSize-yAxisSizeThief):"bottom"}
    rowsToSample = [1, int(yAxisHalf-(yAxisSizeThief/2)), yAxisSize-yAxisSizeThief]
    for row in rowsToSample:
        sampledValues = []
        startingRow = row
        #return the index of the random value
        startingCol = 10

        #average the value of the particles in the sample thief
        i = 0 #row iterator, still want to start at the same row
        j = 1 #col iterator, but want to start at the next col
        while i < xAxisSizeThief:
            while j < yAxisSizeThief:
                currentRow = startingRow + i
                currentColumn = startingCol + j
                sampledValues.append(blenderArray[currentRow][currentColumn])
                j += 1
            j = 0 #after first row, we want to grab all the values    
            i += 1
        if verbose == True:
            st.write(names[row] + " sampling complete.")
        samplingResults.append(np.mean(sampledValues))

    #Visualize
    if visualize == True:
        figure, ax = plt.subplots(figsize=(10,10))
        viz = ax.imshow(blenderArray, interpolation='nearest', cmap='binary') #draw 2D array
        colorbar = figure.colorbar(viz)
        plt.title("Simulated blender, distribution = " + str(distribution))    
        st.pyplot(figure)
    
    #Final Results
    meanAssays = []
    for result in samplingResults:
        meanAssay = (result/DL)*100
        meanAssays.append(round(meanAssay,2))

    return meanAssays
