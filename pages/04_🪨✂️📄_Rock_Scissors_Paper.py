
import streamlit as st
import time
from PIL import Image
import numpy as np
from io import BytesIO
import requests

st.header('ROCK 🪨 SCISSORS✂️ PAPER📄 GAME')


c1,c2,c3 = st.columns([2,8,2])
c1.markdown('\n')
c1.image('https://www.wikihow.com/images/thumb/3/33/Play-Rock%2C-Paper%2C-Scissors-Step-5-Version-3.jpg/v4-460px-Play-Rock%2C-Paper%2C-Scissors-Step-5-Version-3.jpg')


endpoint = "https://tf-serve-model1.herokuapp.com/v1/models/model/versions/1:predict"
class_names = ["rock", "scissors", "paper"]
predicted_class = ''
confidence = ''
# Camera with Porgress bar
camera_image = c2.camera_input('Take a Photo!!!')
if camera_image is not None:
    progress_bar = c2.progress(0)
    for percent_comp in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_comp+1)
    c2.success('Photo taken successfully')
   
    image = np.array(Image.open(BytesIO(camera_image.read())))
    img_batch = np.expand_dims(image, 0)
    json_data = {
        "instances": img_batch.tolist()
    }

    response = requests.post(endpoint, json=json_data)
    prediction = np.array(response.json()["predictions"][0])

    predicted_class = class_names[np.argmax(prediction)]
    confidence = 100*round(np.max(prediction),2)


c3.metric(label = 'Predicted Classification', value = predicted_class ,delta = confidence)



with st.expander('Click to see more info'):
    st.write('Currently Selected image for prediction:')
    if camera_image is not None:
        st.image(camera_image)
    else:
        st.write('No Image taken')
        st.image('https://thumbs.dreamstime.com/z/funny-ugly-face-154818490.jpg')
       
          


    





