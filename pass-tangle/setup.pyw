from PyQt5.QtGui import QFont, QPixmap, QFontDatabase
from PyQt5.QtWidgets import QWidget
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import os
# -- custom scripts
from modules import dataLoader


def get_screen_resolution():
    app = QApplication(sys.argv)
    screen = QDesktopWidget().screenGeometry()
    return screen.width(), screen.height()
width, height = get_screen_resolution()
win_heigth = 500
win_width = 400
x = (width - win_width)//2
y = (height - win_heigth)//2

class SetupDoneWin(QDialog):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('assets/font1.otf')
        font_family1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font_id = QFontDatabase.addApplicationFont('assets/font2.ttf')
        font_family2 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family1, 14)
        font2 = QFont(font_family2, 16)
        font_small_2 = QFont(font_family2, 11)
        font_big = QFont(font_family1, 23)
        font_big_2 = QFont(font_family2, 23)

        self.setWindowTitle('pass-tangle setup')
        self.setFixedHeight(win_heigth)
        self.setFixedWidth(win_width)
        self.setStyleSheet('background: black;')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.move(x, y)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        self.setContentsMargins(10, 10, 10, 10)

        # ----------------------------------------------- layout

        text_big_label = QLabel('All done,')
        text_big_label.setFont(font_big)

        temp_text = ['setup completed. Remember',
                     'to keep your key safe. You',
                     'can use pass-tangle now.']
        temp_text = '\n'.join(temp_text)

        text_normal_label = QLabel(temp_text)
        text_normal_label.setFont(font)

        for label in [text_big_label, text_normal_label]:
            label.setStyleSheet('color: white;')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(label, alignment=QtCore.Qt.AlignCenter)
            self.layout.addSpacing(10)        
        self.layout.addSpacing(40)

        done_btn = QPushButton("let's go")
        done_btn.setFont(font2)
        done_btn.setFixedWidth(200)
        done_btn.setStyleSheet('''QPushButton{
                                background: white;
                                padding: 7px;
                                border-radius: 10px;
                               }
                               QPushButton:hover{
                                background: rgb(200, 200, 200);
                               }''')
        self.layout.addWidget(done_btn, alignment=QtCore.Qt.AlignCenter)

        # ----------------------------------------------- functions

        done_btn.clicked.connect(exit)

