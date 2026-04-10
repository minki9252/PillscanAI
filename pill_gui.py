import os
import sys
import cv2
import requests
import PyQt5
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QTextEdit)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QFont
from ultralytics import YOLO

# --- [환경 설정: Qt 플러그인 경로] ---
dirname = os.path.dirname(PyQt5.__file__)
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')

# 모델 라벨 - 한글명 매핑
LABEL_TO_KOR = {
    "Famondine": "파모딘정", "Glomipide": "글로미피드정",
    "Loxoprofen": "경보록소프로펜나트륨수화물정", "Myoben": "미오벤정",
    "Bronpass": "브론패스정", "Cough": "코푸정",
    "Dexidiphen": "덱시디펜정400밀리그램", "Eupasidin": "유파시딘에스정"
}

# --- AI 추론 전용 스레드 ---
class DetectionThread(QThread):
    result_ready = pyqtSignal(object, object)

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.frame = None
        self.is_running = True

    def run(self):
        while self.is_running:
            if self.frame is not None:
                # 요구사항 성능(Performance) 0.5초 이내 달성을 위한 비동기 추론
                results = self.model(self.frame, conf=0.3, verbose=False)
                annotated_frame = results[0].plot()
                self.result_ready.emit(annotated_frame, results)
                self.frame = None 
            else:
                self.msleep(5)

class PillDetectorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 모델 로드
        self.model = YOLO(r'C:\Users\lms\OneDrive\문서\python\Pill_Detection\runs\detect\train8\weights\best.pt')
        
        self.det_thread = DetectionThread(self.model)
        self.det_thread.result_ready.connect(self.on_detection_finished)
        self.det_thread.start()
        
        # [상세주석] 요구사항 5.1(복수 알약 탐지) 처리를 위한 감지 이력 관리
        self.recent_detections = {} # {pill_name: last_detected_time}
        self.server_url = "http://127.0.0.1:5000/log"
        
        self.initUI()
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def initUI(self):
        self.setWindowTitle('스마트팩토리 알약 식별 자동화 시스템')
        self.setGeometry(100, 100, 1280, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 왼쪽 영역
        left_layout = QVBoxLayout()
        self.video_label = QLabel("카메라 로딩 중...")
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("background-color: black; border: 2px solid #34495E;")
        left_layout.addWidget(self.video_label)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(200)
        self.log_area.setStyleSheet("background-color: #F8F9F9; border: 1px solid #D5DBDB;")
        left_layout.addWidget(self.log_area)
        main_layout.addLayout(left_layout, stretch=1)

        # 오른쪽 영역
        right_layout = QVBoxLayout()
        self.name_label = QLabel("검수 대기 중")
        self.name_label.setFont(QFont("Malgun Gothic", 20, QFont.Bold))
        right_layout.addWidget(self.name_label)
        
        self.info_area = QTextEdit()
        self.info_area.setReadOnly(True)
        self.info_area.setStyleSheet("border: 2px solid #8E44AD; padding: 10px; background-color: white;")
        right_layout.addWidget(self.info_area)
        main_layout.addLayout(right_layout, stretch=1)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            if self.det_thread.frame is None:
                self.det_thread.frame = frame.copy()
            self.display_to_label(frame)

    def on_detection_finished(self, annotated_frame, results):
        self.display_to_label(annotated_frame)
        
        # [상세주석] 요구사항 5.1: 화면 내의 모든 알약을 루프로 순회하며 개별 트래킹
        if len(results[0].boxes) > 0:
            current_time = time.time()
            for box in results[0].boxes:
                pill_en = self.model.names[int(box.cls[0])]
                conf = float(box.conf[0])
                
                # 중복 전송 방지 로직 (동일 알약은 3초 이내에 다시 전송하지 않음)
                last_time = self.recent_detections.get(pill_en, 0)
                if current_time - last_time > 3.0:
                    self.recent_detections[pill_en] = current_time
                    self.process_detection(pill_en, conf)

    def display_to_label(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = rgb.shape
        q_img = QImage(rgb.data, w, h, c * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img).scaled(640, 480, Qt.KeepAspectRatio))

    def process_detection(self, pill_en, conf):
        kor_name = LABEL_TO_KOR.get(pill_en, pill_en)
        is_defect = conf < 0.75 
        status_str = "불량(의심)" if is_defect else "정상"
        
        title_color = "#C0392B" if is_defect else "#27AE60"
        self.name_label.setText(f"{kor_name}")
        self.name_label.setStyleSheet(f"color: {title_color};")

        # 공공데이터 API 호출
        url = 'http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService03/getMdcinGrnIdntfcInfoList03'
        params = {
            'serviceKey': '057a95bd3d088bd732e75b0406635329ffb6e29fe4704976439c238494daafba', 
            'item_name': kor_name, 
            'type': 'json'
        }
        
        try:
            res = requests.get(url, params=params, timeout=0.8)
            items = res.json().get('body', {}).get('items', [])
            
            if items:
                item = items[0]
                entp_name = item.get('ENTP_NAME', '정보 없음')
                
                # [상세주석] 요구사항 F1.2~F1.5에 따른 특징 데이터 시각화 강화
                html_content = f"""
                <h3 style="color:{title_color};">[{status_str}] {item.get('ITEM_NAME', kor_name)}</h3>
                <hr>
                <table border="0" cellpadding="8" style="width:100%; font-size:11pt; border-collapse: collapse;">
                    <tr bgcolor="#F2F4F4"><td><b>제조사</b></td><td>{entp_name}</td></tr>
                    <tr><td><b>모양(Shape)</b></td><td>{item.get('DRUG_SHAPE', '정보 없음')}</td></tr>
                    <tr bgcolor="#F2F4F4"><td><b>색상(Color)</b></td><td>{item.get('COLOR_CLASS1', '정보 없음')}</td></tr>
                    <tr><td><b>분할선(Line)</b></td><td>{item.get('LINE_FRONT', '없음')}</td></tr>
                    <tr bgcolor="#F2F4F4"><td><b>제형(Form)</b></td><td>{item.get('CHART', '정보 없음')}</td></tr>
                    <tr><td><b>식별등급</b></td><td>{conf:.2f} (AI 신뢰도)</td></tr>
                </table>
                <p style="color:gray; font-size:9pt; margin-top:10px;">* {item.get('ETC_OTC_CODE', '')} 의약품</p>
                """
                self.info_area.setHtml(html_content)

                # 불량 데이터만 서버(DB) 전송
                if is_defect:
                    payload = {
                        "line_id": "Line_A_Minki",
                        "pill_name": item.get('ITEM_NAME', kor_name), 
                        "company": entp_name, 
                        "status": status_str
                    }
                    resp = requests.post(self.server_url, json=payload, timeout=0.5)
                    if resp.status_code == 200:
                        self.log_area.append(f"⚠️ [불량 감지] {kor_name} -> DB 기록 완료")
                else:
                    self.log_area.append(f"✅ [정상 통과] {kor_name}")
            else:
                self.log_area.append(f"❓ [미등록] {kor_name} 정보를 API에서 찾을 수 없음")

        except Exception as e:
            self.log_area.append(f"⚠️ 시스템 오류: {e}")

    def closeEvent(self, event):
        self.det_thread.is_running = False
        self.det_thread.wait()
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PillDetectorGUI()
    ex.show()
    sys.exit(app.exec_())