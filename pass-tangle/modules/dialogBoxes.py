#!/usr/bin/env python3

'''module: dialogBoxes'''

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget
import pyperclip
try:
    import dataLoader
except:
    from modules import dataLoader

class CAcceptWin(QDialog):

    def __init__(self, message):
        super().__init__()
        font = QFont('None', 17)
        
        self.setFont(font)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedWidth(400)
        self.setWindowTitle('Info Box')

        layout = QVBoxLayout()
        self.setLayout(layout)

        message_label = QLabel(message)

        ok_btn = QPushButton('ok')
        ok_btn.setFont(font)
        ok_btn.setStyleSheet('background: rgb(230,230,230);')

        layout.addWidget(message_label)
        layout.addWidget(ok_btn)

        ok_btn.clicked.connect(self.close)

class CAddWin(QDialog):

    textEntered = QtCore.pyqtSignal(list)

    def __init__(self, title):
        super().__init__()
        self.title = title
        font = QFont('None', 17)
        font_small = QFont('None', 13)
        self.setFont(font)

        self.setWindowTitle('Add record')
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # ------------------------------------------------- layout

        # ------------------------ title bar & setup
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet('padding: 0px;'
                           'background: rgb(100, 100, 100);')
        self.setLayout(container_layout)

        exit_btn = QPushButton('X')
        exit_btn.setFont(font_small)
        exit_btn.setFixedHeight(22)
        exit_btn.setFixedWidth(22)
        exit_btn.setStyleSheet('background: rgb(230,230,230);')
        container_layout.addWidget(exit_btn)


        title_bar_container = QFrame()
        title_bar_container.setContentsMargins(5, 15, 5, 5)
        title_bar_container.setStyleSheet('background: white;')
        
        container_layout.addWidget(title_bar_container)

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(15)
        title_bar_container.setLayout(layout)

        # ------------------------ window elements
        title_text = QLabel('Add credentials for:\n' + title)
        title_text.setFont(font)

        login_text = QLabel('login:')
        pass_text = QLabel('password:')
        for item in [login_text, pass_text]:
            item.setFont(font_small)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText('login')
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText('password')
        submit_btn = QPushButton('enter')
        for item in [self.login_input, self.pass_input, submit_btn]:
            item.setFont(font)
            #item.setFixedHeight(40)
            item.setStyleSheet('background: rgb(230,230,230);'
                               'padding-left: 2px;'
                               'padding-right: 2px;')

        add_order = [title_text, login_text, self.login_input, pass_text, self.pass_input, submit_btn]

        for widget in add_order:
            layout.addWidget(widget)

        # ------------------------------------------------- functions
        exit_btn.clicked.connect(self.close)
        submit_btn.clicked.connect(self.sendText)

    def sendText(self):
        temp_log = self.login_input.text()
        temp_pas = self.pass_input.text()
        if temp_log and temp_pas:
            text = [self.title, temp_log, temp_pas]
            self.textEntered.emit(text)
            self.close()
        else:
            dialog_box = CAcceptWin("Password or login can't be empty")
            dialog_box.exec_()