class MakeUsbWin(QDialog):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('assets/font1.otf')
        font_family1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font_id = QFontDatabase.addApplicationFont('assets/font2.ttf')
        font_family2 = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family1, 14)
        font2 = QFont(font_family2, 16)
        font_small_2 = QFont(font_family2, 11)

        self.setWindowTitle('pass-tangle setup')
        self.setFixedHeight(win_heigth)
        self.setFixedWidth(win_width)
        self.setStyleSheet('background: black;')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.move(x, y)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.setContentsMargins(10, 10, 10, 10)

        close_btn = QPushButton()
        close_btn.setFixedHeight(15)
        close_btn.setFixedWidth(15)
        close_btn.setStyleSheet('''
                                QPushButton{
                                    background: white;
                                    border-radius: 5px;
                                }
                                QPushButton:hover{
                                    background: rgb(252, 5, 116);
                                }
                                ''')
        self.layout.addWidget(close_btn, alignment=QtCore.Qt.AlignRight)
        self.layout.addSpacing(2)

        # ----------------------------------------------- layout

        choose_drive_text = QLabel('  Choose drives to set key:')
        choose_drive_text.setFont(font2)
        choose_drive_text.setStyleSheet('color: white;')
        self.layout.addWidget(choose_drive_text)
        self.layout.addSpacing(4)

        drives_container = QFrame()
        drives_container.setStyleSheet('''
                                       color: white;
                                       background: rgb(30, 30, 30);
                                       border-radius: 10px;
                                       ''')
        drives_container.setContentsMargins(0, 0, 0, 0)
        self.drives_layout = QVBoxLayout()
        self.drives_layout.setAlignment(QtCore.Qt.AlignTop)
        drives_container.setLayout(self.drives_layout)
        self.drives_layout.setSpacing(10)

        drives_scroll_area = QScrollArea()
        drives_scroll_area.setWidgetResizable(True)
        drives_scroll_area.setStyleSheet('''
                                         color: white;
                                         border-radius: 0px;
                                         ''')
        drives_scroll_area.setFixedWidth(350)
        drives_scroll_area.setFixedHeight(100)
        drives_scroll_area.setWidget(drives_container)
        self.layout.addWidget(drives_scroll_area, alignment=QtCore.Qt.AlignCenter)
        self.layout.addSpacing(10)

        refresh_btn = QPushButton('refresh')
        refresh_btn.setFixedWidth(100)
        refresh_btn.setStyleSheet('''
                                  QPushButton{
                                    color: white;
                                    background: black;
                                    border: solid white;
                                    border-width: 1px;
                                    border-radius: 5px;
                                    padding-top: 2px;
                                    padding-bottom: 2px;
                                  }
                                  QPushButton:hover{
                                    background: white;
                                    color: black;
                                  }
                                  ''')
        refresh_btn.setFont(font_small_2)
        self.layout.addWidget(refresh_btn, alignment=QtCore.Qt.AlignCenter)
        self.layout.addSpacing(20)

        allowed_drives_text = [
            "Choosing recovery device is adviced",
            "(just pick multiple USBs).",
            '',
            "Only removable drives (USBs) are",
            "displayed here (hard drives are",
            "not accepted)."
        ]
        allowed_drives_text = '\n'.join(allowed_drives_text)
        
        allowed_drives_text_label = QLabel(allowed_drives_text)
        allowed_drives_text_label.setStyleSheet('color: white;')
        allowed_drives_text_label.setFont(font2)
        self.layout.addWidget(allowed_drives_text_label, alignment=QtCore.Qt.AlignCenter)
        self.layout.addSpacing(22)

        make_drives_btn = QPushButton('generate key')
        make_drives_btn.setFont(font2)
        make_drives_btn.setFixedHeight(40)
        make_drives_btn.setFixedWidth(270)
        make_drives_btn.setStyleSheet('''QPushButton{
                                    background: white;
                                    border-radius: 10px
                                }
                                QPushButton:hover{
                                    background: rgb(210, 210, 210);
                                }''')
        self.layout.addWidget(make_drives_btn, alignment=QtCore.Qt.AlignCenter)

        # ----------------------------------------------- functions

        self.refreshDrives()

        close_btn.clicked.connect(self.close)
        refresh_btn.clicked.connect(self.refreshDrives)
        make_drives_btn.clicked.connect(self.makeDrive)
    
    def refreshDrives(self):
        while self.drives_layout.count():
            item = self.drives_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.device_lsit = dataLoader.check_connected_usb()

        if self.device_lsit:
            self.device_widget_list = []
            self.check_box_list = []

            for i, device in enumerate(self.device_lsit):
                device = device.replace('\\', '')
                temp_frame = QFrame()
                temp_frame.setStyleSheet('''
                                            background: black;
                                            border-radius: 10px;
                                        ''')
                temp_layout = QHBoxLayout()
                temp_frame.setLayout(temp_layout)

                temp_widget = QLabel(device)
                temp_widget.setStyleSheet('padding: 3px;')
                temp_widget.setFont(self.font)
                temp_layout.addWidget(temp_widget)

                check_btn = QCheckBox()
                temp_layout.addWidget(check_btn, alignment=QtCore.Qt.AlignRight)
                self.check_box_list.append(check_btn)
    
                self.device_widget_list.append(temp_frame)
                self.drives_layout.addWidget(self.device_widget_list[i])

            for box in self.check_box_list:
                box.installEventFilter(self)
            self.checked_active = []
        else:
            temp_frame = QFrame()
            temp_frame.setStyleSheet('''
                                        background: black;
                                        border-radius: 10px;
                                    ''')
            temp_layout = QHBoxLayout()
            temp_frame.setLayout(temp_layout)

            temp_widget = QLabel('No devices found!')
            temp_widget.setAlignment(QtCore.Qt.AlignCenter)
            temp_widget.setStyleSheet('padding: 3px;')
            temp_widget.setFont(self.font)
            temp_layout.addWidget(temp_widget)
            self.drives_layout.addWidget(temp_frame)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            for i, box in enumerate(self.check_box_list):
                if box == obj:
                    
                    if obj.isChecked():
                        obj.setChecked(False)
                        
                        if i in self.checked_active:
                            self.checked_active.remove(i)
                    else:
                        obj.setChecked(True)

                        if i not in self.checked_active:
                            self.checked_active.append(i)
                    return True
        return False

    def makeDrive(self):
        if self.checked_active:
            message = ['WARNING! If selected devices have',
                            'key on them, key will be overwrited',
                            'with new one (old will be lost).']
            message = '\n'.join(message)

            dialog_box = CChooseWin(message)
            if dialog_box.exec_() == QDialog.Accepted:
                
                key = Fernet.generate_key()
                for id in self.checked_active:
                    file_path = self.device_lsit[id] + 'derypt.cdk'
                    with open(file_path, 'wb') as file:
                        file.write(key)
                del key

                os.mkdir('data')
                with open('data/data.cpmpd', 'w') as file:
                    pass
                with open('data/platform.cpmpd', 'w') as file:
                    pass

                dialog_box = SetupDoneWin()
                dialog_box.exec_()

        else:
            dialog_box = CAcceptWin('No drives selected')
            dialog_box.exec_()

