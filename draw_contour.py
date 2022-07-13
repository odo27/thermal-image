import extract_temperature
import utils
import numpy as np
from matplotlib import pyplot as plt

# get maplotlib's QuadContourSet using temperature values of celcius unit
def contour(filename: str):
    # np array having temperature values of celcius unit
    temperature_np = extract_temperature.extract_temperature(filename)

    x = np.arange(0, temperature_np.shape[1], 1)
    # prevent a image reversed
    y = np.arange(temperature_np.shape[0], 0, -1)
    X, Y = np.meshgrid(x, y)

    # 32 to 40 celcius using 0.5 spaces
    CS = plt.contour(X, Y, temperature_np, levels=np.arange(32, 40, 0.5))
    return CS

# ploting contour dataset
def draw_contour(img_path: str, thermal_contents: list):
    results = list()
    plot_counts = 1
    for thermal_img_name in thermal_contents:
        plt.subplot(int(len(thermal_contents)/2), 2, plot_counts)
        plt.clabel(contour(img_path+thermal_img_name))
        plt.xticks([]),plt.yticks([])
        plot_counts += 1
    plt.show()

if __name__ == '__main__':
    img_path, contents = utils.img_list()
    thermal_contents, digital_contents = utils.divide_thermal_digital(contents)
    draw_contour(img_path, thermal_contents)