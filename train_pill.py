from ultralytics import YOLO
import os

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # [수정 1] 실제 폴더명 확인 (Pill_Detection-4 인지 확인 필요)
    yaml_path = r'C:\Users\lms\OneDrive\문서\python\Pill_Detection\Multi-label-Classification\data.yaml'
    
    if not os.path.exists(yaml_path):
        print(f"❌ 설정 파일을 찾을 수 없습니다: {yaml_path}")
        return

    print(f"🚀 학습 시작! 설정 파일 주소: {yaml_path}")

    model = YOLO('yolov8n.pt')

    model.train(
        data=yaml_path,
        epochs=100,
        imgsz=640,
        project='C:/Pill_Train_Results', 
        name='pill_v2_augmented',
        patience=50,
        optimizer='AdamW',
        lr0=0.01,
        device=0  # GPU 사용
    )

if __name__ == '__main__':
    main()