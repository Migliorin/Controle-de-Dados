import base64
import numpy as np
import cv2
from PIL import Image
import io

import os

def byte_string(image:bytes):
    encoded_string = base64.b64encode(image)
    return encoded_string


def decode_string(bytes_):
    result = base64.decodebytes(bytes_)
    return result

def read_bytes_img(path:str) -> bytes:
    if(not os.path.exists(path)):
        raise Exception(f"Path does not exist: {path}")
    
    with open(path, 'rb') as image_file:
          encoded_string = byte_string(image_file.read())
    return encoded_string

def decode_bytes_img(image:bytes,pill=True):
    image = decode_string(image)
    imageStream = io.BytesIO(image)
    if(pill):
        return Image.open(imageStream)
    else:
        file_bytes = np.asarray(bytearray(imageStream.read()), dtype=np.uint8)
        return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    #print("imageFile.size=%s" % imageFile.size)
    #return imageFile
