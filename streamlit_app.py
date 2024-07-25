from model import *
import streamlit as st
st.title("BU Sampler tool")
st.write("Hi and welcome, this tool creates a model of a blender depending on your inputs. It's recommended to start with a single run to get an understanding of how the program works. If you have any feedback, please reach out to either Isaiah Gonzales or Rajarshi Sengupta.")

model_type = st.selectbox("Would you like to perform a singe run or multiple runs?", ["-","single run","multiple runs"], help ="**Single:** This will simulate one blender and sample top, middle, bottom positions, then return assay values for those positions. **Multiple:** This will perform a specified number of simulations and return the distribution of assay values for each position.") 

if model_type == "single run":
  thiefSize = st.number_input("Size of sample thief (mL)", min_value = 1, max_value = 100)
  percentPurityOfDS = st.number_input("Purity of DS (%)", min_value= 0, max_value = 110)
  DL = st.number_input("Blend drug load (%)", min_value = 0, max_value = 100)
  blenderSize = st.number_input("Size of blender (mL)", min_value=5)
  fillRatio = st.number_input("Fill volume (%)", min_value=10, help="What percentage of the blenders total volume is filled with powder?")
  distribution = st.selectbox("Please choose how you wish the powder to be distributed in the blender", ["unmixed", "random", "uniform", "poor"])
  if distribution == "poor":
    numClumps = st.number_input("Number of DS clumps present", min_value = 1, help ="This will create n number of DS clump in the blender, increasing this value makes the distribution more poor")
    sizeClumps = st.number_input("Size of DS clumps", min_value = 2, help="This will control how large the clumps of DS are, increasing this value will make the distribution more poor")
    
if model_type == "mutiple runs":
  numLoops = st.number_input("How many simulations would you like to perform and average")
  thiefSize = st.number_input("Size of sample thief (mL)", min_value = 1, max_value = 100)
  percentPurityOfDS = st.number_input("Purity of DS (%)", min_value= 0, max_value = 110)
  DL = st.number_input("Blend drug load (%)", min_value = 0, max_value = 100)
  blenderSize = st.number_input("Size of blender (mL)", min_value=5)
  fillRatio = st.number_input("Fill volume (%)", min_value=10, help="What percentage of the blenders total volume is filled with powder?")
  distribution = st.selectbox("Please choose how you wish the powder to be distributed in the blender", ["unmixed", "random", "uniform", "poor"])
  if distribution == "poor":
    numClumps = st.number_input("Number of DS clumps present", min_value = 1, help ="This will create n number of DS clump in the blender, increasing this value makes the distribution more poor")
    sizeClumps = st.number_input("Size of DS clumps", min_value = 2, help="This will control how large the clumps of DS are, increasing this value will make the distribution more poor")
    
if st.button("Run my simulation"):
  if model_type == "single run":
    if distribution == "poor":
      meanAssayofSamples = blender2D(
                thiefSize=thiefSize, 
                percentPurityOfDS=percentPurityOfDS,
                DL=DL, 
                blenderSize=blenderSize, 
                fillRatio=fillRatio,
                distribution= distribution,
                numClumps=numClumps,
                sizeClumps=sizeClumps,
                visualize=True)
    else:
      meanAssayofSamples = blender2D(
                thiefSize=thiefSize, 
                percentPurityOfDS=percentPurityOfDS,
                DL=DL, 
                blenderSize=blenderSize, 
                fillRatio=fillRatio,
                distribution= distribution,
                visualize=True)
    st.write("**Top Position Assay** = " + str(meanAssayofSamples[0]) + "%")
    st.write("**Middle Position Assay** = " + str(meanAssayofSamples[1]) + "%")
    st.write("**Bottom Position Assay** = " + str(meanAssayofSamples[2]) + "%")

  if model_type == "multiple runs":
    results = []
    i = 0
    if disitribution == "poor":
      while i < numLoops:
        results.append(thiefSize=thiefSize, 
                  percentPurityOfDS=percentPurityOfDS,
                  DL=DL, 
                  blenderSize=blenderSize, 
                  fillRatio=fillRatio,
                  distribution= distribution,
                  numClumps=numClumps,
                  sizeClumps=sizeClumps,
                  verbose=False)
        i += 1
    else:
      while i < numLoops:
        results.append(thiefSize=thiefSize, 
                  percentPurityOfDS=percentPurityOfDS,
                  DL=DL, 
                  blenderSize=blenderSize, 
                  fillRatio=fillRatio,
                  distribution= distribution,
                  verbose=False)
        i += 1
    st.write("**Min Assay Observed** = " + str(min(results)))
    st.write("**Max Assay Observed** = " +str(max(results)))
    
