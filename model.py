import streamlit as st
from matplotlib import pyplot as plt
from matplotlib import colors
import time
import numpy as np
import random
import math

#create function to return the distance from 100% assay for a given set of parameters  

def blender2D(blenderSize, fillRatio,thiefSize, distribution, DL=20, particleSize=100, estimatorLoops=500, percentPurityOfDS=100, visualize=False, numClumps=10, sizeClumps=1000):
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
        st.write("loading...")
        placeholderArray[yAxisHalf:,:] = percentPurityOfDS
        blenderArray = placeholderArray.copy()

    if distribution == "random":
        st.write("loading...")
        numberDSparticles = (xAxisSize**2) * (DL/100)
        if DL > 100:
            st.write("DL must be less than 100")
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

    if distribution == "poor":
        st.write("loading...")
        clumpedParticles = numClumps * sizeClumps
        flattenedArray = placeholderArray.flatten()
        if (clumpedParticles) > ((xAxisSize**2) * (DL/100)):
            st.write("Number of clumped particles too great, please reduce number or size of clumps")
            return
        numberDSparticles = (xAxisSize**2) * (DL/100)
        possiblePositions = list(range(0, xAxisSize**2, 1))
        possiblePositions = possiblePositions[:(len(flattenedArray)-clumpedParticles)]
        for n in range(numClumps):
            selectedPosition = random.choice(possiblePositions)
            flattenedArray[selectedPosition:selectedPosition+sizeClumps] = percentPurityOfDS
            possiblePositions[selectedPosition:selectedPosition+sizeClumps] = "x"
            possiblePositions.remove("x")
        st.write("clumping complete")
        blenderArray = flattenedArray.reshape(xAxisSize, yAxisSize)
        i = (numClumps*sizeClumps)
        while i < numberDSparticles:
            random_row = random.randint(0, yAxisSize-1) 
            random_value = random.randint(0, xAxisSize-1)
            if blenderArray[random_row][random_value] == 0:
                blenderArray[random_row][random_value] = percentPurityOfDS
                i += 1
            else:
                pass
        st.write("remaining particles dispersed")

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
        st.write(names[row] + " sampling complete.")
        samplingResults.append(np.mean(sampledValues))

    #Visualize
    if visualize == True:
        figure, ax = plt.subplots(figsize=(10,10))
        viz = ax.imshow(blenderArray, interpolation='nearest', cmap='binary') #draw 2D array
        colorbar = figure.colorbar(viz)
        plt.title("Simulated blender, distribution = " + str(distribution))    

    #Final Results
    meanAssays = []
    for result in samplingResults:
        meanAssay = (result/DL)*100
        meanAssays.append(round(meanAssay,2))

    return meanAssays
