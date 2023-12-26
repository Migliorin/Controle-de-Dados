from src.api.connect import Connect
from src.api.database import Database

from src.api.utils import read_bytes_img, decode_bytes_img
import cv2

import yaml

def read_configs(path='config.yml')->dict:
    with open(path, 'r') as file:
        prime_service = yaml.safe_load(file)
        file.close()
    return prime_service


if __name__ == '__main__':
    prime_service = read_configs()
    #print(prime_service)
    connection_class = Connect(**prime_service)
    #print(connection_class.connection.is_connected())
    #print(connection_class.create_database("emotion"))
    #print(connection_class.is_open_connection())
    #connection_class.close()
    database_class = Database(connection_class)
    #print(database_class.create_database("emotion"))
    database_class.create_database("datasets")
    #sender.da
    connection_class.close()
    #

    # img = read_bytes_img("me.jpeg")
    # #print(binary_image)
    # print(len(img))
    # decode_img = decode_bytes_img(img,pill=False)
    # print(decode_img)
    # while True:
    #     cv2.imshow('teste',decode_img)
    #     #cv2.imshow("Image", img)
    #     cv2.waitKey(1)

    #cv2.imshow(img_decode)
    #print(img_decode)

