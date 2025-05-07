import mediapipe as mp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import cv2


class Tracking(QThread):
    result_signal = pyqtSignal(QPixmap)  # QPixmap을 시그널로 전송

    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # 카메라 영상의 가로 길이를 640으로 설정
        self.cap.set(4, 400)  # 카메라 영상의 세로 길이를 400으로 설정

        self.cam_flg = 0
        self.running = False
        self.frame = None
        self.tracking = False
        self.detects = []
        #self.cascade = cv2.CascadeClassifier("/home/jsh/YOUME/youme/src/kimgunhee/haarcascade/haarcascade_frontalface_default.xml")
        self.cascade = cv2.CascadeClassifier("C:/youme/youme/src/kimgunhee/haarcascade/haarcascade_frontalface_default.xml")
        self.tracker = cv2.TrackerKCF_create()

        self.fall_detect_thread = Falldetect()
        self.fall_detect_thread.result_signal.connect(self.fall_detect_thread.handle_fall_result)

    def run(self):
        self.running = True
        while self.running:
            ret, self.frame = self.cap.read()
            fall_detect_frame = self.frame.copy()
            self.frame = cv2.flip(self.frame, 1)
            if ret:
                if self.frame is not None:
                    self.handle_tracking_result(self.frame)

                    # 얼굴 인식 및 트래킹 로직
                    if not self.tracking:
                        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                        self.detects = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                        for (x, y, w, h) in self.detects:
                            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        cv2.putText(self.frame, "Click a box to track", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    else:
                        success, box = self.tracker.update(self.frame)
                        if success:
                            x, y, w, h = [int(v) for v in box]
                            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(self.frame, "Tracking...", (x, y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        else:
                            cv2.putText(self.frame, "Tracking failure", (10, 60),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        self.fall_detect_thread.update_frame(fall_detect_frame)
                    # 프레임을 QPixmap으로 변환하여 시그널 발행
                    self.handle_tracking_result(self.frame)

            self.msleep(100)


    def stop(self):
        self.running = False
        self.tracking = False
        self.fall_detect_thread.stop()

        self.tracker = cv2.TrackerKCF_create()
        self.detects = []
        self.wait()


    def closeEvent(self, event):
        self.stop()
        # 종료 시 카메라 해제
        self.cap.release()
        event.accept()


    def handle_tracking_result(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.result_signal.emit(pixmap)


    def set_roi(self, roi):
        if self.frame is not None:
            self.tracker = cv2.TrackerKCF_create()
            self.tracker.init(self.frame, roi)

        self.tracking = True

        if not self.fall_detect_thread.isRunning():
            self.fall_detect_thread.start()


    def select_roi(self, event):
        if not self.running:
            print('작동 x')

        else:
            x, y = event.x(), event.y()
            if self.tracking:
                print("현재 추적 중")
                return

            detects = self.detects
    
            for (x1, y1, w, h) in detects:
                if x1 < x < x1 + w and y1 < y < y1 + h:
                    roi = (x1, y1, w, h)
                    self.set_roi(roi)
                    if not self.fall_detect_thread.isRunning():
                        self.fall_detect_thread.start()
                    print("Tracking 시작:", roi)
                    break


class Falldetect(QThread):
    result_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.running = False
        self.pose = mp.solutions.pose.Pose()
        self.frame = None
        self.emergency = 0


    def run(self):
        self.running = True
        while self.running:
            if self.frame is not None:
                rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(rgb)
                self.result_signal.emit(results)
            self.msleep(1000)


    def stop(self):
        self.running = False
        self.wait()


    def update_frame(self, frame):
        self.frame = frame


    def handle_fall_result(self, results):
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]

            if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
                print("양손을 들었습니다.")
                self.emergency+=1
                if self.emergency>=5:
                    print("응급상황 5초 이상 이상감지")