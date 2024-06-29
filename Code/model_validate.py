from ultralytics import YOLO
from Code import utils

def main():
    # Getting path to dataset YAML file for location, and getting the model
    config_path = "Code/config_test.yaml"
    config, train_images_path, valid_images_path, devices = utils.prepare_training(config_path)
    model_path = input("Enter model file path: ")

    # Loading the model for validation
    model = YOLO(model_path)
    metrics = model.val(data=config_path, imgsz=864, device=devices, save_json=True, project="runs/detect")
    # Printing additional metrics to check for more details
    metrics.box.map  # map50-95
    metrics.box.map50  # map50
    metrics.box.map75  # map75
    metrics.box.maps  # a list contains map50-95 of each category



