# 📄 README.md (Portfolio Version)

## 💊 PillscanAI: Deep Learning Based Pill Recognition & Info System
> **딥러닝(YOLOv8)과 공공데이터 API를 활용한 지능형 알약 식별 및 실시간 관리 솔루션**

본 프로젝트는 제조 공정 및 스마트 팩토리 환경에서 약품의 오투약을 방지하고, 실시간 비전 검사를 통해 약품 정보를 즉각적으로 사용자에게 제공하는 것을 목표로 합니다.

---

## 🚀 Key Features (주요 기능)
* **실시간 객체 탐지 (Real-time Detection):** YOLOv8 모델을 사용하여 웹캠 환경에서 0.5초 이내의 빠른 알약 식별 수행.
* **데이터 증강 (Data Augmentation):** OpenCV를 활용한 명암 변화, 노이즈 추가 등으로 실제 공정 환경(조명 변화 등)에 강인한 모델 구현.
* **공공데이터 API 연동:** 식별된 알약의 특징을 바탕으로 식품의약품안전처 API와 통신하여 효능, 성분, 주의사항 등 상세 정보 출력.
* **불량 판정 및 서버 로깅:** 신뢰도(Confidence) 임계값 기반 정상/불량 판정 및 원격 서버 로그 전송 시스템 구축.
* **사용자 중심 GUI:** PySide6(Qt) 기반의 직관적인 대시보드와 실시간 시각화 인터페이스 제공.

---

## 🛠 Tech Stack (기술 스택)
* **Language:** Python 3.11
* **Deep Learning:** YOLOv8 (Ultralytics), OpenCV
* **UI Framework:** PySide6 (Qt for Python)
* **Database/API:** Public Data API (식품의약품안전처), REST API
* **Tools:** VSCode, Git, GitHub, Roboflow

---

## 🏗 System Architecture (시스템 구조)



1.  **Image Input:** OpenCV를 통한 실시간 프레임 캡처
2.  **Inference:** YOLOv8n 모델 기반 객체 탐지 및 클래스 분류
3.  **Data Processing:** 탐지된 클래스명을 기반으로 공공데이터 REST API 요청
4.  **Display:** PySide6 GUI 상에 AI 분석 정보 및 API 데이터 렌더링
5.  **Monitoring:** 불량 의심 시 Flask 서버로 실시간 로그 데이터 전송

---

## 📈 Development Results (개발 성과)
* **정확도:** 100 Epoch 학습 결과 **mAP50 0.995** 달성.
* **최적화:** 추론 속도 **약 60ms** 달성으로 초당 15프레임 이상의 실시간 검수 가능.
* **신뢰성:** 데이터 증강 기법을 통해 다양한 조명 조건에서도 85% 이상의 신뢰도 유지.

---

## 📺 Demo Screen (데모 화면)

| 실시간 탐지 및 정보 출력 | 불량 로그 및 상세 리포트 |
| :---: | :---: |
| ![Detection](https://via.placeholder.com/400x300?text=Detection+Screen) | ![Report](https://via.placeholder.com/400x300?text=Detail+Report+Screen) |
*(실제 작동 스크린샷 이미지로 교체하시면 좋습니다)*

---

## 👨‍💻 My Role (기여도 및 역할)
* **모델 설계 및 학습:** Roboflow를 통한 데이터셋 구축 및 YOLOv8 하이퍼파라미터 튜닝.
* **OpenCV 증강 스크립트 작성:** 모델 성능 향상을 위한 전처리 및 데이터 증강 파이프라인 개발.
* **GUI 어플리케이션 개발:** Threading 기법을 사용한 비동기 영상 처리 및 UI 응답성 확보.
* **API 통합:** RESTful API 통신 모듈 및 예외 처리 로직 구현.

---

## 🏁 Future Works (향후 발전 계획)
* **임베디드 최적화:** Jetson Nano 등 엣지 디바이스 배포를 위한 TensorRT 최적화.
* **다중 라벨 분류:** 모양, 색상, 분할선을 개별적으로 인식하는 Multi-label Classification 고도화.

---
