import requests
import os
import download_web
import time

while True:
    camera_path = 'D:/flir/'
    flir_camera_images = os.listdir(camera_path)
    print(flir_camera_images)

    drive_filelist = download_web.drive_filelist('admin')

    for filename in flir_camera_images:
        if filename in drive_filelist:
            print(filename, 'already exists!')
        else:
            path = camera_path+filename
            files = {'file':open(path, 'rb')}
            response = requests.post("http://220.149.88.84:8080/flirupload", files=files)
            print(filename, response.text)
    
    time.sleep(100)