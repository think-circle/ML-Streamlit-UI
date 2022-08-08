import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


city = st.sidebar.selectbox("Explore Or Predict", ("Melbourne", "Sydney","Brisbane","Perth","Adelaide"))

if "shared" not in st.session_state:
   st.session_state["shared"] = True



#@st.cache
def load_data():
    df = pd.read_csv(f"data/{city}/{city}_area.csv",
    usecols=['Street','Suburb', 'Date', 'Price','Area','Latitude','Longitude','Distance'])
    #dtype = {'Suburb' : 'category'}
    #df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
   
    return df

df = load_data()

def show_explore_page():
    st.title(f"{city.upper()} REAL ESTATE DATA VISUALISATION")
    st.write(
        f"""
    ###  Tabular Data for {city} Real Estate
    """)
    st.write(df)
    st.write("###")
    price_range = st.slider('Select price range $:',int(df['Price'].quantile(0.02).item()) ,int(df['Price'].quantile(0.99).item()) , (int(df['Price'].quantile(0.25).item()),  int(df['Price'].quantile(0.75).item())))
    st.write('Minimum Price Selected $', price_range[0] )
    st.write('Maximum Price Selected $', price_range[1] )
    area_range = st.slider('Select area rane SQM',int(df['Area'].quantile(0.02).item()) ,int(df['Area'].quantile(0.99).item()) , (int(df['Area'].quantile(0.25).item()),  int(df['Price'].quantile(0.75).item())))
    st.write('Minimum Area Selected SQM', area_range[0] )
    st.write('Maximum Area Selected SQM', area_range[1] )
    df1 = df[(df.Price >= price_range[0]) & (df.Price < price_range[1]) & (df.Area >= area_range[0]) & (df.Area < area_range[1])]

    fig = px.scatter_mapbox(df1,lat = df1['Latitude'],lon = df1['Longitude'],zoom =8,color = df1['Price'],size = df1['Price'],text = df1.Street + df1.Suburb, width = 1100, height = 800, title = f"{city} House Prices Map")
    fig.update_layout(mapbox_style = 'open-street-map')
    fig.update_layout(margin = {'r':0 , 't': 50, 'l':0 , 'b':10})
    st.write(fig)
    
    with st.container():
        max_disp1 = st.slider("Maximum Number of Suburb Sample Size", 3, 25, 10)
        data = df["Suburb"].value_counts().sort_values(ascending= False)[0:max_disp1]
        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


        st.write(f"""#### Percentage of the Number of Properties Sold out of a Total of  {max_disp1} Suburbs""")
        st.pyplot(fig1)
        st.write("""#### 
        
        """)
  
    max_disp2 = st.slider("Number of Suburbs to display", 3, 50, 10)
    st.write(
            f"""
        #### TOP {max_disp2}: Average Price per Suburb
        """
        )
    data = df.groupby(["Suburb"])["Price"].mean().sort_values(ascending= False)[0:max_disp2].sort_values(ascending= False)
    st.bar_chart(data)


    st.write(
        """
    #### Price based on Distance from City
    """
    )

    data = df.groupby(["Distance"])["Price"].mean().sort_values(ascending=True)
    st.line_chart(data)




show_explore_page()

       

    
