from model import *
import streamlit as st
st.title("BU Sampler tool")
st.write("Hi and welcome, this tool creates a model of a blender depending on your inputs. It's recommended to start with a single run to get an understanding of how the program works. If you have any feedback, please reach out to either Isaiah Gonzales or Rajarshi Sengupta.")

model_type("Would you like to perform a singe run or multiple runs?", ["single run","multiple runs"], help ="**Single:** This will simulate one blender and sample top, middle, bottom positions, then return assay values for those positions. **Multiple:** This will perform a specified number of simulations and return the distribution of assay values for each position." 
