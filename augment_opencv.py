import cv2
import albumentations as A
import os
import glob

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.7),
    A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.5),
    A.GaussNoise(p=0.3), # var_limit 에러 방지를 위해 기본값 사용
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

def augment_data(img_path, label_path, output_dir, count=3):
    image = cv2.imread(img_path)
    if image is None:
        # 한글 경로 및 특수문자 대응을 위해 시도
        import numpy as np
        image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            print(f"❌ 읽기 실패: {img_path}")
            return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 라벨 읽기 (파일이 없으면 빈 리스트로 처리)
    bboxes = []
    class_labels = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) == 5:
                class_labels.append(int(parts[0]))
                bboxes.append([float(x) for x in parts[1:]])

    base_name = os.path.basename(img_path).split('.')[0]

    for i in range(count):
        # 증강 실행
        augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)
        aug_img = augmented['image']
        aug_bboxes = augmented['bboxes']

        # 결과 저장
        img_name = f"{base_name}_aug_{i}.jpg"
        lbl_name = f"{base_name}_aug_{i}.txt"
        
        # 이미지 저장 (한글 경로 대응)
        res, img_encode = cv2.imencode('.jpg', cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))
        if res:
            img_encode.tofile(os.path.join(output_dir, img_name))

        # 라벨 저장 (내용이 없더라도 빈 파일 생성 - YOLO 규격)
        with open(os.path.join(output_dir, lbl_name), 'w') as f:
            for idx, bbox in enumerate(aug_bboxes):
                f.write(f"{class_labels[idx]} {' '.join(map(str, bbox))}\n")
    
    print(f"   ㄴ [완료] {base_name} -> {count}장 생성")

if __name__ == "__main__":

    img_dir = r'C:\Users\lms\OneDrive\문서\python\Pill_Detection\Multi-label-Classification-1\train\images'
    output_path = r'C:\Pill_Aug_Data' # OneDrive 밖 안전한 경로
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image_files = glob.glob(os.path.join(img_dir, "*.jpg"))
    print(f"🔍 찾은 원본 이미지 개수: {len(image_files)}개")

    for img_p in image_files:
        lbl_p = img_p.replace('images', 'labels').replace('.jpg', '.txt')
        augment_data(img_p, lbl_p, output_path, count=3)

    print("\n✅ 모든 작업이 종료되었습니다. C:\Pill_Aug_Data 폴더를 확인하세요.")