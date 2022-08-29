import sys
import download
import draw_contour
import utils
import cv2
import calculate
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('mouse')

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)

        download_push_button = QPushButton('download')
        download_push_button.clicked.connect(self.download_push_button_clicked)

        contour_push_button = QPushButton('contour')
        contour_push_button.clicked.connect(self.contour_push_button_clicked)

        self.avg_result_label = QLabel()
        self.max_result_label = QLabel()
        self.min_result_label = QLabel()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.canvas)

        mid_layout = QVBoxLayout()
        mid_layout.addWidget(self.avg_result_label)
        mid_layout.addWidget(self.max_result_label)
        mid_layout.addWidget(self.min_result_label)

        bot_layout = QHBoxLayout()
        bot_layout.addWidget(download_push_button)
        bot_layout.addWidget(contour_push_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        #main_layout.addLayout(mid_layout)
        main_layout.addLayout(bot_layout)

        self.setLayout(main_layout)

        self.setGeometry(900, 50, 270, 900)
        self.show()
    
    def download_push_button_clicked(self):
        download.image_download()
    
    def contour_push_button_clicked(self):
        img_path, contents = utils.img_list("C:/Users/user/Downloads/")
        thermal_contents, digital_contents = utils.divide_thermal_digital(contents)

        cnt = len(thermal_contents)
        avg_list = list()
        max_list = list()
        min_list = list()
        for i in range(1, cnt+1):

            ax = self.fig.add_subplot(cnt, 2, (2*i-1))
            cs = draw_contour.contour(img_path+thermal_contents[i-1])
            ax.clabel(cs)
            ax.set_xticks([])
            ax.set_yticks([])
            avg_value, max_value, min_value = calculate.cal_value(img_path+thermal_contents[i-1])
            if (avg_value != 0):
                avg_list.append(avg_value)
            if (max_value != 0):
                max_list.append(max_value)
            if (min_value != 0):
                min_list.append(min_value)
            
            ax.text(-30, -13, "avg: %s" %(str(round(avg_value, 2))), fontsize='xx-small')
            ax.text(40, -13, "max: %s" %(str(round(max_value, 2))), fontsize='xx-small')
            ax.text(110, -13, "min: %s" %(str(round(min_value, 2))), fontsize='xx-small')
            ax2 = self.fig.add_subplot(cnt, 2, (2*i))
            digital_img = cv2.imread(img_path+digital_contents[i-1])
            ax2.imshow(digital_img)
            ax2.set_xticks([])
            ax2.set_yticks([])

        #self.avg_result_label.setText("avg: %d" %(round(sum(avg_list)/len(avg_list), 2)))
        #self.max_result_label.setText("max: %d" %(round(max(max_list), 2)))
        #self.min_result_label.setText("min: %d" %(round(min(min_list), 2)))

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())