class CChooseWin(QDialog):
    def __init__(self, message):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('assets/font2.ttf')
        font_family2 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font2 = QFont(font_family2, 12)

        a = (width-350) // 2
        w = (height-220) // 2
        
        self.move(a, w)
        self.setWindowTitle('pass-tangle setup')
        self.setFixedHeight(220)
        self.setFixedWidth(350)
        self.setStyleSheet('background: rgba(0,0,0,0);')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        container_layout = QVBoxLayout()
        self.setLayout(container_layout)
        container_frame = QFrame()
        container_frame.setStyleSheet('''
                                      background: white;
                                      border-radius: 30px;
                                      ''')
        container_layout.addWidget(container_frame)


        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        container_frame.setLayout(layout)
        layout.addSpacing(20)

        message_label = QLabel(message)
        message_label.setFont(font2)
        layout.addWidget(message_label)
        layout.addSpacing(10)

        ok_btn = QPushButton('ok')
        cancel_btn = QPushButton('cancel')
        for button in [ok_btn, cancel_btn]:
            button.setStyleSheet('''QPushButton{
                                    background: black;
                                    color: white;
                                    border-radius: 10px;
                                    padding: 5px;
                                }
                                QPushButton:hover{
                                    background: rgb(70, 70, 70);
                                }
                                ''')
            button.setFixedWidth(100)
            button.setFont(font2)
            layout.addWidget(button, alignment=QtCore.Qt.AlignCenter)

        # ------------------------------------- functions

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

class CAcceptWin(QDialog):
    def __init__(self, message):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('assets/font1.otf')
        font_family1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font_id = QFontDatabase.addApplicationFont('assets/font2.ttf')
        font_family2 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family1, 14)
        font2 = QFont(font_family2, 16)
        font_small_2 = QFont(font_family2, 11)
        font_big = QFont(font_family1, 23)
        font_big_2 = QFont(font_family2, 23)

        a = (width-350) // 2
        w = (height-200) // 2
        
        self.move(a, w)
        self.setWindowTitle('pass-tangle setup')
        self.setFixedHeight(200)
        self.setFixedWidth(350)
        self.setStyleSheet('background: rgba(0,0,0,0);')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        container_layout = QVBoxLayout()
        self.setLayout(container_layout)
        container_frame = QFrame()
        container_frame.setStyleSheet('''
                                      background: white;
                                      border-radius: 30px;
                                      ''')
        container_layout.addWidget(container_frame)


        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        container_frame.setLayout(layout)
        layout.addSpacing(20)

        message_label = QLabel(message)
        message_label.setFont(font2)
        layout.addWidget(message_label)
        layout.addSpacing(10)

        ok_btn = QPushButton('ok')
        ok_btn.setStyleSheet('''QPushButton{
                                background: black;
                                color: white;
                                border-radius: 10px;
                                padding: 5px;
                             }
                             QPushButton:hover{
                                background: rgb(70, 70, 70);
                             }
                             ''')
        ok_btn.setFont(font2)
        layout.addWidget(ok_btn)

        # ------------------------------------- functions

        ok_btn.clicked.connect(self.close)

