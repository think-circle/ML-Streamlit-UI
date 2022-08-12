import streamlit as st
import pandas as pd
import plotly.express as px
from utils import reduce_mem_usage


city = st.sidebar.selectbox("Choose City", ("Melbourne", "Sydney","Brisbane","Perth","Adelaide"))
view = st.sidebar.selectbox("Choose View to display", ('Table','Map','Suburb Price Comparison','Top Suburbs','Bottom Suburbs'))

if "shared" not in st.session_state:
   st.session_state["shared"] = True


#@st.cache
def load_data():
    df = pd.read_csv(f"data/{city}/{city}_area.csv",usecols=['Street','Suburb', 'Date', 'Price','Area','Latitude','Longitude','Distance'],
    dtype = {'Suburb':'category', 'Price':'int32','Area':'int32', 'Distance':'float16',  })
    #df = reduce_mem_usage(df)
    df['Date']= pd.to_datetime(df.Date, infer_datetime_format=True)
    df['Date'] = df['Date'].dt.strftime('%m-%d-%Y')
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    

    return df



def show_explore_page(view , df,total_records):
    st.title(f"{city.upper()} REAL ESTATE DATA VISUALISATION")


    # ---- TABULAR VIEW OF DATA ----
    if view == 'Table':
        with st.container():
            st.write(f"Tabular Data for {city} Real Estate")
            st.write("##")
            st.write(df)
    


    # ---- MAP VIEW OF DATA ----
    if view == 'Map':
        with st.container():
            st.write("---")
            st.write("MAP VIEW OF ALL PROPERTIES")
            st.write("##")
            suburb_options = df['Suburb'].unique().tolist()
            suburb = st.multiselect('Which suburbs would you like to view on the map?',suburb_options,suburb_options[0])
            df = df[df['Suburb'].isin(suburb)]
            df['Suburb'] = df['Suburb'].astype(str)
            df = df.sort_values('Year', ascending=True)
            
            # import_records = st.sidebar.slider("Maximum Number of Records to import", 0, total_records , 20000)
            # df = df[0:import_records]
            price_range = st.slider('Select Price range $:',int(df['Price'].min().item()) ,int(df['Price'].max().item()) , (int(df['Price'].min().item()),  int(df['Price'].max().item())))
            st.write('Minimum Price Selected $', price_range[0] )
            st.write('Maximum Price Selected $', price_range[1] )
            
            area_range = st.slider('Select Area range in SQM',int(df['Area'].min().item()) ,int(df['Area'].max().item()) , (int(df['Area'].min().item()),  int(df['Area'].max().item())))
            st.write('Minimum Area Selected SQM', area_range[0])
            st.write('Maximum Area Selected SQM', area_range[1])

            year_range = st.slider('Select Year range',int(df['Year'].min().item()) ,int(df['Year'].max().item()) , (int(df['Year'].min().item()),  int(df['Year'].max().item())))
            st.write('Minimum Year', year_range[0] )
            st.write('Maximum Year', year_range[1] )
            
            df = df[(df.Price >= price_range[0]) & (df.Price <= price_range[1]) & (df.Area >= area_range[0]) & (df.Area <= area_range[1]) & (df.Year >= year_range[0]) & (df.Year <= year_range[1])]
            showing_records = len(df.index)
            fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",color="Suburb", size="Price",zoom=8,hover_name = 'Price' , hover_data= ['Street','Suburb','Price','Area','Date','Latitude','Longitude'],
                  title = f"{city}  Map View",animation_frame = 'Year', animation_group = 'Suburb')
                  #animation_frame = 'Date', animation_group = 'Suburb',
            fig.update_layout(mapbox_style = 'open-street-map')
            fig.update_layout(margin = {'r':0 , 't': 50, 'l':0 , 'b':10})
            fig.update_layout(width = 800,height = 600)
            # fig.update_layout(showlegend = False)
            st.write(fig)

            st.write(f"Showing {showing_records} records out of a total {total_records} records for {city}")
            for suburb, count in df['Suburb'].value_counts().items():
                st.write(f"{suburb}: {count} PROPERTIES")

    


    # ----  BAR CHART COMPARISON OF DIFFERENT SUBURBS ----
    if view == 'Suburb Price Comparison':
        with st.container():
            st.write("---")
            st.write("AVERAGE PRICE OF SUBURB COMPARISON")
            st.write("##")
            suburb_options = df['Suburb'].unique().tolist()
            suburb = st.multiselect('Which suburbs would you like to compare?',suburb_options,suburb_options[0])
            df = df[df['Suburb'].isin(suburb)]
            df['Suburb'] = df['Suburb'].astype(str)
            
            fig = px.histogram(df,x = 'Suburb',y='Price', color = 'Suburb', barmode='group',histfunc='avg',title="Average Price per Suburb",animation_frame = df['Year'], animation_group = 'Suburb')
            st.write(fig)


    # ----  BAR CHART VIEW OF TOP SUBURBS ----
    if view == 'Top Suburbs':
        with st.container():
            st.write("---")
            st.write("TOP SUBURBS MEDIAN CATEGORIES")
            st.write("##")
            max_disp = st.slider("Maximum Number of Suburbs to display", 3, 25, 10)
            category_list = ['Price','Area','Distance']
            category = st.selectbox("Choose Category", category_list)
            if category =='Distance':
                ascending = True
            else:
                ascending = False
            
            df_top = df.groupby('Suburb')[category].median().to_frame().sort_values(by=[category],ascending= ascending).head(max_disp).reset_index()
            df = df[df['Suburb'].isin(df_top.Suburb)]
            df = df.sort_values('Year', ascending=True)
        
            fig = px.histogram(df,x= category,y= df['Suburb'],color = df.Suburb.astype(str),histfunc='avg',orientation="h",title= f"Top {max_disp} Suburbs in {city} in terms of {category}",width=1100,height = 600,
            animation_frame = 'Year', animation_group = df.Suburb.astype(str))
            st.write(fig)
    
    # ----  BAR CHART VIEW OF BOTTOM SUBURBS ----
    if view == 'Bottom Suburbs':
        with st.container():
            st.write("---")
            st.write("TOP SUBURBS MEDIAN CATEGORIES")
            st.write("##")
            max_disp = st.slider("Maximum Number of Suburbs to display", 3, 25, 10)
            category_list = ['Price','Area','Distance']
            category = st.selectbox("Choose Category", category_list)
            if category =='Distance':
                ascending = False
            else:
                ascending = True
            df = df.groupby('Suburb')[category].median().sort_values(ascending= ascending)[0:max_disp]
            fig = px.bar(df,x=category,y= df.index,color = df.index.astype(str), orientation="h",title= f"Bottom {max_disp} Suburbs in {city}",width=1100,height = 600)
            st.write(fig)




    #     st.write(f"""#### Percentage of the Number of Properties Sold out of a Total of  {max_disp1} Suburbs""")
    #     st.pyplot(fig1)
    #     st.write("""#### 
        
    #     """)
  
    # max_disp2 = st.slider("Number of Suburbs to display", 3, 50, 10)
    # st.write(
    #         f"""
    #     #### TOP {max_disp2}: Average Price per Suburb
    #     """
    #     )
    # data = df.groupby("Suburb")["Price"].mean().sort_values(ascending= False)[0:max_disp2].sort_values(ascending= False)
    # st.bar_chart(data)


    # st.write(
    #     """
    # #### Price based on Distance from City
    # """
    # )

    # data = df.groupby(["Distance"])["Price"].mean().sort_values(ascending=True)
    # st.line_chart(data)


df = load_data()
show_explore_page(view, df,len(df.index))


# def downcast_dtypes(df):
#     _start = df.memory_usage(deep=True).sum() / 1024 **2
#     float_cols = [c for c in df if df[c].dtype == "float64"]
#     int_cols = [c for c in df if df[c].dtype in ['int64','int32']]
#     df[float_cols] = df[float_cols].astype(np.float32)
#     df[int_cols] = df[int_cols].astype(np.int16)
#     _end = df.memory_usage(deep=True).sum() / 1024 **2
#     saved = (_start - _end)/ _start*100
#     print(f"Saved {saved:.2f}%")
#     return df

       

    
