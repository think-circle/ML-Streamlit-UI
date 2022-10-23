
import streamlit as st
import time
from PIL import Image
import numpy as np
from io import BytesIO
import requests

st.header('POTATO DISEASE CLASSIFICATION')


c1,c2,c3 = st.columns([2,8,2])
c1.markdown('\n')
c1.image('https://img.freepik.com/premium-vector/cute-potato-farmer-cartoon-illustration-vegetable-cartoon-vector-illustration_290315-688.jpg?w=2000')


endpoint = "https://tf-serve-model1.herokuapp.com/v1/models/model/versions/1:predict"
class_names = ["Early Blight", "Late Blight", "Healthy"]

predicted_class = ''
confidence = ''
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
    confidence = 100*round(np.max(prediction),2)



c3.metric(label = 'Predicted Classification', value = predicted_class ,delta = confidence +'%')



with st.expander('Click here to see result:'):
    
    if uploaded_image is not None:
        st.write('CLASSIFICATION: '+predicted_class)
        st.write('CONFIDENCE: '+confidence +'%')
        st.image(uploaded_image)
    else:
        st.write('No Image uploaded')
        st.image('https://img.freepik.com/premium-vector/cute-potato-farmer-cartoon-illustration-vegetable-cartoon-vector-illustration_290315-688.jpg?w=2000')
       
          


    





