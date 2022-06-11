#-*- coding: utf-8 -*- 


# pyqt5 설치해야함
# pip uninstall PyGLM PySide2 pyopengl
# pip install PyGLM PySide2 pyopengl
# pip install pyqt5
# pip install pyqt5-tools


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow, QApplication,QSizePolicy
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os
import run
from retrieval import retrieval_f
from summalize import summalize_f
from summalize import ocr
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'#텐서플로우 오류 제거용
sum_size=1

class Form(QWidget):
    
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        self.ui=uic.loadUi("./myqt01.ui",self)
        self.setWindowTitle("뉴스검색기")
        self.setAcceptDrops(True)
        self.output.setWordWrap(True)    
        self.our_data.setWordWrap(True)  
        self.web_data.setWordWrap(True) 	 
        self.map_data.setWordWrap(True)  
        self.output.setOpenExternalLinks(True)
        self.our_data.setOpenExternalLinks(True)
        self.web_data.setOpenExternalLinks(True)
        self.output.setTextFormat(1)
        self.our_data.setTextFormat(1)
        self.web_data.setTextFormat(1)
        self.ui.show()
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
    #ocr 읽는 부분
    def img_read(self,imPath):
        text=ocr.ocr_read(imPath)
        self.input_text.setPlainText(text)
        self.output.setText(self.search(text))
        
	#버튼 클릭시 읽어서 textbox(출 수정)
    def button_clicked(self):
        text=self.input_text.toPlainText()
        self.set_textbox(text)
  
    def eval_button_clicked(self):
        text=self.query_input.toPlainText()
        self.web_data.setText('검색중')
        self.our_data.setText('검색중')
        our,crawl,ans,avg=run.evaluate(text)		
        text1=""
        for link,context,index in our:
        	text1+="<br><br>"+summalize_f.generate_summary(context, 1)+"<br>"+\
                '<a href="'+link+'">링크</a>'
        self.our_data.setText(text1)
        text2=""
        for title,link,context in crawl:
        	text2+="<br><br>"+title+"<br>"+\
                '<a href="'+link+'">링크</a>'
        self.web_data.setText(text2)
		
        text3='True check: '+str(ans)+'\n\n'+"map value:"+str(avg)
        self.map_data.setText(text3)
		
		
    def set_textbox(self,text):
        self.output.setText(self.search(text))
        
    def search(self,text):
        output=""
        
        for newsFeed in retrieval_f.retrieval(text,int(self.src_num.currentText())):
        	output+="<br><br>"+summalize_f.generate_summary(newsFeed[1], int(self.sum_num.currentText()))+"<br>"+\
                '<a href="'+newsFeed[0]+'">링크</a>'
                
            
        return output
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    form=Form()
    form.show()
    sys.exit(app.exec_())