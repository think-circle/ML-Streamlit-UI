import streamlit as st
from utils import calc_distance,get_coordinates
import requests
import json
from datetime import date
from PIL import Image
from constants import Melbourne_suburbs,Sydney_suburbs,Brisbane_suburbs,Adelaide_suburbs,Perth_suburbs



city_list = ["Melbourne", "Sydney","Brisbane","Perth","Adelaide","Hobart"]

city = st.sidebar.selectbox("Choose a city",city_list  )
img_city = Image.open(f"images/{city}.png")

def show_predict_page():
    col1, col2, col3 = st.columns([1,3,1])

    with col1:
     st.write("")

    with col2:
     st.subheader(f"{city} House Price Estimator")
     st.image(img_city)

    with col3:
     st.write("")
    
    
    st.write("""### Please fill in the detail below:""")
    if city == 'Melbourne':
        suburbs = Melbourne_suburbs
    elif city == 'Sydney':
        suburbs = Sydney_suburbs
    elif city == 'Brisbane':
        suburbs = Brisbane_suburbs
    elif city == 'Perth':
        suburbs = Perth_suburbs
    elif city == 'Adelaide':
        suburbs = Adelaide_suburbs

    Type = ('House', 'Townhouse', 'Apartment ')
    Method = ('auction','private treaty')
   
    suburb = st.selectbox("Suburb", suburbs)
    property_type = st.selectbox("Type of Property", Type)
    method = st.selectbox("Method of Sale", Method)

    rooms = st.slider("Number of Bedrooms", 1, 5, 3)
    bathrooms = st.slider("Number of Bathrooms", 1, 4, 2)
    cars = st.slider("Number of car spots", 0, 4, 2)
    area = st.slider("Land size", 0, 3700, 445)
 
    ok = st.button("Calculate Price")

    # Calculation of distance,latitude,longitude & year
    distance = calc_distance(suburb, city)
    latitude,longitude = get_coordinates(suburb,city)
    year = date.today().year
    
    if ok:
        input_dict = {'Suburb':suburb,'Type': property_type,'Method': method,'Bedrooms':  rooms, 'Bathrooms':  bathrooms, 'Cars':  cars, 'Area':  area,'Latitude':  latitude,'Longitude':  longitude,'Distance':  distance, 'Year':  year}
        data = {"instances": [input_dict]}
        
        vers = city_list.index(city)+1
        r = requests.post(url=f"https://tf-serve-model.herokuapp.com/v1/models/model/versions/{vers}:predict", data=json.dumps(data))
        #r = requests.post(url="http://localhost:8601/v1/models/real_estate_price_est:predict", data=json.dumps(data))
        print(r.text)
        pred = r.json()["predictions"][0][0]
        
        price = "${:,.2f}".format(pred)
        st.subheader(f"The estimated house price is {price}")



show_predict_page()
