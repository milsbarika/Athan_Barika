# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.uic import loadUiType
import sqlite3
from playsound import playsound
import sys
from os import path
import datetime
import pytz
from hijri_converter import Hijri, Gregorian
global nomMois
global noJours
global nomJours

FORM_CLASS,_ =loadUiType(path.join(path.dirname(__file__),'C:/allFiles/athanBarika.ui'))	


class Etudiant(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Etudiant, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.maFenetre()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)
        global nomMois
        global noJours
        global nomJours

        dt_mtn = datetime.datetime.now()
        # print(dt_mtn.strftime("%A"))

        mtn_tz = pytz.timezone('US/Mountain')
        dt_mtn = mtn_tz.localize(dt_mtn)
        # print(dt_mtn.strftime('%B %d, %Y'))
        # self.label_9.setText(dt_mtn.strftime('%B %d, %Y'))
       
        nomMois= dt_mtn.strftime('%B')
        noJours= dt_mtn.strftime('%d')
        nomJours=dt_mtn.strftime("%A")
        
        h = Gregorian.today().to_hijri()
        # print("hhh",h)
        myDateH = h.day_name('ar')+" "+str(h.day)+" "+h.month_name('ar')+" "+str(h.year)
        self.label_8.setText(myDateH)
        # print(myDateH)
        
        
        self.tabledetails.setColumnWidth(0,25)
#        self.tabledetails.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3","Header 4", "Header 5", "Header 6","Header 7", "Header 8", "Header 9"])
#        self.tabledetails.resizeColumnsToContents()
        self.msg=QMessageBox()
        self.afficher_le_Mois()
        self.afficher_le_Jours()
        
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.closeButton.clicked.connect(lambda: self.close())
        # self.Image_btn.clicked.connect(self.afficher_image)
   
    def displayTime(self):
        # if nomJours=="Thursday":
        #     self.label_8.setText(u"الخميس")
        # elif nomJours=="Friday":
        #     self.label_8.setText(u"الجمعة")
        # elif nomJours=="Saturday":
        #     self.label_8.setText(u"السبت")
        # elif nomJours=="Sunday":
        #     self.label_8.setText(u"الاحد")
        # elif nomJours=="Monday ":
        #     self.label_8.setText(u"الاثنين")
        # elif nomJours=="Tuesday ":
        #     self.label_8.setText(u"الثلاثاء")
        # elif nomJours=="Wednesday ":
        #     self.label_8.setText(u"الاربعاء")
        time = QTime.currentTime()
        date =QDate.currentDate()
        temps = time.toString('hh:mm:ss')
        LaDate = date.toString(Qt.DefaultLocaleLongDate)
        self.label_9.setText((LaDate.upper()))
        self.lcdNumber.display(temps) 
        
        if self.fajrtxt.text()==temps:
            print("le temps est :Fajr")
            playsound("elBanna.mp3")
            
        elif self.sunrisetxt.text()==temps:
            print("le temps est :Sunrise")
            playsound("elBanna.mp3")
        
        elif self.dhuhrtxt.text()==temps:
            print("le temps est :Dohur")
            playsound("elBanna.mp3")
            
        elif self.asrtxt.text()==temps:
            print("le temps est :Asr")
            playsound("elBanna.mp3")
            
        elif self.maghribtxt.text()==temps:
            print("le temps est :Maghrib")
            playsound("elBanna.mp3")
            
        elif self.ishatxt.text()==temps:
            print("le temps est :Isha")
            playsound("elBanna.mp3")
            
                
    def msg_display(self,title,msg):
        self.msg.setWindowTitle(title)
        self.msg.setText(msg)
        self.msg.exec()

    
    def afficher_le_Mois(self):

        global nomMois
        # print("le mois est:",str(nomMois))
        # leMois=self.label_8.setText()
        # print("le mois est :",leMois)
        cnn=sqlite3.connect("C:/allFiles/priere_csv.db")
#        connection=get_sql_connection()
        rs=cnn.cursor()
        # sql = "SELECT * FROM December"
        sql = "SELECT * FROM "+nomMois+""
        
        result=rs.execute(sql)
        print(sql)
        self.tabledetails.setRowCount(0)
        for row_number, row_data in enumerate(result):
#            print(row_number)
            self.tabledetails.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabledetails.setItem(row_number, column_number, QTableWidgetItem(str(data)))
#        cnn.close()
                
    def afficher_le_Jours(self):
        global nomMois
        global noJours

        cnn=sqlite3.connect("C:/allFiles/priere_csv.db")
               
        rs=cnn.cursor()
        rs.execute("SELECT * FROM "+nomMois+" WHERE Day="+noJours+"")

        resultat=rs.fetchone()
        print(resultat)


        if resultat is False:
            self.msg_display("ERROR","pas d'enregistrements!!")
            return
        # self.daytxt.setText(str(resultat[0]))
        self.fajrtxt.setText(str(resultat[1]))
        self.sunrisetxt.setText(str(resultat[2]))
        self.dhuhrtxt.setText(str(resultat[3]))
        self.asrtxt.setText(str(resultat[4]))
        self.maghribtxt.setText(str(resultat[5]))
        self.ishatxt.setText(str(resultat[6]))                
        cnn.close()
        
        
    # def afficher_image(self):
    #     self.image_path,return_status=QFileDialog.getOpenFileName()
    #     print(self.image_path)
        
    #     if self.image_path.split('.')[1] not in ['img','jpg','jpeg','png']:
    #         self.msg_display("ERROR","Select only image files!")
    #     else:
    #         image=QPixmap(self.image_path).scaled(self.imageInput.height(),self.imageInput.width())
    #         self.imageInput.setPixmap(image)

    
    def maFenetre(self):
        self.setFixedSize(334,419)
#        self.setWindowIcon(QIcon('chat.png'))    
        self.show()
        
        
    # def CloseApp(self):
    #     sys.exit() 
        
        
def main():
    app = QApplication(sys.argv)
    window = Etudiant()
    # connection=get_sql_connection()
    window.show()
    app.exec_()

    
    
if __name__ == "__main__":
    main()


#def main():            
#    app = QApplication(sys.argv)
#    window = Etudiant()
#    window.show()
#    app.exec_()

#if __name__ == "__main__":
#    main()