class CDisplayWin(QDialog):
    def __init__(self, data):
        super().__init__()

        font = QFont('None', 17)
        font_small = QFont('None', 13)
        font_very_small = QFont('None', 9)
        self.setFont(font)

        self.move(10, 10)
        self.setWindowTitle('Pass Show')
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet('padding: 0px;'
                           'background: rgb(100, 100, 100);')
        self.setLayout(container_layout)

        exit_btn = QPushButton('X')
        exit_btn.setFont(font_small)
        exit_btn.setFixedHeight(22)
        exit_btn.setFixedWidth(22)
        exit_btn.setStyleSheet('background: rgb(230,230,230);')
        container_layout.addWidget(exit_btn)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        title_bar_container = QWidget()
        scroll_area.setWidget(title_bar_container)
        container_layout.addWidget(scroll_area)
        title_bar_container.setContentsMargins(5,0,5,0)
        title_bar_container.setStyleSheet('background: white;')

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(15)
        
        
        title_bar_container.setLayout(layout)

        title_label = QLabel('Show credentials for:\n' + data[0][0])
        title_label.setFont(font)
        layout.addSpacerItem(QSpacerItem(10, 10))
        layout.addWidget(title_label)

        labels_list = []
        for i, record in enumerate(data):
            temp_login_label = QPushButton(record[1])
            temp_password_label = QPushButton(record[2])
            
            for label in [temp_login_label, temp_password_label]:
                label.setStyleSheet("""
                                    background: rgb(230,230,230);
                                    padding-top: 5px;
                                    padding-bottom: 5px;
                                    """)
                
            login_text = QLabel('login:')
            password_text = QLabel('password:')
            click_to_copy_text_1 = QLabel('(click to copy)')
            click_to_copy_text_2 = QLabel('(click to copy)')
            
            for label in [login_text, password_text]:
                label.setFont(font_small)

            for label in [click_to_copy_text_1, click_to_copy_text_2]:
                label.setFont(font_very_small)
            
            temp_label_record = [temp_login_label, temp_password_label]
            
            labels_list.append(temp_label_record)
            
            layout.addWidget(login_text)
            labels_list[i][0].installEventFilter(self)
            labels_list[i][0].setFont(font)
            layout.addWidget(labels_list[i][0])
            layout.addWidget(click_to_copy_text_1, alignment=QtCore.Qt.AlignCenter)
            
            layout.addWidget(password_text)
            labels_list[i][1].installEventFilter(self)
            labels_list[i][1].setFont(font)
            layout.addWidget(labels_list[i][1])
            layout.addWidget(click_to_copy_text_2, alignment=QtCore.Qt.AlignCenter)

            spacer = QPushButton()
            spacer.setStyleSheet('background: rgb(230,230,230);')
            layout.addWidget(spacer)
        
        # ------------------------------------------------- functions
        
        exit_btn.clicked.connect(self.close)

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:
            pyperclip.copy(obj.text())
        
        return False
    
