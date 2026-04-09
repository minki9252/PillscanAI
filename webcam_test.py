import cv2
from ultralytics import YOLO

# 1. 모델 로드 (본인의 best.pt 경로로 수정)
model = YOLO(r'C:\Users\lms\OneDrive\문서\python\Pill_Detection\runs\detect\pill_final_model8\weights\best.pt')

# 2. 웹캠 설정 (DSHOW 모드)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("🚀 실시간 인식 모드 시작! 종료하려면 'q'를 누르세요.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # stream=True를 사용하면 for 문으로 결과를 꺼내야 합니다.
    # imgsz를 320으로 낮추면 저화질 웹캠에서도 특징을 더 잘 잡을 수 있습니다.
    results = model(frame, conf=0.5, imgsz=640, stream=True)

    for r in results:
        # 결과 화면 그리기
        annotated_frame = r.plot()
        
        # 화면 표시
        cv2.imshow("Pill Detection Test", annotated_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()