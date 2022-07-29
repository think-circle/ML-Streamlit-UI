import pandas as pd
import numpy as np
from scipy import stats
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as gd

def get_coordinates(suburb):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(f"{suburb},Victoria,Australia")
    return getLoc.latitude,getLoc.longitude

def calc_distance(suburb):
    lat0,long0 = get_coordinates("Melbourne")
    lat1,long1 = get_coordinates(suburb)
    dist = round(gd((lat0, long0), (lat1, long1)).km,2)
    return dist

def normalize(df):
    num_feat = ['Bedrooms','Bathrooms','Cars','Area','Latitude','Longitude','Distance']
    result = df.copy()
    
    for feature_name in num_feat:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

def transform_input(inp_list):
    num_feat = ['Bedrooms','Bathrooms','Cars','Area','Latitude','Longitude','Distance']
    cat_feat = ['Suburb','Type','Method']
    drop_feat = ['Street','Address','State','Postcode','Date','Agent','Price']
    #READ IN DATA
    df= pd.read_csv('data/Melbourne/Melbourne_template.csv')
    df = df.dropna(how='any',axis=0)

    # Drop features that are not required
    if set(drop_feat).issubset(df.columns):
        df = df.drop(drop_feat, axis = 1)



    
    for feat in cat_feat:
        dummy = pd.get_dummies(df[feat], prefix=feat)
        df = pd.merge(left=df,right=dummy,left_index=True,right_index=True,)
    #print(df[num_feat].info())
    df = df.drop(cat_feat, axis = 1)
    df = df[(np.abs(stats.zscore(df[num_feat])) < 3).all(axis=1)]
    df = normalize(df)
    print(df.info())
    input = df.to_numpy().tolist()[0:1]

    return {"instances": input}