import matplotlib
import cv2
from tensorflow.keras.models import load_model 
import numpy as np
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import path
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

MainUI, _ = loadUiType(path.join(path.dirname(__file__), 'untitled.ui'))

class MainApp(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Signature")
        self.setWindowIcon(QIcon('icon.png'))
        self.imagesPaths={}
        self.progressBar.hide()
        self.progressBar.setTextVisible(False)
        self.cnn_model = self.load_cnn_model()
        self.siamese_model = self.load_siamese_model()
        self.another_model = self.load_identification_model()
        self.handle_actions()


    def handle_actions(self):
        self.add_img1_btn.clicked.connect(lambda: self.open_image(self.first_img_original,self.add_img1_btn,'1'))
        self.add_img2_btn.clicked.connect(lambda: self.open_image(self.second_img_original,self.add_img2_btn,'2'))
        self.add_img1_btn_3.clicked.connect(lambda: self.open_image(self.first_img_original_3,self.add_img1_btn_3,'3'))
        self.add_img1_btn_4.clicked.connect(lambda: self.open_image(self.first_img_original_4,self.add_img1_btn_4,'4'))
        self.first_img_original.mousePressEvent = lambda event, label=self.first_img_original,num='1',upload_name=self.add_img1_btn: self.labelClicked(event, label,num,upload_name)
        self.second_img_original.mousePressEvent = lambda event, label=self.second_img_original,num='2',upload_name=self.add_img2_btn: self.labelClicked(event, label,num,upload_name)
        self.first_img_original_3.mousePressEvent = lambda event, label=self.first_img_original_3,num='3',upload_name=self.add_img1_btn_3: self.labelClicked(event, label,num,upload_name)
        self.first_img_original_4.mousePressEvent = lambda event, label=self.first_img_original_4,num='4',upload_name=self.add_img1_btn_4: self.labelClicked(event, label,num,upload_name)
        self.submit_cnn.clicked.connect(self.use_cnn_model)
         
         


    def labelClicked(self, event,label,num,upload_name):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)",
                                                  options=options)
        if fileName:
            upload_name.hide()
            self.imagesPaths[num]=fileName
            pixmap = QPixmap(fileName) 
            label.setPixmap(pixmap)
            label.setScaledContents(True) 




    def open_image(self, label_name,upload_name,num):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)",
                                                  options=options)
        if fileName:
            self.imagesPaths[num]=fileName
            upload_name.hide()
            pixmap = QPixmap(fileName) 
            label_name.setPixmap(pixmap)
            label_name.setScaledContents(True) 
            print(self.imagesPaths) 

    def load_cnn_model(self):
        return load_model('CNN model.h5')


    def load_siamese_model(self):
            pass

    def load_identification_model(self):
            pass

    def preprocess_cnn(self,image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    
    def use_cnn_model(self):
        if '3' not in self.imagesPaths or not self.imagesPaths['3']:
            QMessageBox.warning(self, "Upload Image", "Please upload an image first.")
            return
        self.progressBar.show()
        inputImage=self.preprocess_cnn(self.imagesPaths['3'])
        predictions = self.cnn_model.predict(inputImage)
        predictedLabel = "Forged" if predictions[0, 0] > 0.5 else "Real"
        self.progressBar.setTextVisible(True)
        self.progressBar.setValue(100) 
        self.progressBar.setFormat(f" {predictedLabel}")
        if predictions[0, 0] > 0.5:
            self.progressBar.setStyleSheet('''
        QProgressBar {
            border: 1px solid #2196F3;
            border-radius: 5px;
            text-align: center; /* Center-align the text */
        }
        QProgressBar::chunk {
            background-color: red; 
        }
    ''')
        else:
            self.progressBar.setStyleSheet('''
        QProgressBar {
            border: 1px solid #2196F3;
            border-radius: 5px;
            text-align: center; /* Center-align the text */
        }
        QProgressBar::chunk {
            background-color: #7FFF7F;
        }
    ''')
        QTimer.singleShot(5000, self.hide_progress_bar)

            
    def hide_progress_bar(self):
        self.progressBar.setValue(0)
        self.progressBar.hide()
                

    def use_siamese_model(self):
            pass
    
    def use_siamese_model(self):
            pass

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
    