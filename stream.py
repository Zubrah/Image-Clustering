import streamlit as st
from PIL import Image
from itertools import cycle
import os

st.title("Google Images Clustering")

st.text(
    """
    A Machine Learning App that clusters product images according to either the similarity of the images or the similarity of the texts that describe the images.
    """
)

directory = "Output"

i = 1
for folder in os.listdir(directory):
    st.header('Cluster ' + str(i))
    cols = cycle(st.columns(4))
    for filename in os.listdir(os.path.join(directory, folder)):
        image = Image.open(os.path.join(directory, folder, filename))
        next(cols).image(image, caption=filename, width=150)
    i+=1


    # 