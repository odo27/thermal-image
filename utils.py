import os

# file names of flir thermal cameras are followed this format:
# 'FLIR0000.jpg'
# so it need to be parsed with number sections
def convert_filename_to_num(filename: str) -> int:
    # int() convert '0001' -> 1
    # so if any kind of index like '0180', '0010' can convert correctly 180, 10
    return int(filename[4:8])


# my images path and file list
def img_list(img_path: str ='./img/') -> (str, list):
    contents = os.listdir(img_path)
    return img_path, contents


# divide thermal and digital images using odd, even
# 'FLIR0001.jpg' and 'FLIR0002.jpg' are pair of images included same things
# odd index has a thermal image, even index has a digital image
def divide_thermal_digital(contents: list) -> (list, list):
    thermal_contents = list()
    digital_contents = list()
    for img_name in contents:
        if (convert_filename_to_num(img_name) % 2 == 1):
            thermal_contents.append(img_name)
        else:
            digital_contents.append(img_name)
    return thermal_contents, digital_contents