import sys
import cv2
import numpy as np

from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMainWindow, 
    QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photoshop")

        # 메뉴바 만들기
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("파일")
        exit = QAction("나가기", self, triggered=app.quit)
        self.menu_file.addAction(exit)

        # 메인화면 레이아웃
        main_layout = QHBoxLayout()

        # 사이드바 메뉴버튼
        sidebar = QVBoxLayout()
        button1 = QPushButton("이미지 열기")
        button2 = QPushButton("좌우반전")
        button3 = QPushButton("새로고침")
        button4 = QPushButton("세피아")
        button5 = QPushButton("회전")
        button6 = QPushButton("합성")
        button7 = QPushButton("이미지 열기2")

        button1.clicked.connect(self.show_file_dialog)
        button2.clicked.connect(self.flip_image)
        button3.clicked.connect(self.clear_label)
        button4.clicked.connect(self.sepia)
        button5.clicked.connect(self.rotate_image)
        button6.clicked.connect(self.plus_image)
        button7.clicked.connect(self.show_file_dialog2)

        sidebar.addWidget(button1)
        sidebar.addWidget(button2)
        sidebar.addWidget(button3)
        sidebar.addWidget(button4)
        sidebar.addWidget(button5)
        sidebar.addWidget(button6)
        sidebar.addWidget(button7)

        main_layout.addLayout(sidebar)

        self.label1 = QLabel(self)
        self.label1.setFixedSize(640, 480)
        main_layout.addWidget(self.label1)

        self.label2 = QLabel(self)
        self.label2.setFixedSize(640, 480)
        main_layout.addWidget(self.label2)

        self.label3 = QLabel(self)
        self.label3.setFixedSize(640, 480)
        main_layout.addWidget(self.label3)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
    
    def show_file_dialog(self):
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        self.image = cv2.imread(file_name[0])
        h, w, _ = self.image.shape
        bytes_per_line = 3 * w
        image = QImage(
            self.image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.label1.setPixmap(pixmap)

    def show_file_dialog2(self):
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        self.image2 = cv2.imread(file_name[0])
        h, w, _ = self.image2.shape
        bytes_per_line = 3 * w
        image2 = QImage(
            self.image2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image2)
        self.label2.setPixmap(pixmap)

    def flip_image(self):
        image = cv2.flip(self.image, 1)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(
            image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    def clear_label(self):
        self.label2.clear()

    def sepia(self):
        image1 = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        res = image1.copy()
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB) # converting to RGB as sepia matrix is for RGB
        res = np.array(res, dtype=np.float64)
        res = cv2.transform(res, np.matrix([[0.393, 0.769, 0.189],
                                            [0.349, 0.686, 0.168],
                                            [0.272, 0.534, 0.131]]))
        res[np.where(res > 255)] = 255 # clipping values greater than 255 to 255
        res = np.array(res, dtype=np.uint8)
        res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
        h, w, _ = image1.shape
        bytes_per_line = 3 * w
        res = QImage(
            res.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()

        pixmap = QPixmap(res)
        self.label2.setPixmap(pixmap)

        #pixmap = QPixmap(image1)
        #self.label1.setPixmap(pixmap)


    # def brightness(self):
    #     cv2.namedWindow('image')
    #     cv2.createTrackbar('val', 'image', 100, 150, nothing)
    #     while True:
    #         hsv = cv2.cvtColor(self, cv2.COLOR_BGR2HSV)
    #         hsv = np.array(hsv, dtype=np.float64)
    #         val = cv2.getTrackbarPos('val', 'image')
    #         val = val/100 # dividing by 100 to get in range 0-1.5
    #         # scale pixel values up or down for channel 1(Saturation)
    #         hsv[:, :, 1] = hsv[:, :, 1] * val
    #         hsv[:, :, 1][hsv[:, :, 1] > 255] = 255 # setting values > 255 to 255.
    #         # scale pixel values up or down for channel 2(Value)
    #         hsv[:, :, 2] = hsv[:, :, 2] * val
    #         hsv[:, :, 2][hsv[:, :, 2] > 255] = 255 # setting values > 255 to 255.
    #         hsv = np.array(hsv, dtype=np.uint8)
    #         res = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    #         cv2.imshow("original", img)
    #         cv2.imshow('image', res)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     cv2.destroyAllWindows()

    def rotate_image(self):
        image = cv2.flip(self.image, 1)
        img90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        pixmap = QPixmap(img90)
        self.label2.setPixmap(pixmap)

    def plus_image(self):
        image1 = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2RGB)
        h, w, _= image1.shape[:3]
        bytes_per_line = 3 * w 
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        alpha = 0.5
        plus_image = image1 * alpha + image2 * (1-alpha)
        plus_image = plus_image.astype(np.uint8)
        plus_image = QImage(
            plus_image.data, w, h, bytes_per_line, QImage.Format_BGR888).rgbSwapped()
        pixmap = QPixmap(plus_image)
        self.label3.setPixmap(pixmap)   

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





