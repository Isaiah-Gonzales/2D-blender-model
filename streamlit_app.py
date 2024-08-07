from model import *
import streamlit as st
st.title("BU Sampler tool")
st.write("Hi and welcome, this tool creates a model of a blender depending on your inputs. It's recommended to start with a single run to get an understanding of how the program works. If you have any feedback, please reach out to either Isaiah Gonzales or Rajarshi Sengupta.")

model_type = st.selectbox("Would you like to perform a singe run or multiple runs?", ["-","single run","multiple runs"], help ="**Single:** This will simulate one blender and sample top, middle, bottom positions, then return assay values for those positions. **Multiple:** This will perform a specified number of simulations and return the distribution of assay values for each position.") 

if model_type == "single run":
  thiefSize = st.number_input("Size of sample thief (mL)", min_value = 1, max_value = 100)
  percentPurityOfDS = st.number_input("Purity of DS (%)", min_value= 0, max_value = 110, value = 100)
  DL = st.number_input("Blend drug load (%)", min_value = 0, max_value = 100, value = 20)
  blenderSize = st.number_input("Size of blender (mL)", min_value=500)
  fillRatio = st.number_input("Fill volume (%)", min_value=10,value=50, help="What percentage of the blenders total volume is filled with powder?")
  distribution = st.selectbox("Please choose how you wish the powder to be distributed in the blender", ["unmixed", "random", "uniform", "poor"])
  if distribution == "poor":
    percentClumps = st.number_input("What percent of DS particles would you like clumped?", min_value = 1,value=100)
    sizeClumps = st.number_input("Size of DS clumps (microns)", min_value = 2,value=1000)
    
if model_type == "multiple runs":
  numLoops = int(st.number_input("How many simulations would you like to perform and average", min_value = 1, max_value = 500))
  thiefSize = st.number_input("Size of sample thief (mL)", min_value = 1, max_value = 100)
  percentPurityOfDS = st.number_input("Purity of DS (%)", min_value= 0, max_value = 110, value = 100)  
  DL = st.number_input("Blend drug load (%)", min_value = 0, max_value = 100, value = 20)
  blenderSize = st.number_input("Size of blender (mL)", min_value=500)
  fillRatio = st.number_input("Fill volume (%)", min_value=10,value=50, help="What percentage of the blenders total volume is filled with powder?")
  distribution = st.selectbox("Please choose how you wish the powder to be distributed in the blender", ["unmixed", "random", "uniform", "poor"])
  if distribution == "poor":
    percentClumps = st.number_input("What percent of DS particles would you like clumped?", min_value = 1,value=100)
    sizeClumps = st.number_input("Size of DS clumps (microns)", min_value = 2,value=1000)
    
if st.button("Run my simulation"):
  if model_type == "single run":
    if distribution == "poor":
      meanAssayofSamples = blender2D(
                thiefSize=thiefSize, 
                percentPurityOfDS=percentPurityOfDS,
                DL=DL, 
                blenderSize=blenderSize, 
                fillRatio=(fillRatio/100),
                distribution= distribution,
                clumpiness=percentClumps/10,
                clumpSize=sizeClumps,
                visualize=True)
    else:
      meanAssayofSamples = blender2D(
                thiefSize=thiefSize, 
                percentPurityOfDS=percentPurityOfDS,
                DL=DL, 
                blenderSize=blenderSize, 
                fillRatio=(fillRatio/100),
                distribution= distribution,
                visualize=True)
    st.write("**Top Position Assay** = " + str(meanAssayofSamples[0]) + "%")
    st.write("**Middle Position Assay** = " + str(meanAssayofSamples[1]) + "%")
    st.write("**Bottom Position Assay** = " + str(meanAssayofSamples[2]) + "%")

  if model_type == "multiple runs":
    st.write("loading...")
    results = []
    i = 0
    if distribution == "poor":
      while i < numLoops:
        results.append(np.mean(blender2D(thiefSize=thiefSize, 
                  percentPurityOfDS=percentPurityOfDS,
                  DL=DL, 
                  blenderSize=blenderSize, 
                  fillRatio=(fillRatio/100),
                  distribution= distribution,
                  clumpiness=percentClumps/10,
                  clumpSize=sizeClumps,
                  verbose=False)))
        i += 1
    else:
      while i < numLoops:
        results.append(np.mean(blender2D(thiefSize=thiefSize, 
                  percentPurityOfDS=percentPurityOfDS,
                  DL=DL, 
                  blenderSize=blenderSize, 
                  fillRatio=(fillRatio/100),
                  distribution= distribution,
                  verbose=False)))
        i += 1
    figure, ax = plt.subplots(figsize=(10,10))
    viz = ax.boxplot(results)
    plt.title("Spread of mean assays for simulated blender with distribution = " + str(distribution))
    plt.ylabel("Mean Assay (%)")
    st.pyplot(figure)
    
    st.write("**Min Average Assay Observed** = " + str(round(min(results),2))+ "%")
    st.write("**Max Average Assay Observed** = " + str(round(max(results),2))+ "%")
    st.write("**Std Dev. = " + str(round(np.std(results),2))
    
