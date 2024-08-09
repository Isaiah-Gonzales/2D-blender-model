from model import *
import streamlit as st

tab1, tab2 = st.tabs(["model", "example"])

with tab1:
  st.title("BU Sampler tool")
  st.write("Hi and welcome, this tool creates a model of a blender depending on your inputs. It's recommended to start with simulating one blender to get an understanding of how the program works. If you have any feedback, please reach out to either **Isaiah Gonzales** or **Rajarshi Sengupta**.")
  
  st.sidebar.write("**Input simulation parameters here**")
  model_type = st.sidebar.selectbox("Would you like to simulate one blender (single run), or multiple blenders (multiple runs)", ["-","single run","multiple runs"], help ="**Single:** This will simulate one blender, and return *individual* assays of BU samples extracted. **Multiple:** This will simulate multiple blenders, and return *mean* assays, this can be useful to understand probabilities. ") 
  
  if model_type != "-":
    distribution = st.sidebar.selectbox("Please choose how you wish the powder to be distributed in the blender", ["unmixed", "random", "uniform", "poor"])
    blenderSize = st.sidebar.number_input("Size of blender (mL)", min_value=500)
    advanced_options = st.sidebar.expander("Advanced Options")
    with advanced_options:
      thiefSize = st.slider("Size of sample thief (mL)", min_value = 1, max_value = 10, step =1)
      numSamples = st.slider("Number of samples to extract", min_value = 1, max_value = 10, step =1)
      percentPurityOfDS = st.slider("Purity of DS (%)", min_value= 0, max_value = 110, value = 100, step=10)
      DL = st.slider("Blend drug load (%)", min_value = 0, max_value = 100, value = 20, step=10)
      fillRatio = st.slider("Fill volume (%)", min_value=10, max_value=100, step= 10, value=50, help="What percentage of the blenders total volume is filled with powder?")
  
    if distribution == "poor":
      with advanced_options:
        percentClumps = st.slider("What percent of DS particles would you like clumped?", min_value = 1,value=50, step =10)
        sizeClumps = st.number_input("Size of DS clumps (microns)", min_value = 100,value=1000, max_value =10000)
    
  if model_type == "multiple runs":
    numLoops = int(st.sidebar.number_input("How many simulations would you like to perform and average", min_value = 1, max_value = 500))
    
  if st.sidebar.button("Run my simulation"):
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
      i=1
      for assay in meanAssayofSamples:
        st.write("Sample " + str(i) + "= " + str(assay) + "%")
        i += 1
  
    if model_type == "multiple runs":
      results = []
      meanResults = []
      i = 0
      progbar = st.progress(0.0)
      if distribution == "poor":
        while i < numLoops:
          progbar.progress(i/numLoops, text = "simulation " + str(i) + " of " + str(numLoops))
          results.append(blender2D(thiefSize=thiefSize, 
                    percentPurityOfDS=percentPurityOfDS,
                    DL=DL, 
                    blenderSize=blenderSize, 
                    fillRatio=(fillRatio/100),
                    distribution= distribution,
                    clumpiness=percentClumps/10,
                    clumpSize=sizeClumps,
                    verbose=False))
          i += 1
        progbar.empty()
      else:
        while i < numLoops:
          progbar.progress(i/numLoops, text = "simulation " + str(i) + " of " + str(numLoops))
          results.append(blender2D(thiefSize=thiefSize, 
                    percentPurityOfDS=percentPurityOfDS,
                    DL=DL, 
                    blenderSize=blenderSize, 
                    fillRatio=(fillRatio/100),
                    distribution= distribution,
                    verbose=False))
          i += 1
        progbar.empty()
          
      flattenedResults = []
      for result in results:
        meanResults.append(np.mean(result))
        for val in result:
          flattenedResults.append(val)
  
      
      figure, ax = plt.subplots(figsize=(10,10))
      viz = ax.boxplot(meanResults)
      plt.title("Spread of mean assays for simulated blender with distribution = " + str(distribution))
      plt.ylabel("Mean Assay (%)")
      st.pyplot(figure)
  
  
                           
      st.write("**Min Average Assay Observed** = " + str(round(min(meanResults),2))+ "%")
      st.write("**Max Average Assay Observed** = " + str(round(max(meanResults),2))+ "%")
      st.write("**Std Dev.** = " + str(round(np.std(meanResults),2)))
      st.write("Min Individual Assay Observed = " + str(round(min(flattenedResults),2)) + "%")
      st.write("Max Individual Assay Observed = " + str(round(max(flattenedResults),2)) + "%")
