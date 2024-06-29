from ultralytics import YOLO
from Code import utils

# Load the YOLO model
def main():
    # Getting path to model and test images
    model_path = input("Enter model path: ")
    source_path = input("Enter path to test images: ")
    # Getting devices
    devices = utils.check_pytorch()
    # Loading Model and run prediction
    model=YOLO(model_path)
    model.predict(source=source_path, imgsz=864, device=devices, save=True, visualize=True, project="runs/")