class SetupWin(QDialog):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('assets/font2.ttf')
        font_family2 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font2 = QFont(font_family2, 16)

        self.setWindowTitle('pass-tangle setup')
        self.setFixedHeight(win_heigth)
        self.setFixedWidth(win_width)
        self.setStyleSheet('background: black;')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.move(x, y)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.setContentsMargins(10, 10, 10, 10)

        close_btn = QPushButton()
        close_btn.setFixedHeight(15)
        close_btn.setFixedWidth(15)
        close_btn.setStyleSheet('''
                                QPushButton{
                                    background: white;
                                    border-radius: 5px;
                                }
                                QPushButton:hover{
                                    background: rgb(252, 5, 116);
                                }
                                ''')
        self.layout.addWidget(close_btn, alignment=QtCore.Qt.AlignRight)
        self.layout.addSpacing(40)

        setup_text_1 = [
            'In this setup encryption key for',
            'your passwords will be created',
            'on your USB drive.',
            '',
            'WARNING: if you lose encryption',
            "key, it's not possible to",
            'recover your passwords anymore.',
            '',
            'To prevent this, you can choose',
            'multiple USB devices in the next',
            'step.'
        ]
        setup_text_1 = '\n'.join(setup_text_1)
        
        setup_text_label_1 = QLabel(setup_text_1)
        setup_text_label_1.setStyleSheet('color: white;')
        setup_text_label_1.setFont(font2)
        self.layout.addWidget(setup_text_label_1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addSpacing(40)

        next_btn = QPushButton('next step')
        next_btn.setFont(font2)
        next_btn.setFixedHeight(40)
        next_btn.setFixedWidth(270)
        next_btn.setStyleSheet('''QPushButton{
                                    background: white;
                                    border-radius: 10px
                                }
                                QPushButton:hover{
                                    background: rgb(210, 210, 210);
                                }''')
        self.layout.addWidget(next_btn, alignment=QtCore.Qt.AlignCenter)

        # ----------------------------------------------- functions

        close_btn.clicked.connect(self.close)
        next_btn.clicked.connect(self.nextStep)

    def nextStep(self):
        dialog_box = MakeUsbWin()
        dialog_box.exec_()

class WelcomeWindow(QFrame):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont('assets/font1.otf')
        font_family1 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font_id = QFontDatabase.addApplicationFont('assets/font2.ttf')
        font_family2 = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family1, 14)
        font2 = QFont(font_family2, 16)
        font_big = QFont(font_family1, 23)

        self.setWindowTitle('pass-tangle setup')
        self.setFixedHeight(win_heigth)
        self.setFixedWidth(win_width)
        self.setStyleSheet('background: black;')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.move(x, y)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.setContentsMargins(10, 10, 10, 10)

        close_btn = QPushButton()
        close_btn.setFixedHeight(15)
        close_btn.setFixedWidth(15)
        close_btn.setStyleSheet('''
                                QPushButton{
                                    background: white;
                                    border-radius: 5px;
                                }
                                QPushButton:hover{
                                    background: rgb(252, 5, 116);
                                }
                                ''')
        self.layout.addWidget(close_btn, alignment=QtCore.Qt.AlignRight)
        self.layout.addSpacing(40)

        pixmap = QPixmap('assets/lock.png').scaled(80, 80)
        icon_box = QLabel()
        icon_box.setPixmap(pixmap)
        self.layout.addWidget(icon_box, alignment=QtCore.Qt.AlignCenter)
        self.layout.addSpacing(30)

        welcome_label = QLabel('Welcome,')
        welcome_label.setFont(font_big)
        welcome_message_label = QLabel('to pass-tangle, your\nrectangle for passwords')
        welcome_message_label.setAlignment(QtCore.Qt.AlignCenter)
        welcome_message_label.setFont(font)
        
        for label in [welcome_label, welcome_message_label]:
            label.setStyleSheet('color: white;')
            self.layout.addWidget(label, alignment=QtCore.Qt.AlignCenter)
            self.layout.addSpacing(10)
        self.layout.addSpacing(20)

        setup_btn = QPushButton('setup')
        setup_btn.setFont(font2)
        setup_btn.setFixedHeight(40)
        setup_btn.setFixedWidth(270)
        setup_btn.setStyleSheet('''QPushButton{
                                    background: white;
                                    border-radius: 10px
                                }
                                QPushButton:hover{
                                    background: rgb(210, 210, 210);
                                }''')
        self.layout.addSpacing(10)
        self.layout.addWidget(setup_btn, alignment=QtCore.Qt.AlignCenter)


        # ----------------------------------------------- functions

        close_btn.clicked.connect(self.close)
        setup_btn.clicked.connect(self.runSetup)

    def runSetup(self):
        dialog_box = SetupWin()
        dialog_box.exec_()
        

AppHandler = QApplication(sys.argv)
App = WelcomeWindow()
App.show()
sys.exit(AppHandler.exec_())