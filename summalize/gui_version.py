from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys
import cv2
import pytesseract

#pip install git+https://github.com/haven-jeon/PyKoSpacing.git
#pip install tensorflow 2.5.3(python 3.10이면 버전 낮춰야 함)
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'#텐서플로우 오류 제거용
from pykospacing import Spacing
pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'
form_class= uic.loadUiType("./myqt01.ui")[0]

#import os 
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'#텐서플로우 오류 제거용

class WindowClass(QMainWindow,form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Drag and Drop")
        self.resize(720, 480)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
            self.textprint(str(f))
    def textprint(self,imPath):
        config = ('-l kor --oem 3 --psm 4')
        img_gray = cv2.imread(imPath, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.imread(imPath, cv2.IMREAD_GRAYSCALE)
        string=pytesseract.image_to_string(img_gray, config=config)
        spacing = Spacing()
        no_space_string=string.replace(" ","").replace("\n","")
        newstring = spacing(no_space_string) 
        self.lbl.setText(newstring)
        self.lbl.setWordWrap(True) 

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ui = WindowClass()
    ui.show()
    sys.exit(app.exec_())