import mediapipe as mp
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent, QTimer
import json, os
from bluetooth import Bluetooth
from camera_func import Tracking
from Keyboard import SoftKeyboardDialog
from database import DB


class Youme(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Tracking 쓰레드
        self.tracking_thread = Tracking()
        self.tracking_thread.result_signal.connect(self.update_cam_label)

        # bluetooth 쓰레드
        self.bluetooth_thread = Bluetooth()
        self.bluetooth_thread.result_signal.connect(self.handle_bluetooth_message)
        self.bluetooth_thread.start()

        # DB 클래스
        self.db = DB()

        self.area = None

        self.line_edits = []
        self.InitUI()


    def InitUI(self):
        self.setWindowTitle("Youme Camera")

        self.setFixedSize(800, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.cam_layout = QHBoxLayout()
        self.func_layout = QVBoxLayout()

        self.main_layout.addLayout(self.cam_layout, 7)
        self.main_layout.addLayout(self.func_layout, 3)

        # 카메라 영상 표시용 QLabel
        self.cam_label = QLabel(self)
        self.cam_label.setAlignment(Qt.AlignCenter)
        self.cam_label.setFixedSize(640, 400)

        self.cam_layout.addWidget(self.cam_label)

        self.start_btn = QPushButton("START")
        self.stop_btn = QPushButton("STOP")
        self.map_btn = QPushButton("MAP")
        self.edit_item = QPushButton("Edit")
        self.close_btn = QPushButton("Close")

        self.func_layout.addWidget(self.start_btn)
        self.func_layout.addWidget(self.stop_btn)
        self.func_layout.addWidget(self.map_btn)
        self.func_layout.addWidget(self.edit_item)
        self.func_layout.addWidget(self.close_btn)

        self.start_btn.clicked.connect(self.start_cam)
        self.stop_btn.clicked.connect(self.stop_cam)
        self.map_btn.clicked.connect(self.map)
        self.edit_item.clicked.connect(self.edit)
        self.close_btn.clicked.connect(self.close)

        self.stop_btn.setEnabled(False)

        self.cam_label.mousePressEvent = self.tracking_thread.select_roi

    
    def update_cam_label(self, pixmap):
        # 카메라 영상 업데이트 (UI에서 QImage를 QLabel로 표시)
        self.cam_label.setPixmap(pixmap)


    def start_cam(self):
        # 카메라 시작
        self.tracking_thread.start()
        self.tracking_thread.result_signal.connect(self.update_cam_label)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)


    def stop_cam(self):
        # 카메라 종료
        self.tracking_thread.stop()
        QTimer.singleShot(0, self.cam_label.clear)
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
            

    def map(self):
        self.map_dialog = QDialog(self)
        self.map_dialog.setWindowTitle("Map Dialog")
        self.map_dialog.setFixedSize(800,480)

        map_layout = QVBoxLayout()
        self.line_edits = []

        # 검색창
        search_input = QLineEdit()
        search_input.installEventFilter(self)
        self.search_input = search_input
        search_input.setPlaceholderText("품목을 입력하세요...")
        self.line_edits.append(search_input)

        # 검색 버튼
        search_button = QPushButton("검색")
        search_button.clicked.connect(self.select_item)
        # 닫기 버튼
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.map_dialog.close)

        # 레이아웃 구성
        youme_map = QLabel()
        youme_map.mousePressEvent = self.select_location
        youme_map.setFixedSize(778, 360)

        #pixmap = QPixmap('/home/jsh/YOUME/youme/src/kimgunhee/imgs/map.png')
        pixmap = QPixmap('C:\youme\youme\src\kimgunhee\imgs\map.png')
        youme_map.setPixmap(pixmap)

        map_layout.addWidget(youme_map)

        map_layout.addWidget(search_input)
        map_layout.addWidget(search_button)
        map_layout.addWidget(close_btn)

        self.map_dialog.setLayout(map_layout)
        self.map_dialog.exec_()
        

    def select_item(self):
        name = self.search_input.text().strip()
        print(name)
        locations = self.db.search_item(name)
        locations_text = ', '.join(locations)+'에 있습니다.' if locations else "등록된 구역이 없습니다."

        QMessageBox.information(self.map_dialog, f"{name}", f"{locations_text}")
        

    def select_location(self, event):
        x, y = event.x(), event.y()

        if x < 389 and y < 180:
            self.area = "A"
        elif x < 389 and y >= 180:
            self.area = "B"
        elif x >= 389 and y < 180:
            self.area = "C"
        else:
            self.area = "D"

        items = self.db.search_location(self.area)
        print(items)
        item_text = ', '.join(items) if items else "등록된 항목이 없습니다."

        QMessageBox.information(self, f"{self.area} 구역", f"{self.area} 구역에 있는 항목:\n{item_text}")


    def eventFilter(self, obj, event):
        if isinstance(obj, QLineEdit) and event.type() == QEvent.MouseButtonPress:
            if obj in getattr(self, "line_edits", []):
                keyboard = SoftKeyboardDialog(obj)
                keyboard.exec_()
                return True
        return super().eventFilter(obj, event)
    

    def edit(self):
        self.edit_dialog = QDialog()
        self.edit_dialog.setWindowTitle("Edit Dialog")
        self.edit_dialog.setFixedSize(800, 480)

        main_layout = QVBoxLayout()
        self.edit_dialog.setLayout(main_layout)

        button_layout = QHBoxLayout()
        add_item_btn = QPushButton("ADD Item")
        remove_item_btn = QPushButton("REMOVE Item")
        button_layout.addWidget(add_item_btn)
        button_layout.addWidget(remove_item_btn)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        dynamic_widget = QWidget()
        self.dynamic_layout = QVBoxLayout(dynamic_widget)
        dynamic_widget.setLayout(self.dynamic_layout)

        scroll_area.setWidget(dynamic_widget)
        main_layout.addWidget(scroll_area)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.edit_dialog.close)
        main_layout.addWidget(close_btn)

        def clear_dynamic_layout():
            while self.dynamic_layout.count():
                child = self.dynamic_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()


        # === ADD ITEM ===
        def show_add_fields():
            clear_dynamic_layout()
            self.line_edits = []

            area_select = QComboBox()
            locations = self.db.search_location('*')
            area_select.addItems(['select location'] + locations)
            self.dynamic_layout.addWidget(area_select)

            # 검색창
            item_input = QLineEdit()
            item_input.installEventFilter(self)
            self.item_input = item_input
            item_input.setPlaceholderText("추가할 품목명을 입력하세요")
            self.line_edits.append(item_input)
            self.dynamic_layout.addWidget(item_input)

            confirm_btn = QPushButton("추가하기")
            self.dynamic_layout.addWidget(confirm_btn)

            def on_confirm():
                name = item_input.text().strip()
                area = area_select.currentText()
                if name and area!='select location':
                    self.add_item(name, area)

            confirm_btn.clicked.connect(on_confirm)

        # === REMOVE ITEM ===
        def show_remove_message():
            clear_dynamic_layout()
            self.line_edits = []

            # 검색창
            item_remove = QLineEdit()
            item_remove.installEventFilter(self)
            self.item_remove = item_remove
            item_remove.setPlaceholderText("추가할 품목명을 입력하세요")
            self.line_edits.append(item_remove)
            self.dynamic_layout.addWidget(item_remove)

            confirm_btn = QPushButton("삭제하기")
            self.dynamic_layout.addWidget(confirm_btn)

            def on_remove():
                name = item_remove.text().strip()
                if name:
                    self.remove_item(name)

            confirm_btn.clicked.connect(on_remove)

        add_item_btn.clicked.connect(show_add_fields)
        remove_item_btn.clicked.connect(show_remove_message)

        self.edit_dialog.exec_()


    def add_item(self, name, area):
        try:
            self.db.add_item(area, name)
            QMessageBox.information(self.edit_dialog, "아이템 추가 결과", f"{area}에 {name}이 추가되었습니다.")
        except:
            QMessageBox.warning(self.edit_dialog, "아이템 추가 결과", "실패하였습니다.")


    def remove_item(self, name):
        try:
            flg = self.db.remove_item(name)
            if flg==2:
                QMessageBox.information(self.edit_dialog, "아이템 삭제 결과", f"{name}이 한 개 삭제되었습니다.")
            elif flg==1:
                QMessageBox.information(self.edit_dialog, "아이템 삭제 결과", f"{name}이 삭제되었습니다.")
            else:
                QMessageBox.information(self.edit_dialog, "아이템 삭제 결과", f"{name}이 없습니다.")
        except:
            QMessageBox.information(self.edit_dialog, "아이템 삭제 결과", "실패하였습니다.")


    def handle_bluetooth_message(self, data):
        if str(data):
            print(f"[Youme] 새 메시지: {data}")
            self.db.search_by_id_and_log_usage(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    youme = Youme()
    youme.show()
    sys.exit(app.exec_())