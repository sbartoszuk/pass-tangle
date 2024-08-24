from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
import sys
from modules import taskGrabber
from modules import dataLoader
from modules import dialogBoxes

class CustomListener(QObject):
    refresh = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_conditions)
        self.timer.start(2000)
    def check_conditions(self):
        self.refresh.emit()

def get_screen_height():
    screen_geometry = QDesktopWidget().screenGeometry()
    screen_height = screen_geometry.height()
    return screen_height

def c_dialog_box(message, win_title):
    app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    #msg.setInformativeText("Click OK to continue")
    msg.setWindowTitle(win_title)
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()

    sys.exit()

class CWindowBox(QFrame):
    def __init__(self) -> None:
        super().__init__()
        font = QFont('None', 14)
        
        # --------------------------------- variables
        
        self.clickPos = 0

        if dataLoader.check_data_file():
                self.cpm_data = dataLoader.DataManagement()
        else:
            c_dialog_box('Run setup first!', 'Error')
            exit()
    
        # --------------------------------- layout

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        screen_heigth = get_screen_height()
        self.move(-6, screen_heigth - 294)
        self.setWindowTitle('Pass-Tangle')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        unroll_box = QLabel()
        unroll_box.setFixedWidth(80)
        unroll_box.setFixedHeight(80)
        unroll_box.setAlignment(QtCore.Qt.AlignCenter)
        unroll_box.setStyleSheet('background: black;'
                                 'border: 3px solid white;')
        self.layout.addWidget(unroll_box)
        unroll_layout = QHBoxLayout()
        unroll_box.setLayout(unroll_layout)

        unroll_btn = QPushButton()
        unroll_btn.setFixedHeight(30)                    # here
        unroll_btn.setFixedWidth(30)
        unroll_btn.setStyleSheet('color: black;'
                                 'border: 0px;'
                                 'background: url(assets/lock.png);')
        unroll_layout.addWidget(unroll_btn)

        self.records_box = QLabel()
        self.records_box.setFixedWidth(250)
        self.records_box.setFixedHeight(150)
        self.records_box.setStyleSheet('background: white;')
        self.layout.addWidget(self.records_box)
        self.records_box.hide()
        self.unrolled = False
        records_layout = QVBoxLayout()
        self.records_box.setLayout(records_layout)

        self.active_task = taskGrabber.activeTask()
        self.records_counter = str(self.cpm_data.count_records(self.active_task))
        self.records_couter_display = QLabel(self.active_task + 
                                             '\n' + str(self.records_counter) + 
                                             ' records')
        self.records_couter_display.setStyleSheet('padding-left: 10px')
        self.records_couter_display.setFont(font)
        records_layout.addWidget(self.records_couter_display)

        show_active_btn = QPushButton('show')

        add_record_btn = QPushButton('add')
        
        more_btn = QPushButton('more')
        more_btn.setFixedWidth(215)
        more_btn.setFixedHeight(23)

        for button in [show_active_btn, add_record_btn, more_btn]:
            button.setStyleSheet('background: rgb(230,230,230);')
            button.setFont(font)

        btn_container = QFrame()
        btn_container.setStyleSheet('padding: 0px;')
        records_layout.addWidget(btn_container)

        btn_layout = QHBoxLayout()
        btn_container.setLayout(btn_layout)

        btn_layout.addWidget(show_active_btn)
        btn_layout.addWidget(add_record_btn)

        records_layout.addWidget(more_btn, alignment=QtCore.Qt.AlignCenter)

        # --------------------------------- layout functions

        unroll_box.mouseMoveEvent = self.CMoveWindow
        unroll_btn.mousePressEvent = self.Unroll
        show_active_btn.clicked.connect(self.showRecord)
        add_record_btn.clicked.connect(self.addRecord)
        more_btn.clicked.connect(self.moreOptions)

        self.listener = CustomListener()
        self.listener.refresh.connect(self.WinRefresh)

    def moreOptions(self):
        if dataLoader.check_key_connection():
            if self.cpm_data.data[0]:
                temp_data = self.cpm_data.show_all()
            else:
                temp_data = []

            dialog_box = dialogBoxes.CMoreWin(temp_data)
            dialog_box.exec_()

            self.cpm_data.load_from_files()
            temp_win_act = self.active_task
            self.active_task = False
            self.WinRefresh(temp_win_act)

            del temp_data
            del dialog_box
        else:
            dialog_box = dialogBoxes.CAcceptWin('Key not found! Connect USB drive.')
            dialog_box.exec_()

    
    def showRecord(self):
        if dataLoader.check_key_connection() and self.records_counter != '0':
            decrypted = self.cpm_data.show_active(self.active_task)
            
            dialog_box = dialogBoxes.CDisplayWin(decrypted)
            dialog_box.exec_()

            del dialog_box
            del decrypted
        if dataLoader.check_key_connection() and self.records_counter == '0':
            dialog_box = dialogBoxes.CAcceptWin('No records found!')
            dialog_box.exec_()
        elif not  dataLoader.check_key_connection():
            dialog_box = dialogBoxes.CAcceptWin('Key not found! Connect USB drive.')
            dialog_box.exec_()
        
    def addRecord(self):
        new_cred = []
        def reciveCredentials(data):
            return data
        if dataLoader.check_key_connection():
            dialog_box = dialogBoxes.CAddWin(self.active_task)
            dialog_box.textEntered.connect(lambda x: new_cred.extend(reciveCredentials(x)))
            dialog_box.exec_()

            if len(new_cred) > 0:
                self.cpm_data.add_record(new_cred)
                self.active_task = False
                self.WinRefresh(new_cred[0])
            del new_cred
        else:
            dialog_box = dialogBoxes.CAcceptWin('Key not found! Connect USB drive.')
            dialog_box.exec_()
            
    def WinRefresh(self, option_inp = False):
        if option_inp:
            self.temp = option_inp
        else:
            self.temp = taskGrabber.activeTask()
        if self.active_task != self.temp:

            dont_change_list = ['python', 'pythonw', 'py']
            
            if self.temp not in dont_change_list:
                self.active_task = self.temp
                self.records_counter = str(self.cpm_data.count_records(self.active_task))

                self.records_couter_display.setText(self.active_task + 
                                                    '\n' + self.records_counter +
                                                    ' records')

    def Unroll(self, event):
        if self.unrolled:
            self.unrolled = False
            self.records_box.hide()
        else:
            self.unrolled = True
            self.records_box.show()

    def CMoveWindow(self, event):
        if self.clickPos == 0:
            self.clickPos = event.globalPos()
        self.move(self.pos() + event.globalPos() - self.clickPos)
        self.clickPos = event.globalPos()
        event.accept()
        pass

AppHandler = QApplication(sys.argv)
App = CWindowBox()
App.show()
sys.exit(AppHandler.exec_())