class CChooseWin(QDialog):
    def __init__(self, message):
        super().__init__()
        font = QFont('None', 17)
        self.setFont(font)

        self.setWindowTitle('Choose')
        self.setFixedWidth(400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        message_label = QLabel(message)
        layout.addWidget(message_label, alignment=QtCore.Qt.AlignCenter)

        accept_btn = QPushButton('ok')
        cancel_btn = QPushButton('cancel')
        for button in [accept_btn, cancel_btn]:
            button.setStyleSheet('background: rgb(230, 230, 230)')
            button.setFont(font)

        btn_layout = QHBoxLayout()
        btn_container = QFrame()
        btn_container.setLayout(btn_layout)
        layout.addWidget(btn_container)

        btn_layout.addWidget(accept_btn)
        btn_layout.addWidget(cancel_btn)

        # ----------------------------------- functions

        accept_btn.clicked.connect(lambda: self.accept())
        cancel_btn.clicked.connect(lambda: self.reject())

class CEditRecord(QDialog):
    button_clicked = QtCore.pyqtSignal(list)

    def __init__(self, current_record):
        super().__init__()
        font = QFont('None', 17)

        self.setFont(font)
        self.setWindowTitle('Edit')
        self.setStyleSheet('background: rgb(220, 220, 220)')
        self.setFixedHeight(500)
        self.setFixedWidth(400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.platform = current_record[0]

        title = QLabel('Record for: \n' + self.platform)
        title.setStyleSheet('background: rgb(200, 200, 200)')
        title.setContentsMargins(10, 0, 10, 0)
        title.setFixedHeight(70)
        title.setFont(font)

        self.login_holder = QLineEdit(current_record[1])
        self.pass_holder = QLineEdit(current_record[2])
        for holder in [self.login_holder, self.pass_holder]:
            holder.setStyleSheet('background: rgb(230, 230, 230);')
            holder.setFont(font)

        save_btn = QPushButton('save')
        save_btn.setStyleSheet('background: rgb(230, 230, 230);')
        save_btn.setFont(font)

        self.setContentsMargins(15, 5, 15, 5)
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(35)
        self.setLayout(layout)

        layout.addWidget(title)
        layout.addWidget(self.login_holder)
        layout.addWidget(self.pass_holder)
        layout.addWidget(save_btn)

        # ---------------------------------------------  functions

        save_btn.clicked.connect(self.cSave)

    def cSave(self):

        signal_list = []

        signal_list.append(self.platform)
        signal_list.append(self.login_holder.text())
        signal_list.append(self.pass_holder.text())

        self.button_clicked.emit(signal_list)

        del signal_list
        self.close()

class CMoreWin(QDialog):

    def __init__(self, data):
        super().__init__()
        font = QFont('None', 17)
        font_small = QFont('None', 13)
        self.setFont(font)

        self.setWindowTitle('More')
        self.setFixedWidth(400)
        self.setFixedHeight(500)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # ------------------------------------------------- layout

        # ------------------------ title bar & setup
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet('padding: 0px;'
                           'background: rgb(100, 100, 100);')
        self.setLayout(container_layout)

        exit_btn = QPushButton('X')
        exit_btn.setFont(font_small)
        exit_btn.setFixedHeight(22)
        exit_btn.setFixedWidth(22)
        exit_btn.setStyleSheet('background: rgb(230,230,230);')
        container_layout.addWidget(exit_btn)


        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        title_bar_container = QWidget()
        scroll_area.setWidget(title_bar_container)
        container_layout.addWidget(scroll_area)
        title_bar_container.setContentsMargins(5, 15, 5, 5)
        title_bar_container.setStyleSheet('background: white;')

        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(15)
        title_bar_container.setLayout(self.layout)

        # ------------------------ window elements

        search_container = QFrame()
        self.layout.addWidget(search_container)
        search_layout = QHBoxLayout()
        search_container.setLayout(search_layout)

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText('enter login or platform')
        self.search_line.setFont(font_small)
        self.search_line.setStyleSheet('''
                             background: rgb(230, 230, 230);
                             padding-left: 3px;
                             padding-right: 3px;
                             ''')
        search_layout.addWidget(self.search_line)
        
        search_btn = QPushButton('search')
        search_btn.setStyleSheet('''
                                 background: rgb(230, 230, 230);
                                 padding-left: 10px;
                                 padding-right: 10px;
                                 ''')
        search_btn.setFont(font_small)
        search_layout.addWidget(search_btn)

        self.no_records = QLabel('no records found')
        self.no_records.setFont(font)
        self.no_records.setStyleSheet('''
                                      background: rgb(200,200,200);
                                      padding: 20px;
                                      ''')
        if len(data) == 0:
            self.layout.addWidget(self.no_records)

        self.record_boxes = []

        for i, record in enumerate(data):
            
            record_container = QFrame()
            record_container.setStyleSheet('background: rgb(200,200,200);')
            record_layout = QVBoxLayout()
            record_layout.setSpacing(0)
            record_layout.setContentsMargins(10, 15, 10, 15)
            record_container.setLayout(record_layout)

            text = QLabel(record[0] + ':  ' + record[1])
            text.setFont(font)
            text.setStyleSheet('padding-left: 10px')
            record_layout.addWidget(text)
            
            btn_container = QFrame()
            record_layout.addWidget(btn_container)
            btn_layout = QHBoxLayout()
            btn_container.setLayout(btn_layout)

            edit_btn = QPushButton('edit')
            edit_btn.installEventFilter(self)
            btn_layout.addWidget(edit_btn)

            remove_btn = QPushButton('remove')
            remove_btn.installEventFilter(self)
            btn_layout.addWidget(remove_btn)

            for button in [edit_btn, remove_btn]:
                button.setFont(font)
                button.setStyleSheet('background: white')

            self.record_boxes.append(record_container)
            self.layout.addWidget(self.record_boxes[i])

        # ------------------------------------------------- functions
        
        exit_btn.clicked.connect(self.close)
        search_btn.clicked.connect(self.CSearch)

    def eventFilter(self, obj, event):

        def isChild(widget, parent):
            while widget is not None:
                if widget == parent:
                    return True
                widget = widget.parentWidget()
            return False
        
        if event.type() == event.MouseButtonPress:
            for i, record in enumerate(self.record_boxes):
                if isChild(obj, record):
                    if dataLoader.check_data_file():
                        self.cpm_data = dataLoader.DataManagement()

                    if obj.text() == 'remove':
                        self.delRecord(i)

                    elif obj.text() == 'edit':
                        self.editRecord(i)

                    del self.cpm_data
                    break
        return False
    
    def delRecord(self, id):
        dialog_box = CChooseWin('Are you sure?')

        if dialog_box.exec_():
            self.layout.removeWidget(self.record_boxes[id])
            self.record_boxes[id].hide()
            self.record_boxes.pop(id)

            if len(self.record_boxes) == 0:
                self.layout.addWidget(self.no_records)
                self.no_records.show()

            self.cpm_data.remove_record(id)
        else:
            pass

    def editRecord(self, id):

        self.id = id

        rec_to_send = self.cpm_data.show_by_id(id)

        dialog_box = CEditRecord(rec_to_send)
        dialog_box.button_clicked.connect(self.handle_edit_signal)
        dialog_box.exec_()

        del rec_to_send

    def handle_edit_signal(self, data):

        font = QFont('None', 17)

        self.cpm_data.edit_record(self.id, data)

        record_container = QFrame()
        record_container.setStyleSheet('background: rgb(200,200,200);')
        record_layout = QVBoxLayout()
        record_layout.setSpacing(0)
        record_layout.setContentsMargins(10, 15, 10, 15)
        record_container.setLayout(record_layout)       
        text = QLabel(data[0] + ':  ' + data[1])
        text.setFont(font)
        text.setStyleSheet('padding-left: 10px')
        record_layout.addWidget(text)

        btn_container = QFrame()
        record_layout.addWidget(btn_container)
        btn_layout = QHBoxLayout()
        btn_container.setLayout(btn_layout)     
        edit_btn = QPushButton('edit')
        edit_btn.installEventFilter(self)
        btn_layout.addWidget(edit_btn)      
        remove_btn = QPushButton('remove')
        remove_btn.installEventFilter(self)
        btn_layout.addWidget(remove_btn)        
        for button in [edit_btn, remove_btn]:
            button.setFont(font)
            button.setStyleSheet('background: white')

        self.record_boxes[self.id].hide()
        self.record_boxes[self.id] = record_container
        self.record_boxes[self.id].show()

        self.CSearch()


    def CClear(self):
        for record in self.record_boxes:
            try:
                self.layout.removeWidget(record)
                record.hide()
            except:
                pass
        try:
            self.layout.removeWidget(self.no_records)
            self.no_records.hide()
        except:
            pass

    def CSearch(self):
        
        self.CClear()

        if len(self.record_boxes) == 0:
            self.layout.addWidget(self.no_records)
            self.no_records.show()
            
        else:
            phrase = self.search_line.text().strip()
            if phrase == '':
                for record in self.record_boxes:
                    self.layout.addWidget(record)
                    record.show()
            else:
                empty = True
                for record in self.record_boxes:
                    text_line = record.findChild(QLabel)
                    if phrase in text_line.text():
                        self.layout.addWidget(record)
                        record.show()
                        empty = False
                if empty:
                    self.layout.addWidget(self.no_records)
                    self.no_records.show()