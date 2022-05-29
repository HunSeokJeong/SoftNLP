from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys
import os
from retrieval import retrieval_f
from summalize import summalize_f
from summalize import ocr
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'#텐서플로우 오류 제거용
form_class= uic.loadUiType("./myqt01.ui")[0]
sum_size=1
# #import os 
# #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'#텐서플로우 오류 제거용

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
            self.img_read(str(f))
    
    def img_read(self,imPath):
        text=ocr.ocr_read(imPath)
        self.textEdit.setPlainText(text)
        self.lbl.setPlainText(self.search(text))
        
    def button_clicked(self):
        text=self.textEdit.toPlainText()
        self.set_textbox(text)
        
    def set_textbox(self,text):
        self.lbl.setPlainText(self.search(text))
        
    def search(self,text):
        output=""
        
        for newsFeed in retrieval_f.retrieval(text,int(self.cbx_src.currentText())):
        	output+="\n\n"+summalize_f.generate_summary(newsFeed, int(self.cbx_sum.currentText()))
            
        return output
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ui = WindowClass()
    ui.show()
    sys.exit(app.exec_())