import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import serial


class Bluetooth(QThread):
    result_signal = pyqtSignal(object)

    def __init__(self, revc_port="COM8", baudrate=9600):
        super().__init__()
        self.recv_port = revc_port
        self.baudrate = baudrate
        self._running = True
        self.ser = None
        self.send_queue = []


    def run(self):
        while self._running:
            try:
                self.ser = serial.Serial(self.recv_port, self.baudrate, timeout=1)
                print("블루투스 연결 성공")
                break
            except serial.SerialException:
                print("블루투스 연결 대기 중...")
                time.sleep(1)

        try:
            time.sleep(2)

            while self._running:
                self.receive_message()
                self.send_message()
                time.sleep(0.1)

        except Exception as e:
            print('error')

        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()
            print('블루투스 연결 종료')

    def receive_message(self):
        """메시지를 수신하고 처리"""
        if self.ser.in_waiting:
            data = self.ser.readline().decode('utf-8').strip()
            self.result_signal.emit(data)
            self.handle_received_message(data)  # 오버라이드용 메서드

    def send_message(self):
        """메시지 큐에서 메시지를 보내기"""
        if self.send_queue:
            message = self.send_queue.pop(0)
            self.ser.write((message + '\n').encode())

   

    def send(self, message):
        self.send_queue.append(message)

    def stop(self):
        self._running = False
        self.wait()

    def handle_received_message(self, message):
        """하위 클래스에서 메시지를 받았을 때 행동 정의 가능"""
        pass
