from rembg import remove
import cv2
import os
currentDir = os.path.dirname(__file__)

def removeBackground(filename,image_src):
    results_dir = os.path.join(currentDir, 'Result/bg_result/')
    input_path = filename
    images = image_src.split(".")[0]
    output_path = results_dir+images+".png"
    oout = images+".png"
    input = cv2.imread(input_path)
    output = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=50)
    cv2.imwrite(output_path, output)
    return oout