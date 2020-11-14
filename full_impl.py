import streamlit as st
import numpy as np
import pandas as pd
import pickle
import base64

filename = 'finalized_model_xgboost.sav'
model = pickle.load(open(filename, 'rb'))

st.title('EPP predictor')

all_df = pd.read_csv(r'/Users/Pranjal/Desktop/LatestProjects/EPP-predictor/all_data_final.csv')

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
    a = a.iloc[:,[2,3,4,5,6,7,8]]
    prediction = model.predict(a)
    prediction = float(prediction)*100
    prediction = round(prediction,3)
    st.write(f'There is a {prediction}% chance that a solar plant built there will be successful')
else:
    st.write("Enter valid parameters")
