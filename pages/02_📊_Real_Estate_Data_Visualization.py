import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


city = st.sidebar.selectbox("Explore Or Predict", ("Melbourne", "Sydney","Brisbane"))

if "shared" not in st.session_state:
   st.session_state["shared"] = True
#st.subheader('Explore Data')
#suburb_list = ['Abbotsford','Aberfeldie','Airport West']
#suburb_chosen = st.sidebar.selectbox("Select a country:",suburb_list)


#@st.cache
def load_data():
    df = pd.read_csv(f"data/{city}/{city}_distance.csv")
    df["FullAddress"] = df['Street'].astype(str) +","+ df["Address"]
   
    return df

df = load_data()

def show_explore_page():
    st.title(f"{city} Real Estate")

    st.write(
        f"""
    ###  Data Statistics Visualisation for {city}
    """
    )
    max_disp1 = st.slider("Maximum Number of Suburb Sample Size", 3, 25, 10)
    data = df["Suburb"].value_counts().sort_values(ascending= False)[0:max_disp1]
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    #ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


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

       

    
