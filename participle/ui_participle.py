# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import jieba
import os
import openpyxl
import re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(903, 577)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 90, 551, 451))
        self.textBrowser.setObjectName("textBrowser")
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(600, 90, 291, 451))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(600, 50, 96, 28))
        self.pushButton.setObjectName("pushButton")
        self.checkBox = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox.setGeometry(QtCore.QRect(720, 50, 141, 25))
        self.checkBox.setObjectName("checkBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 50, 96, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.radioButton = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton.setGeometry(QtCore.QRect(120, 50, 81, 25))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton_2.setGeometry(QtCore.QRect(200, 50, 91, 25))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton_3.setGeometry(QtCore.QRect(300, 50, 115, 25))
        self.radioButton_3.setObjectName("radioButton_3")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 903, 28))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_excel = QtWidgets.QAction(MainWindow)
        self.action_excel.setObjectName("action_excel")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_excel)
        self.menu.addAction(self.action_3)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "统计词频"))
        self.checkBox.setText(_translate("MainWindow", "按分词结果统计"))
        self.pushButton_2.setText(_translate("MainWindow", "分词"))
        self.radioButton.setText(_translate("MainWindow", "全模式"))
        self.radioButton_2.setText(_translate("MainWindow", "精确模式"))
        self.radioButton_3.setText(_translate("MainWindow", "搜索引擎模式"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.action.setText(_translate("MainWindow", "导入文本"))
        self.action_2.setText(_translate("MainWindow", "导出分词结果"))
        self.action_excel.setText(_translate("MainWindow", "导出词频"))
        self.action_3.setText(_translate("MainWindow", "退出"))



class Participle(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Participle,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("分词工具")
        self.init()
        self.filetext=''
        self.result=''

    def init(self):
        self.action_3.triggered.connect(self.close)
        self.action.triggered.connect(self.loadText)
        self.pushButton.clicked.connect(self.wordfrequency)
        self.pushButton_2.clicked.connect(self.participle)
        self.action_2.triggered.connect(self.export_result)
        self.action_excel.triggered.connect(self.export_word)

    def loadText(self):
        filename,filetype=QFileDialog.getOpenFileName(self,'选择文件','.',"All Files (*);;Text Files (*.txt)")
        try:
            self.filetext=open(filename,'r',encoding='utf-8').read()
        except:
            return
        sub_re='[\!\/_,$%^*\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?【】“”;-]+'
        self.filetext=re.sub(sub_re,'',self.filetext)
        self.textBrowser.setText(self.filetext)

    def participle(self):
        jieba.set_dictionary("dict/dict.txt")
        jieba.initialize()
        if(self.radioButton.isChecked()):
            self.result=jieba.cut(self.filetext,cut_all=True)
        elif(self.radioButton_2.isChecked()):
            self.result=jieba.cut(self.filetext,cut_all=False)
        elif(self.radioButton_3.isChecked()):
            self.result=jieba.cut_for_search(self.filetext)
        else:
            self.result=jieba.cut(self.filetext,cut_all=False)
        self.textBrowser.clear()
        self.textBrowser.setText('/'.join(self.result))

    def wordfrequency(self):
        pass

    def export_word(self):
        pass

    def export_result(self):
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    participle=Participle()
    participle.show()
    sys.exit(app.exec_())
