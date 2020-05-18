from _thread import start_new_thread
import time
import sys
import PyQt5
import PyMySQL
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from RegLogin import MyLogin
from exam import MainWindow
from QuizDatabase import DBWindow
import smtplib

class MyDBWindow(DBWindow,QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)  #will call the method of QuizDatabase.py
        self.dbConnect()
        self.groupBox.setEnabled(False);
        self.lblMsg.hide()
        self.btNew.clicked.connect(self.btAddNew_clicked)
        self.btSave.clicked.connect(self.btSave_clicked)
        self.btDelete.clicked.connect(self.btDelete_clicked)
        self.btUpdate.clicked.connect(self.btUpdate_clicked)
        self.btClose.clicked.connect(self.btClose_clicked)
        self.btClear.clicked.connect(self.btClear_clicked)
    def dbConnect(self):
         try:
             qno=self.GenerateQuesNo();
             self.t1.setText(str(qno))
             global db
             global cursor
             db = PyMySQL.connect("localhost","root","tiger","exam" )
             cursor = db.cursor()
             count=cursor.execute("select * from questions")
             print(count)
             row=cursor.fetchall()
             self.table1.setRowCount(count)
             for i in range(0,count,1):
                 for j in range(0,7,1):
                     #print(i,j)
                     self.table1.setItem(i,j,QTableWidgetItem(str(row[i][j])))
         except Exception as e:
            print(e)

    def btAddNew_clicked(self):
        self.groupBox.setEnabled(True)

    def GenerateQuesNo(self):
         print("ok")
         try:
             count=cursor.execute("select max(qno) from questions")
             row=cursor.fetchone()
             qno=1
             if count==0:
                qno=1
             else:
                qno=row[0] + 1
             return qno
         except Exception as e:
            print(e)
            
    def btSave_clicked(self):
        
        try:
            qno=self.t1.text()
            self.t1.setText(""+qno)
            qdesc=self.t2.text()
            option1=self.t3.text()
            option2=self.t4.text()
            option3=self.t5.text()
            option4=self.t6.text()
            crtoption=self.t7.text()
            query="""INSERT INTO QUESTIONS
                        VALUES(%d,'%s','%s','%s','%s','%s','%s')""" %(int(qno),qdesc,option1,option2,option3,option4,crtoption)
            print(query)
            cursor.execute(query)
            db.commit()
            self.dbConnect()
            self.lblMsg.setText("Record added to database successfully")
            self.lblMsg.show()
        except Exception as e:
            print(e)

    def btDelete_clicked(self):
        try:
            qno=int(self.t1.text())
            query="delete from questions where qno=%d" %(qno)
            cursor.execute(query)
            db.commit()
            self.dbConnect()
            self.lblMsg.setText("Record deleted from Database successfully")
            self.lblMsg.show()
        except Exception as e:
            print(e)

    def btUpdate_clicked(self):
        try:
            qno=int(self.t1.text())
            qdesc=self.t2.text()
            option1=self.t3.text()
            option2=self.t4.text()
            option3=self.t5.text()
            option4=self.t6.text()
            crtoption=self.t7.text()
            query="""UPDATE QUESTIONS SET qdesc='%s',option1='%s',
                    option2='%s',option3='%s',option4='%s',crtoption='%s' where qno=%d""" %(qdesc,option1,option2,option3,option4,crtoption,qno)
            cursor.execute(query)
            db.commit()
            self.dbConnect()
            self.lblMsg.setText("Record update successfully")
            self.lblMsg.show()
        except Exception as e:
            print(e)

    def btClose_clicked(self):
        self.close()

    def btClear_clicked(self):
        self.t1.setText("")
        self.t2.setText("")
        self.t3.setText("")
        self.t4.setText("")
        self.t5.setText("")
        self.t6.setText("")
        self.t7.setText("")
