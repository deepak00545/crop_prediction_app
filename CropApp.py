import streamlit as st
import pickle as pkl
import numpy as np
import pandas as pd
loaded_model=pkl.load(open("Crop_NIT.pkl",'rb'))
state=pkl.load(open('Crop_State.pkl','rb'))

fi=set(state["STATE_UT_NAME"])

st.markdown("<h2>Crop Predictor</h2>",unsafe_allow_html=True)
n=st.text_input("Enter % Nitrogen")
k=st.text_input("Enter % Potassium")
p=st.text_input("Enter % Phosphorus")
month=(1,2,3,4,5,6,7,8,9,10,11,12)
month=list(range(1,len(month)+1))
monthnum=st.selectbox("Month number",month)
statename=st.selectbox("State",fi)

import json
import urllib.request

def get_weath(city):
    res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                city+'&appid=764197b2d0a6b547cda5451c97546cf4').read()
    json_data = json.loads(res)
    data = {
        "code": str(json_data['sys']['country']),
        "coor": str(json_data['coord']['lon'])+' '+str(json_data['coord']['lat']),
        "tem": str(json_data['main']['temp'])+'K',
        "tem1": int(json_data['main']['temp'])-273,
        "tem2": int(json_data['main']['feels_like'])-273,
        "pre": str(json_data['main']['pressure']),
        "hum": str(json_data['main']['humidity'])
    }
    return data

# state_N_P_K={'ANDHRA PRADESH':{'N':3.7,'P':1.825,'K':1},'KARNATAKA':{'N':203,'P':1.425,'K':1},'KERALA':{'N':1.225,'P':0.625,'K':1},
#              'TAMIL NADU':{'N':1.9,'P':0.775,'K':1},'PONDICHERRY':{'N':2.875,'P':0.9,'K':1},'ANDAMAN And NICOBAR ISLANDS':{'N':2.167,'P':1.7,'K':1},
#              'GUJARAT':{'N':6.3,'P':2.675,'K':1},'MADHYA PRADESH':{'N':8.875,'P':5.675,'K':1},'CHATISGARH':{'N':4.8,'P':2.375,'K':1},
#              'MAHARASHTRA':{'N':2.95,'P':1.8,'K':1},'RAJASTHAN':{'N':27.325,'P':11.625,'K':1},'GOA':{'N':1.6,'P':1.175,'K':1},
#              'DADAR NAGAR HAVELI':{'N':15,'P':10.3,'K':1},'HARYANA':{'N':27.075,'P':8.275,'K':1},'PUNJAB':{'N':23.85,'P':6.75,'K':1},'UTTAR PRADESH':{'N':11.85,'P':3.825,'K':1},
#              'UTTARANCHAL':{'N':9.85,'P':2.745,'K':1},'HIMACHAL':{'N':3.125,'P':0.975,'K':1},'JAMMU AND KASHMIR':{'N':8.05,'P':3.025,'K':1},
#              'ARUNACHAL PRADESH':{'N':5.73,'P':2.367,'K':1},'BIHAR':{'N':6.95,'P':1.8,'K':1},'JHARKHAND':{'N':7.45,'P':3.825,'K':1},
#              'ORISSA':{'N':3.65,'P':1.8,'K':1},'WEST BENGAL':{'N':1.85,'P':1.15,'K':1},'ASSAM':{'N':1.9,'P':0.825,'K':1},'TRIPURA':{'N':2.975,'P':1.2,'K':1},'MANIPUR':{'N':15.175,'P':2.35,'K':1},
#              'MEGHALAYA':{'N':6.9,'P':2.75,'K':1},'MIZORAM ':{'N':1.9,'P':1.867,'K':1},'NAGALAND':{'N':3.825,'P':3.233,'K':1},
#              'DELHI':{'N':2.7,'P':1,'K':1},'SIKKIM':{'N':0.688,'P':0.38,'K':1},'CHANDIGARH':{'N':25.4625,'P':7.5125,'K':1}}


df_rain = pd.read_csv("TriNit/district wise rainfall normal.csv")
gh=np.array(df_rain)

li=[]
for i in gh:
    if i[0]==statename.upper():
        li.append(i[1])

df_rain.drop(["STATE_UT_NAME","Jan-Feb","Mar-May","Jun-Sep","Oct-Dec"],axis=1,inplace=True)
districtname=st.selectbox("District",li)

gh=np.array(df_rain)
def get_rainfall(dist,month_no):
    dist=dist.upper()
    for i in gh:
        if i[0]==dist:
            return i[month_no]

if st.button("Check"):
    rain_fall = get_rainfall(districtname,monthnum)
    weath = get_weath(districtname)
    ph_mod = pkl.load(open("PH.pkl",'rb'))
    temp,humid = weath["tem1"],float(weath["hum"])
    arr_ph=[[n,p,k,temp,humid,rain_fall]]
    arr_ph=np.array(arr_ph)
    ph= ph_mod.predict(arr_ph)

    arr =[[n,p,k,temp,humid,ph,rain_fall]]
    arr = np.array(arr)

    p= loaded_model.predict(arr)
    st.info(f"We can grow the Crop: {p}")