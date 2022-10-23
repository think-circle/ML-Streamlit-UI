
import streamlit as st
import time
from PIL import Image
import numpy as np
from io import BytesIO
import requests

st.header('POTATOE CLASSIFICATION')


c1,c2,c3 = st.columns([2,8,2])
c1.markdown('\n')
c1.image('https://www.nurseryrhymes.org/nursery-rhymes-styles/images/one-potatoe-two-potatoes.jpg')


endpoint = "https://tf-serve-model1.herokuapp.com/v1/models/model/versions/1:predict"
class_names = ["Early Blight", "Late Blight", "Healthy"]


# Upload an Image & make a prediction
uploaded_image  = c2.file_uploader('Choose Image to upload',type = ['jpeg','jpg','png'])
if uploaded_image is not None:
    c2.success('Image uploaded successfully')
    image = np.array(Image.open(BytesIO(uploaded_image.read())))
    img_batch = np.expand_dims(image, 0)
    json_data = {
        "instances": img_batch.tolist()
    }

    response = requests.post(endpoint, json=json_data)
    prediction = np.array(response.json()["predictions"][0])

    predicted_class = class_names[np.argmax(prediction)]
    confidence = np.max(prediction)
    c1.markdown(predicted_class)
    c1.markdown(confidence)

# Camera with Porgress bar
camera_image = c2.camera_input('Take a Photo!!!')
if camera_image is not None:
    progress_bar = c2.progress(0)
    for percent_comp in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_comp+1)
    c2.success('Photo taken successfully')


c3.metric(label = 'Class', value = '60' + '\u00b0'+'C',delta = '3' + '\u00b0'+'C')



with st.expander('Click to see more info'):
    st.write('Currently Selected image for prediction:')
    if uploaded_image is not None:
        st.image(uploaded_image)
    elif camera_image is not None:
        st.image(camera_image)
    else:
        st.write('No Image uploaded or taken')
        st.image('https://www.nurseryrhymes.org/nursery-rhymes-styles/images/one-potatoe-two-potatoes.jpg')
       
          


    