class MyWindow(MainWindow,QMainWindow):
    qcorrect=0
    qwrong=0
    QNO=1
    NOQ=5  #No. of questions 
    def __init__(self, parent=None):
        #super(MyWindow,self).__init__()
        global seconds
        seconds=20
        QMainWindow.__init__(self,parent)
        self.setupUi(self)  #will call the method of exam.py
        self.btBegin.clicked.connect(self.btBegin_clicked)
        self.lcd.display(seconds)
        self.btLogOut.clicked.connect(self.btLogout_clicked)
        self.btNext.clicked.connect(self.btNext_clicked)
        self.btAns.clicked.connect(self.GetResult)
        self.label8.hide()
        self.label9.hide()
        self.table1.hide()
        self.quesBox.hide()
        t=time.localtime()
        ct=time.asctime(t)
        self.lblDate.setText(""+ct);
        
    def createTable(self):
        try:
                email=self.t1.text()
                query="select * from result where email='%s'" % (email)
                cursor.execute(query)
                data = cursor.fetchone()
                #code to create table at run time
                self.tableWidget = QTableWidget()
                self.tableWidget.setRowCount(2)
                self.tableWidget.setColumnCount(7)
                self.tableWidget.setItem(0,0,QTableWidgetItem("Email"))
                self.tableWidget.setItem(0,1,QTableWidgetItem("Name"))
                self.tableWidget.setItem(0,2,QTableWidgetItem("Correct"))
                self.tableWidget.setItem(0,3,QTableWidgetItem("Wrong"))
                self.tableWidget.setItem(0,4,QTableWidgetItem("Score"))
                self.tableWidget.setItem(0,5,QTableWidgetItem("Status"))
                self.tableWidget.setItem(0,6,QTableWidgetItem("DateOfExam"))
                for i in range(1,2,1):
                    for j in range(0,7,1):
                       self.tableWidget.setItem(i,j,QTableWidgetItem(str(data[j])))
                self.tableWidget.setGeometry(240, 90, 831, 131)
                self.tableWidget.setWindowTitle("Your Result")
                self.tableWidget.show()
                #code for filling PyQt Designer Table
                self.table1.setItem(0,0,QTableWidgetItem("Email"))
                self.table1.setItem(0,1,QTableWidgetItem("Name"))
                self.table1.setItem(0,2,QTableWidgetItem("Correct"))
                self.table1.setItem(0,3,QTableWidgetItem("Wrong"))
                self.table1.setItem(0,4,QTableWidgetItem("Score"))
                self.table1.setItem(0,5,QTableWidgetItem("Status"))
                self.table1.setItem(0,6,QTableWidgetItem("DateOfExam"))
                for i in range(1,2,1):
                    for j in range(0,7,1):
                       self.table1.setItem(i,j,QTableWidgetItem(str(data[j])))
                
        except Exception as e:
            print(e)

    def  display(self,sec):
        for i in range(sec,-1,-1):
            self.lcd.display(i)
            time.sleep(1)
        else:
            #self.quesBox.setEnabled(False)
            self.btAns.setEnabled(True)
            self.quesBox.hide()
            self.label8.show()
            
    def GetResult(self):
        try:
            status=""
            score=MyWindow.qcorrect/(MyWindow.NOQ)*100
            if score>=60:
                status="Qualified"
                self.label8.setText("CONGRATS!!! You have  QUALIFIED for the next round.")
            else:
                status="Not Qualified"
                self.label8.setText("SORRY!!! You have NOT QUALIFIED for the next round")
            
            email=self.t1.text()
            name=self.t2.text()
            t=time.localtime()
            ct=time.asctime(t)
            q="DELETE FROM RESULT WHERE email='%s'" % (email)
            cursor.execute(q)
            db.commit()
            query="INSERT INTO RESULT VALUES('%s','%s',%d,%d,%d,'%s','%s')" % (email,name,MyWindow.qcorrect,MyWindow.qwrong,score,status,str(ct))
            print(query)    
            cursor.execute(query)
                   
            db.commit()
            self.label8.hide()
            self.table1.setGeometry(10,140,631,111)
            
            self.table1.show()
            self.createTable()
            self.label8.show()
            self.label9.setText("Your Result has been sent to your registered Email.Kindly Check!")
            self.label9.show()
            # Content-type and Subject are required to send HTML mail using HTML tags
            message="""MIME-Version: 1.0
Content-type: text/html
Subject: Python Quiz Result"""
            message+="\n<h1>" + self.label8.text() + "</h1>"
            message+="""<table border=2 cellspacing=5><th>Name<th>Correct<th>Wrong<th>Score<th>Status<th>DOE
            <tr><td>%s<td>%d<td>%d<td>%d<td>%s<td>%s </tr></table>""" % (name,MyWindow.qcorrect,MyWindow.qwrong,score,status,str(ct))
            self.sendEmail(message)

        except Exception as e:
            print(e)

    def sendEmail(self,message):
        sender = 'mohit310.mt@gmail.com'
        to=self.t1.text()
        receivers = [to]
        try:
            
            smtpObj = smtplib.SMTP('smtp.gmail.com',25,'localhost')
            smtpObj.starttls()
            smtpObj.login("mohit310.mt","lollo@123")
            smtpObj.sendmail(sender, receivers, message)         
            print ("Successfully sent email")
        except Exception as e:
            print (e)

    def getQuestion(self,qno):
        global ans
        query="select * from questions where qno=%d" % (qno)
        print(query)
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data!=None:
            self.lblQues.setText(str(data[1]))
            self.rb1.setText(data[2])
            self.rb2.setText(data[3])
            self.rb3.setText(data[4])
            self.rb4.setText(data[5])
            ans=data[6]
        
    def btBegin_clicked(self):
        MyWindow.QNO=1
        self.btBegin.setEnabled(False)
        self.quesBox.show()
        self.quesBox.setEnabled(True)
        self.getQuestion(MyWindow.QNO)
        start_new_thread(self.display,(seconds,))

    def btLogout_clicked(self):
        self.close()
    def btNext_clicked(self):
            
            try:
                print("ok")
                if MyWindow.QNO<= (MyWindow.NOQ):
                    choice=""
                    if self.rb1.isChecked():
                        choice="option1"
                    elif self.rb2.isChecked():
                        choice="option2"
                    elif self.rb3.isChecked():
                        choice="option3"
                    elif self.rb4.isChecked():
                        choice="option4"

                    print(ans,choice)
                    if ans==choice:
                        MyWindow.qcorrect+=1
                    else:
                        MyWindow.qwrong+=1
         
                    print(MyWindow.qcorrect,MyWindow.qwrong)
                    MyWindow.QNO=MyWindow.QNO+1
                    self.getQuestion(MyWindow.QNO)
                    print(MyWindow.QNO)
                else:
                    
                    self.quesBox.hide()
                    self.label8.show()
                    
            except Exception as e:
                print(e)

