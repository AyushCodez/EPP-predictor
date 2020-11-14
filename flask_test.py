import numpy as np
import pandas as pd
import pickle
import base64
from flask import Flask, jsonify

app = Flask("EPP-Predictor")
# CORS(app, resources={r"/": {"origins": "*"}})

filename = 'finalized_model_xgboost.sav'
model = pickle.load(open(filename, 'rb'))

all_df = pd.read_csv(r'/Users/Pranjal/Desktop/LatestProjects/EPP-predictor/all_data_final.csv')

def get_data(db,lat,longi):
    lat = round(lat*4)/4
    longi = round(longi*4)/4
    df = db[db["latitude"] == lat]
    df = df[df["longitude"] == longi]
    return df

# lat = st.number_input('Enter lat')
# ns = st.selectbox('', ('N', 'S'))
# longi = st.number_input('Enter long')
# ew = st.selectbox('', ('E', 'W'))

@app.route('/<lat>/<longi>')
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def predictor(lat, longi):
    lat = float(lat)
    longi = float(longi)
    print(lat, longi)
    if -90<=lat<=90 and -180<=longi<=180:

        longi = 180 + longi
        if longi > 359.75:
            return "Enter valid parameters"
        
        print(lat,longi)
        a = (get_data(all_df,lat,longi))

        a = a.iloc[:,[2,3,4,5,6,7,8]]
        prediction = model.predict(a)
        prediction = float(prediction)*100
        prediction = round(prediction,3)

        r = jsonify({"text": f'There is a {prediction}% chance that a solar plant built there will be successful'})
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
    else:
        r = jsonify({"text": "Enter valid parameters"})
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
