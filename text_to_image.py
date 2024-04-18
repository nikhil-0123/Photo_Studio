from diffusers import StableDiffusionPipeline
import torch
import os
import cv2
import numpy as np

currentDir = os.path.dirname(__file__)
results_dir = os.path.join(currentDir, 'static/Result/generated_images/')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32, device=device)
def text2image(prompt):
    text = prompt.replace(" ", "")
    image = pipe(prompt,512,512,25).images[0]
    output_path = results_dir+text+'.png'
    image_np = np.array(image)
    output = text+'.png'
    if image_np.shape[2] == 4:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
    cv2.imwrite(output_path, image_np)
    return output
