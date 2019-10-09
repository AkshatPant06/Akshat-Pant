# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Akshat Pant\Desktop\QT\Advanced.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(596, 464)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectImageBtn = QtWidgets.QPushButton(self.centralwidget)
        self.selectImageBtn.setGeometry(QtCore.QRect(110, 100, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Light")
        self.selectImageBtn.setFont(font)
        self.selectImageBtn.setObjectName("selectImageBtn")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(100, 310, 111, 23))
        self.addButton.setObjectName("addButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 290, 111, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.listWidget = QtWidgets.QListView(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(220, 220, 256, 192))
        self.listWidget.setObjectName("listWidget")
        self.imageLbl = QtWidgets.QFrame(self.centralwidget)
        self.imageLbl.setGeometry(QtCore.QRect(219, 40, 261, 151))
        self.imageLbl.setFrameShape(QtWidgets.QFrame.Box)
        self.imageLbl.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imageLbl.setObjectName("imageLbl")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 70, 47, 13))
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 596, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.selectImageBtn.clicked.connect(self.setImage)
        self.addButton.clicked.connect(self.addItem)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.selectImageBtn.setText(_translate("MainWindow", "Select Image"))
        self.addButton.setText(_translate("MainWindow", "Add"))

    def setImage(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "",
                                                            "Image Files (*.png *.jpg *jpeg *.bmp)")  # Ask for file
        if fileName:  # If the user gives a file
            pixmap = QtGui.QPixmap(fileName)  # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.imageLbl.width(), self.imageLbl.height(),
                                   QtCore.Qt.KeepAspectRatio)  # Scale pixmap
            self.imageLbl.setPixmap(pixmap)  # Set the pixmap onto the label
            self.imageLbl.setAlignment(QtCore.Qt.AlignCenter)  # Align the label to center

    def addItem(self):
        value = self.lineEdit.text()  # Get the value of the lineEdit
        self.lineEdit.clear()  # Clear the text
        self.listWidget.addItem(value)  # Add the value we got to the list

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
