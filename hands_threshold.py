import cv2
import utils
import numpy as np
from matplotlib import pyplot as plt

# it has const hands_thresh: 180
# this value divide body temperature and temperature of things in rooms well
# it has function of cv2.threshold using binarization, return result img matrix
def hands_threshold(img: np.array, hands_thresh:int = 180) -> np.array:
    ret, thresh = cv2.threshold(img,hands_thresh,255,cv2.THRESH_BINARY)
    return thresh


# results list has original images and binarization images
# plot images at the same time using subplot function of matplotlib
def draw_threshold(img_path: str, thermal_contents: list):
    results = list()
    for thermal_img_name in thermal_contents:
        # it returns a rgb image matrix
        thermal_img = cv2.imread(img_path+thermal_img_name)
        # it returns grayscale image matrix
        gray_img = cv2.imread(img_path+thermal_img_name, cv2.IMREAD_GRAYSCALE)
        results.append(thermal_img)
        results.append(hands_threshold(gray_img))

    for i in range(len(results)):
        plt.subplot(int(len(results)/2),2,i+1)
        plt.imshow(results[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

if __name__ == '__main__':
    img_path, contents = utils.img_list()
    thermal_contents, digital_contents = utils.divide_thermal_digital(contents)
    draw_threshold(img_path, thermal_contents)