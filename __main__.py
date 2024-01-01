from src.api.connect import Connect
from src.api.database import Database
from src.api.table import Table
from src.api.table_query_default import TableQueryDefault

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
    table_default_class = TableQueryDefault()
    table_class = Table(connection_class,table_default_class)

    database = 'datasets_2'

    #try:

    #print(database_class.create_database("emotion"))
    if(not database_class.database_exist(database)):
        database_class.create_database(database)

    database_class.use_database(database)

    if(not table_class.table_exist('emotion')):
        table_class.create_table(table='emotion',info_= 'create_table_img_dataset') # type: ignore
    if(not table_class.table_exist('emotion_inline')):
        table_class.create_table(
            table='emotion_inline',
            info_={
                "id": ('INT','AUTO_INCREMENT','PRIMARY KEY'),
                "name": ('VARCHAR(255)'),
                "format" : ('VARCHAR(15)'),
                "width": ('MEDIUMINT UNSIGNED'),
                "height" : ('MEDIUMINT UNSIGNED'),
                "image" : ('LONGBLOB')
            } # type: ignore
        )
        
    from time import time
    info = {
        "name": f"me{str(int(time()))}",
        "format": "jpeg",
        "width": 120,
        "height": 240,
        "image": read_bytes_img("tmp/me.jpeg")
    }
        
    #table_class.send_values_table("emotion",info=info)
    image = table_class.get_value_table("emotion","fetch_image",1,column_name=["image"],filter_={"name":"me1704135018"})[0][0]
    image = decode_bytes_img(image)
    #image = image.resize((224,224))
    image.show()
    #print(image)
        
    # except Exception as e:
    #     print(e)

    # finally:
    #     #sender.da
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

