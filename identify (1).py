
import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf



# Define the monument identification page
def identify_page():
    st.title("Identify Monument")
    st.write("Upload an image of the monument you want to identify.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file,caption='Uploaded Image',use_column_width=True)
        st.write("")
        st.write("Identifying...")

        # Load pre-trained VGG16 model without the top classification layers
        vgg_model = VGG16(weights='imagenet', include_top=False)

        # Load your trained model
        model = tf.keras.models.load_model('/content/drive/MyDrive/model.h5')

        feat = np.load("/content/drive/MyDrive/features.npy")
        labels = np.load("/content/drive/MyDrive/labels.npy")

        # Assuming 'labels' is defined and contains the class names
        label_encoder = LabelEncoder()
        encoder_data = label_encoder.fit_transform(labels)

        # Convert the file to an image
        img = image.load_img(uploaded_file, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)

        # Extract features using VGG16 model
        img_data = preprocess_input(img_data)
        features = vgg_model.predict(img_data)
        test_features = features.flatten()

        # Reshape features and predict
        test_features_reshaped = test_features.reshape((-1, 7, 7, 512))
        predictions = model.predict(test_features_reshaped)
        predicted_index = np.argmax(predictions)
        predicted_class_encoded = label_encoder.inverse_transform([predicted_index])

        # Display results
        st.write("Predicted Monument:", predicted_class_encoded[0])

