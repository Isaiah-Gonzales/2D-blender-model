from model import *
import streamlit as st
st.title("BU Sampler tool")
st.write("Hi and welcome, this tool creates a model of a blender depending on your inputs. It's recommended to start with a single run to get an understanding of how the program works. If you have any feedback, please reach out to either Isaiah Gonzales or Rajarshi Sengupta.")

model_type = st.selectbox("Would you like to perform a singe run or multiple runs?", ["single run","multiple runs"], help ="**Single:** This will simulate one blender and sample top, middle, bottom positions, then return assay values for those positions. **Multiple:** This will perform a specified number of simulations and return the distribution of assay values for each position.") 

if model_type == "single run":
  thiefSize = st.numberinput("Size of sample thief (mL)", min_value = 1, max_value = 100)
  percentPurtityofDS = st.numberinput("Purity of DS (%)", min_value= 0, max_value = 110)
  DL = st.numberinput("Blend drug load (%)", min_value = 0, max_value = 100)
  blenderSize = st.numberinput("Size of blender (mL)", min_value=5)
  fillRatio = st.numberinput("Fill volume (%)", min_value=10, help="What percentage of the blenders total volume is filled with powder?")
  distribution = st.selectbox("Please choose how you wish the powder to be distributed in the blender", ["unmixed", "random", "uniform", "poor"])
  st.write("The below inputs only matter if your distribution is **random** ")
  numClumps = st.numberinput("Number of DS clumps present", min_value = 1, help ="This will create n number of DS clump in the blender, increasing this value makes the distribution more poor")
  sizeClumps = st.numberinput("Size of DS clumps", min_value = 2, help="This will control how large the clumps of DS are, increasing this value will make the distribution more poor")

if st.button("Run my simulation"):
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
              distribution= distribution,,
              visualize=True)
  st.print("Top Position Assay = " + str(meanAssayofSamples[0]) + "%")
  st.print("Middle Position Assay = " + str(meanAssayofSamples[1]) + "%")
  st.print("Bottom Position Assay = " + str(meanAssayofSamples[2]) + "%")
