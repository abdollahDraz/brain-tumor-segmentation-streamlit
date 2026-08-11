import streamlit as st
import os
os.environ["SM_FRAMEWORK"] = "tf.keras"

import tensorflow as tf
import segmentation_models as sm
import cv2
import numpy as np
from huggingface_hub import hf_hub_download


BACKBONE = "resnet34"           # Encoder
preprocess_input = sm.get_preprocessing(BACKBONE)


# loading Model
model_path = hf_hub_download(
    repo_id="abdollah111/brain-tumor-segmentation",
    filename="best_model.keras"
)

model = tf.keras.models.load_model(
    model_path,
    compile=False
)





# Page Configuration

st.set_page_config(
    page_title="Brain Tumor Segmentation",
    page_icon="🧠",
    layout="wide"
)



# Main Title

st.title("🧠 Brain Tumor Segmentation")



# describtion

st.markdown('''
### AI-powered brain tumor segmentation from MRI images using Deep Learning.

### Tumor Types :

- Glioma Tumor
- Pituitary tumor
- Meningioma Tumor
''')



st.divider()



# upload image
st.warning(
        "⚠️ The MRI image should contain one of the following types of tumors: "
        "Glioma Tumor, Pituitary Tumor, or Meningioma Tumor."
    )
image_uploaded = st.file_uploader("📤 Upload MRI Image",
                                  type=["png", "jpg", "jpeg"],
                                  help="Upload an image as PNG, JPG or JPEG"
                                  )



# Segementation button

mask = None
if image_uploaded is not None:
    if st.button("🔍 Segment Tumor"):
        st.write("Button Clicked")
# Preprocecessing input MRI image
        image_bytes = image_uploaded.read()                         # reading image as Bytes
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)  # Convert Image_bytes to image array
        image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)     # convert image array to Opencv image
        image = cv2.resize(image, (256, 256))   # resize
        image = image[..., np.newaxis]         # channel dim
        image = np.repeat(image, 3, axis=-1)   # change num of channels
        image = preprocess_input(image)        # preprocessing of Encoder
        image = np.expand_dims(image, axis=0)  # batch dim
        prediction = model.predict(image)
        mask = ((prediction[0] > .5).astype(np.uint8))
# test uploaded

if image_uploaded is not None:
    st.image(image=image_uploaded, caption="Uploaded MRI Image")


st.divider()


# layout of result
col1, col2 = st.columns(2)
with col1:
      st.subheader("Original MRI")

      if image_uploaded is not None:
        st.image(image=image_uploaded, caption="Original Image")

with col2:
      st.subheader("Predicted Segmentation Mask")
      if mask is not None:
          st.image(mask*255, caption="Predicted Mask")

