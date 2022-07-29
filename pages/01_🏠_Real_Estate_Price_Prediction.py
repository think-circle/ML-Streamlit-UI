import streamlit as st
from utils import transform_input,calc_distance,get_coordinates
import numpy as np
import requests
import json
import pandas as pd



def show_predict_page():
    st.title("Melbourne House Price Prediction")

    st.write("""### We need some information to predict the price""")

    Suburb = ('ABBOTSFORD','ABERFELDIE','AIRPORT WEST','ALBANVALE','ALBERT PARK','ALBION','ALPHINGTON','ALTONA','ALTONA MEADOWS','ALTONA NORTH','ARDEER','ARMADALE','ASCOT VALE','ASHBURTON','ASHWOOD','ASPENDALE','ASPENDALE GARDENS','ATTWOOD','AVONDALE HEIGHTS','BACCHUS MARSH','BALACLAVA','BALWYN','BALWYN NORTH','BAYSWATER','BAYSWATER NORTH','BEACONSFIELD','BEACONSFIELD UPPER','BEAUMARIS','BELLFIELD','BENTLEIGH','BENTLEIGH EAST','BERWICK','BLACK ROCK','BLACKBURN','BLACKBURN NORTH','BLACKBURN SOUTH','BONBEACH','BORONIA','BOTANIC RIDGE','BOX HILL','BRAYBROOK','BRIAR HILL','BRIGHTON','BRIGHTON EAST','BROADMEADOWS','BROOKFIELD','BROOKLYN','BRUNSWICK','BRUNSWICK EAST','BRUNSWICK WEST','BULLEEN','BULLENGAROOK','BUNDOORA','BURNLEY','BURNSIDE','BURNSIDE HEIGHTS','BURWOOD','BURWOOD EAST','CAIRNLEA','CAMBERWELL','CAMPBELLFIELD','CANTERBURY','CARLTON','CARLTON NORTH','CARNEGIE','CAROLINE SPRINGS','CARRUM','CARRUM DOWNS','CAULFIELD','CAULFIELD EAST','CAULFIELD NORTH','CAULFIELD SOUTH','CHADSTONE','CHELSEA','CHELSEA HEIGHTS','CHELTENHAM','CHIRNSIDE PARK','CLARINDA','CLAYTON','CLAYTON SOUTH','CLIFTON HILL','COBURG','COBURG NORTH','COLLINGWOOD','COOLAROO','CRAIGIEBURN','CRANBOURNE','CRANBOURNE NORTH','CREMORNE','CROYDON','CROYDON HILLS','CROYDON NORTH','CROYDON SOUTH','DALLAS','DANDENONG','DANDENONG NORTH','DEEPDENE','DEER PARK','DELAHEY','DERRIMUT','DIAMOND CREEK','DIGGERS REST','DINGLEY VILLAGE','DONCASTER','DONCASTER EAST','DONVALE','DOREEN','DOVETON','EAGLEMONT','EAST MELBOURNE','EDITHVALE','ELSTERNWICK','ELTHAM','ELTHAM NORTH','ELWOOD','EMERALD','ENDEAVOUR HILLS','EPPING','ESSENDON','ESSENDON NORTH','ESSENDON WEST','FAIRFIELD','FAWKNER','FERNTREE GULLY','FITZROY','FITZROY NORTH','FLEMINGTON','FOOTSCRAY','FOREST HILL','FRANKSTON','FRANKSTON NORTH','FRANKSTON SOUTH','GARDENVALE','GISBORNE','GISBORNE SOUTH','GLADSTONE PARK','GLEN HUNTLY','GLEN IRIS','GLEN WAVERLEY','GLENROY','GOWANBRAE','GREENSBOROUGH','GREENVALE','HADFIELD','HALLAM','HAMPTON','HAMPTON EAST','HAMPTON PARK','HAWTHORN','HAWTHORN EAST','HEALESVILLE','HEATHMONT','HEIDELBERG','HEIDELBERG HEIGHTS','HEIDELBERG WEST','HIGHETT','HILLSIDE','HOPPERS CROSSING','HUGHESDALE','HUNTINGDALE','HURSTBRIDGE','IVANHOE','IVANHOE EAST','JACANA','KEALBA','KEILOR','KEILOR DOWNS','KEILOR EAST','KEILOR LODGE','KEILOR PARK','KENSINGTON','KEW','KEW EAST','KEYSBOROUGH','KILSYTH','KINGS PARK','KINGSBURY','KINGSVILLE','KNOXFIELD','KOOYONG','KURUNJANG','LALOR','LANGWARRIN','LOWER PLENTY','LYSTERFIELD','MAIDSTONE','MALVERN','MALVERN EAST','MARIBYRNONG','MCKINNON','MEADOW HEIGHTS','MELBOURNE','MELTON','MELTON SOUTH','MELTON WEST','MENTONE','MERNDA','MICKLEHAM','MIDDLE PARK','MILL PARK','MITCHAM','MONT ALBERT','MONTMORENCY','MONTROSE','MOONEE PONDS','MOORABBIN','MOOROOLBARK','MORDIALLOC','MOUNT EVELYN','MOUNT WAVERLEY','MULGRAVE','MURRUMBEENA','NARRE WARREN','NEWPORT','NIDDRIE','NOBLE PARK','NORTH MELBOURNE','NORTH WARRANDYTE','NORTHCOTE','NOTTING HILL','NUNAWADING','OAK PARK','OAKLEIGH','OAKLEIGH EAST','OAKLEIGH SOUTH','OFFICER','ORMOND','PAKENHAM','PARKDALE','PARKVILLE','PASCOE VALE','PATTERSON LAKES','PLUMPTON','POINT COOK','PORT MELBOURNE','PRAHRAN','PRESTON','PRINCES HILL','RESEARCH','RESERVOIR','RICHMOND','RIDDELLS CREEK','RINGWOOD','RINGWOOD EAST','RINGWOOD NORTH','RIPPONLEA','ROSANNA','ROWVILLE','ROXBURGH PARK','SANDHURST','SANDRINGHAM','SCORESBY','SEABROOK','SEAFORD','SEAHOLME','SEDDON','SKYE','SOUTH KINGSVILLE','SOUTH MELBOURNE','SOUTH MORANG','SOUTH YARRA','SOUTHBANK','SPOTSWOOD','SPRINGVALE','SPRINGVALE SOUTH','ST ALBANS','ST HELENA','ST KILDA','STRATHMORE','STRATHMORE HEIGHTS','SUNBURY','SUNSHINE','SUNSHINE NORTH','SUNSHINE WEST','SURREY HILLS','SYDENHAM','TARNEIT','TAYLORS HILL','TAYLORS LAKES','TEMPLESTOWE','TEMPLESTOWE LOWER','THE BASIN','THOMASTOWN','THORNBURY','TOORAK','TRAVANCORE','TRUGANINA','TULLAMARINE','UPWEY','VERMONT','VERMONT SOUTH','VIEWBANK','WALLAN','WANTIRNA','WANTIRNA SOUTH','WARRANDYTE','WATERWAYS','WATSONIA','WATSONIA NORTH','WATTLE GLEN','WERRIBEE','WEST FOOTSCRAY','WEST MELBOURNE','WESTMEADOWS','WHEELERS HILL','WHITTLESEA','WILLIAMS LANDING','WILLIAMSTOWN','WILLIAMSTOWN NORTH','WINDSOR','WOLLERT','WYNDHAM VALE','YALLAMBIE','YARRA GLEN','YARRAVILLE')

    
    Type = ('House', 'Townhouse', 'Apartment ')
    Method = ('auction','private treaty')
   
    suburb = st.selectbox("Suburb", Suburb)
    type = st.selectbox("Type of Property", Type)
    method = st.selectbox("Method of Sale", Method)

    rooms = st.slider("Number of Bedrooms", 1, 5, 3)
    bathrooms = st.slider("Number of Bathrooms", 1, 4, 2)
    cars = st.slider("Number of car spots", 0, 4, 2)
    area = st.slider("Land size", 0, 3700, 445)
 

    ok = st.button("Calculate Price")

    # 
    distance = calc_distance(suburb)
    latitude,longitude = get_coordinates(suburb)
    
    if ok:
        list = [suburb,type,method,rooms,bathrooms,cars,area,latitude,longitude,distance]
        data = transform_input(list)
        r = requests.post(url="https://tf-serve-model.herokuapp.com/v1/models/model:predict", data=json.dumps(data))
        print(r.text)
        pred = r.json()["predictions"][0][0]
        
        price = "${:,.2f}".format(pred)
        st.subheader(f"The estimated house price is {price}")



show_predict_page()
