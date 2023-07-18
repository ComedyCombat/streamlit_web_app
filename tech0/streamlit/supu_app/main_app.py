import streamlit as st
from PIL import Image


st.title('テストアプリ')
st.caption('これは、コメコン用のテストアプリです')

image = Image.open('./data/kuwa.jpg')
st.image(image, width=200)