class AppWindow(QDialog):
    def connectDB(self):
        global db
        global cursor
        db = PyMySQL.connect("localhost","root","tiger","exam" )
        cursor = db.cursor()
    def rb1_clicked(self):
        try:
            if self.ui.rb1.isChecked():
                self.ui.groupBox_2.setEnabled(True)
                self.ui.groupBox.setEnabled(False)
        except Exception as e:
                print(e)
    def rb2_clicked(self):
        if self.ui.rb2.isChecked():
            self.ui.groupBox.setEnabled(True)
            self.ui.groupBox_2.setEnabled(False)
    def button3_clicked(self):
            self.ui.t1.setText("")
            self.ui.t2.setText("")
            self.ui.label1.setText("")
    def button4_clicked(self):
            self.ui.t3.setText("")
            self.ui.t4.setText("")
            self.ui.label2.setText("")


    def button1_clicked(self):
        try:
            uname=self.ui.t1.text()
            passw=self.ui.t2.text()
            query="insert into login values('%s','%s')" % (uname,passw)
            print(query)
            count=cursor.execute(query)
            if(count==1):
                self.ui.label1.setText("Your are registered successfully")
                            
            db.commit()
        except Exception as e:
            print(e)
            self.ui.label1.setText("Your are already registered")
    def button2_clicked(self):
        try:
            uname=self.ui.t3.text()
            passw=self.ui.t4.text()
            query="select * from login where email='%s' and password='%s'" % (uname,passw)
            print(query)
            count=cursor.execute(query)
            if count==1 and uname=="admin":
                self.winDB=MyDBWindow()
                self.winDB.show()
                self.close()
            elif count==1:
               self.m=MyWindow()
               self.m.show()
               self.close()
            else:
                   self.ui.label2.setText("Invalid Username/Password.")
        except Exception as e:
           print(e)

      
    def __init__(self):
        self.connectDB()
        super().__init__()
        self.ui = MyLogin()
        self.ui.setupUi(self)
        
        self.ui.rb1.clicked.connect(self.rb1_clicked)
        self.ui.rb2.clicked.connect(self.rb2_clicked)
        self.ui.button2.clicked.connect(self.button2_clicked)
        self.ui.button1.clicked.connect(self.button1_clicked)
        self.ui.button1_2.clicked.connect(self.button3_clicked)
        self.ui.button2_2.clicked.connect(self.button4_clicked)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

