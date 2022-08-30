import requests
import json
import wget
import os

def drive_filelist(username: str) -> list:
    response = requests.get("http://220.149.88.84:8080/flir/" + username)
    filelist = response.json()
    return filelist

def download_from_web(username: str, down_path: str):
    client_filelist = os.listdir(down_path)
    filelist = drive_filelist(username)
    for filename in filelist:
        if filename in client_filelist:
            pass
        else:
            response = wget.download("http://220.149.88.84:8080/download/admin/"+filename, './download_web/'+filename)


if __name__ == '__main__':
    download_from_web('admin', './download_web')