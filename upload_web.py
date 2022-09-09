import requests
import os
import download_web
import time
import subprocess

while True:
    #camera_path = 'D:/flir/'
    #camera_path = './img_mouse/'
    #camera_path = './img_hand/'
    camera_path = '/run/user/1000/gvfs/mtp:host=FLIR_Systems_FLIR_Camera/Images/DCIM/100_FLIR/'
    flir_camera_images = os.listdir(camera_path)
    print(flir_camera_images)
    
    result = subprocess.check_output(['sudo', 'uhubctl', '-a', 'off', '-p', '4', '-l', '1-1'])
    print(result)
    result2 = subprocess.check_output(['sudo', 'uhubctl', '-a', 'on', '-p', '4', '-l', '1-1'])
    print(result2)
    time.sleep(10)

    
    drive_filelist = download_web.drive_filelist('admin')

    for filename in flir_camera_images:
        if filename in drive_filelist:
            print(filename, 'already exists!')
        else:
            path = camera_path+filename
            files = {'file':open(path, 'rb')}
            response = requests.post("http://34.64.107.120:8080/flirupload", files=files)
            print(filename, response.text)
    
    time.sleep(5)