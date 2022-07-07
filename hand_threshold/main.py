import os
import cv2
from matplotlib import pyplot as plt

# file names of flir thermal cameras are followed this format:
# 'FLIR0000.jpg'
# so it need to be parsed with number sections
def convert_filename_to_num(filename: str) -> int:
    # int() convert '0001' -> 1
    # so if any kind of index like '0180', '0010' can convert correctly 180, 10
    return int(filename[4:8])

# it has const hands_thresh: 180
# this value divide body temperature and temperature of things in rooms well
# it has function of cv2.threshold using binarization, return result img matrix
def hands_threshold(img):
    hands_thresh = 180
    ret, thresh = cv2.threshold(img,hands_thresh,255,cv2.THRESH_BINARY)
    return thresh

# my images path and file list
path = './img/'
img_list = os.listdir(path)
print('img_list: ', img_list)

# divide thermal and digital images using odd, even
# 'FLIR0001.jpg' and 'FLIR0002.jpg' are pair of images included same things
# odd index has a thermal image, even index has a digital image
thermal_img_list = list()
digital_img_list = list()
for img_name in img_list:
    if (convert_filename_to_num(img_name) % 2 == 1):
        thermal_img_list.append(img_name)
    else:
        digital_img_list.append(img_name)
print('thermal_img_list: ', thermal_img_list)
print('digital_img_list: ', digital_img_list)

# results list has original images and binarization images
# plot images at the same time using subplot function of matplotlib
results = list()
for thermal_img_name in thermal_img_list:
    # it returns a rgb image matrix
    thermal_img = cv2.imread(path+thermal_img_name)
    # it returns grayscale image matrix
    gray_img = cv2.imread(path+thermal_img_name, cv2.IMREAD_GRAYSCALE)
    results.append(thermal_img)
    results.append(hands_threshold(gray_img))

for i in range(len(results)):
    plt.subplot(int(len(results)/2),2,i+1)
    plt.imshow(results[i])
    plt.xticks([]),plt.yticks([])
plt.show()