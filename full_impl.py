import streamlit as st
import numpy as np
import pandas as pd
from keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

st.title('EPP predictor')

all_df = pd.read_csv('all_data_final.csv')

def get_data(db,lat,long):
    lat = round(lat*4)/4
    long = round(long*4)/4
    df = db[db["latitude"] == lat]
    df = df[df["longitude"] == long]
    return df

lat = st.number_input('Enter lat')
ns = st.selectbox('', ('N', 'S'))
longi = st.number_input('Enter long')
ew = st.selectbox('', ('E', 'W'))

if 0<=lat<=90 and 0<=longi<=90:
    if ns == 'S':
        lat = -lat
    if ew == 'W':
        longi = -longi
    try:
    	a = (get_data(all_df,lat,longi).iloc[-1])

    except:
        pass

    else:
        a = a.iloc[[2,3,4,7,8]]
        a = list(a.values)
        prediction = model.predict([a])
        prediction = float(prediction)*100
        prediction = round(prediction,3)
        st.write(f'There is a {prediction}% chance that a solar plant built there will be succesfull')
else:
    st.write("Enter valid parameters")
