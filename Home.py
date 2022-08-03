import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import requests



# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="thinkCircle AI by Khaled", page_icon=":tada:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
img_profile_pic = Image.open("images/tc_profile_pic.png")
img_web_scraper = Image.open("images/tc_web_scraper.png")
img_real_estate = Image.open("images/tc_real_estate.png")
img_streamlit = Image.open("images/tc_streamlit.png")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")

# ---- HEADER SECTION ----
with st.container():
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_profile_pic)
    with text_column:
        st.subheader("Hello :wave: I am Khaled")
    
    

    st.title("A Machine Learning Engineer From Australia")
    st.write(
        "I am passionate about learning and applying data science, machine learning & general programming to solve real life problems."
    )
    st.write("[Find me here >](https://www.linkedin.com/in/stevehajjaj/)")

# ---- WHAT I DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("##")
        st.write(
            """
            On my Web page I am creating various Machine Learning, Data Analytics & General automation based projects in the following fields:
            - Machine Learning Regression & Classifcation models utilizing Deep Neural Networks
            - Computer Vision using Convolutional neural networks
            - Natual Language Processing using Transformer models such as Bidirectional Encoder Representations from Transformers (BERT)
            - Application Programming Interface (API) & ML model Serving such as Tensorflow Serving
            - Automation projects such as Web scraping for Data collection & automated report preparation & email sending.
            - Data Visualization & reporting
            - MLOps  utilizing pipeline framework such as Google created Kubeflow, Airbnb created Apache Airflow & MLflow.
            
            """
        )
        st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

# ---- PROJECTS ----
with st.container():
    st.write("---")
    st.header("My Projects")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_web_scraper)
    with text_column:
        st.subheader("DATA DATA DATA.....& more DATA!")
        st.write(
            """
            So How Do We Get Meaningful Data In The First Place?
            Create a Python based Web Scraping App offcourse!
            In this example, I created an application that extracts all the house details from a well known Australian
            real estate website. The python program is based on Python BeautifulSoup. 
            """
        )
        st.markdown("[See Code...](https://github.com/think-circle/ML-Web-Scraper.git)")
with st.container():
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_real_estate)
    with text_column:
        st.subheader("TENSORFLOW AUSTRALIAN REAL ESTATE PRICE PREDICTION ML")
        st.write(
            """
           Tensorflow Deep Neural Network Regression to estimate the price of a home in Australian Real Estate, along with
           Tensorflow Serving utilizing docker container.
            """
        )
        st.markdown("[See Code...](https://github.com/think-circle/MLrealestate.git)")


with st.container():
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_streamlit)
    with text_column:
        st.subheader("HEROS ARE LIT..STREAMLIT & HEROKU TO RESCUE ML ENGINEERS")
        st.write(
            """
           Streamlit is a handsome  web UI based on Python that can be hosted on Heroku with Ease that allows you to focus
           ML Engineering rather than being a fully fledged Front End Developer.
            """
        )
        st.markdown("[See Code...](https://github.com/think-circle/ML-Streamlit-UI.git)")


# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/steve_h_112@hotmail.com" method="POST">
        <input type="hidden" name="_captcha" value="True">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()

    







