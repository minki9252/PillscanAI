from ultralytics import YOLO

import os

def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    yaml_path = os.path.join(current_dir, "Pill_Detection", "data.yaml")

    print(f"🚀 학습 시작! 설정 파일 주소: {yaml_path}")

    model = YOLO('yolov8n.pt')

    model.train(
        data=yaml_path,
        epochs=100,
        imgsz=640,
        patience=50,
        optimizer='AdamW',
        lr0=0.01,
        label_smoothing=0.1,
        close_mosaic=30,
        augment=True,
        cls=2.0,
        box=7.5,
        device=0  # GPU가 있다면 반드시 추가!
    )

if __name__ == '__main__':
    main()