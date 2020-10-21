import streamlit as st
import numpy as np
import pandas as pd
from keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background.png')


with open('model.json', 'r') as json_file: 
    loaded_model_json = json_file.read()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

st.title('EPP predictor')

all_df = pd.read_csv(r'C:\Users\Ayush\Documents\GitHub\EPP-predictor\all_data_final.csv')

def get_data(db,lat,longi):
    lat = round(lat*4)/4
    longi = round(longi*4)/4
    df = db[db["latitude"] == lat]
    df = df[df["longitude"] == longi]
    return df

lat = st.number_input('Enter lat')
ns = st.selectbox('', ('N', 'S'))
longi = st.number_input('Enter long')
ew = st.selectbox('', ('E', 'W'))

if 0<=lat<=90 and 0<=longi<=180:
    if ns == 'S':
        lat = -lat
    if ew == 'W':
        if longi>0:
            longi = 360-longi
    a = (get_data(all_df,lat,longi))
    a = a.iloc[:,[2,3,4,7,8]]
    st.write(a)
    prediction = model.predict([a])
    prediction = float(prediction)*100
    prediction = round(prediction,3)
    st.write(f'There is a {prediction}% chance that a solar plant built there will be successful')
else:
    st.write("Enter valid parameters")
