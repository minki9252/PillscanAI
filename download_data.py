from roboflow import Roboflow

rf = Roboflow(api_key="gItv8tRfkEVeDw2BKs82")

project = rf.workspace("mk-h4sai").project("pill_detection-fc2or")

version = project.version(5)

dataset = version.download("yolov8")
                