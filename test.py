# test_image.py (새로 만들기)
from ultralytics import YOLO
import cv2

model = YOLO(r'C:\Users\lms\OneDrive\문서\python\Pill_Detection\runs\detect\train\weights\best.pt') # 본인 경로
# 학습에 사용했던 이미지 파일 경로를 넣으세요
img_path = r'C:\Users\lms\OneDrive\문서\python\Pill_Detection\Pill_Detection-1\train\images\KakaoTalk_20260406_202603215_02_jpg.rf.167893dbdb908a3b36492e9c3c7ff642.jpg' 

results = model(img_path, conf=0.1)
results[0].show() # 인식된 결과 창 띄우기