import rembg
from PIL import Image
import os
import requests
from io import BytesIO
currentDir = os.path.dirname(__file__)

def replacecolor(image,color,image_src):
    results_dir = os.path.join(currentDir, 'static/Result/bg_result/')
    output_path = results_dir + image_src
    with open(image, 'rb') as f:
        image_data = f.read()
    transparent_image_data=rembg.remove(image_data, alpha_matting=True, alpha_matting_foreground_threshold=50)
    with open(output_path, 'wb') as f:
        f.write(transparent_image_data)
    image = Image.open(output_path)
    new_bg_color = color 
    new_image = Image.new("RGB", image.size, new_bg_color)
    new_image.paste(image, (0, 0), image)
    new_image.save(output_path)
    return image_src

def replace(image, bg, image_src):
    currentDir = os.getcwd()
    results_dir = os.path.join(currentDir, 'static/Result/bg_result/')
    output_dir = os.path.join(results_dir, image_src)
    with open(image, 'rb') as f:
        image_data = f.read()
    subject = rembg.remove(image_data, alpha_matting=True, alpha_matting_foreground_threshold=50)
    with open(output_dir, 'wb') as f:
        f.write(subject)
    background_img = Image.open(bg)
    input_img = Image.open(output_dir)
    background_img = background_img.resize((input_img.width, input_img.height))
    # masked_dir = os.path.join(currentDir, 'masked/')
    # os.makedirs(masked_dir, exist_ok=True)
    # masked_image_path = os.path.join(masked_dir, image_src)
    background_img.paste(input_img, (0, 0), input_img)
    # background_img.save(masked_image_path)
    background_img.save(output_dir)
    return image_src 