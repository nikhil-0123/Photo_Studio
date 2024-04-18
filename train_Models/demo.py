import numpy as np
from PIL import Image
import tensorflow as tf

# Load the trained Zero-DCE model
zero_dce_model = tf.keras.models.load_model('low_light_enhencer.h5')

# Function to preprocess the image
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((256, 256))  # Resize image to match model input size
    image = np.array(image) / 255.0   # Normalize pixel values
    return image

# Function to enhance low-light image
def enhance_low_light_image(image_path, save_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Perform inference to get enhanced image
    enhanced_image = zero_dce_model.predict(np.expand_dims(preprocessed_image, axis=0))[0]
    # Ensure the enhanced image is in the correct data type and shape
    enhanced_image = np.clip(enhanced_image * 255, 255, 255).astype(np.uint8)
    enhanced_image = Image.fromarray(enhanced_image)
    
    # Save the enhanced image
    enhanced_image.save(save_path)
    
    print("Enhanced image saved successfully.")

# Path to the low-light image you want to enhance
# low_light_image_path = '10.png'

# # Path to save the enhanced image in the current directory
# enhanced_image_save_path = 'enhanced_image.png'

# # Enhance the low-light image and save it
# enhance_low_light_image(low_light_image_path, enhanced_image_save_path)
