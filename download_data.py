from roboflow import Roboflow
rf = Roboflow(api_key="gItv8tRfkEVeDw2BKs82")
project = rf.workspace("mk-h4sai").project("multi-label-classification-w3ocq")
version = project.version(1)
dataset = version.download("yolov8")
                