from ultralytics import YOLO
from Code import utils

def main():
    # Prepare for training
    config_path = "Code/config.yaml"
    config, train_images_path, valid_images_path, devices = utils.prepare_training(config_path)

    if config is None or train_images_path is None or valid_images_path is None or devices is None:
        print("Error preparing for training. Exiting...")
        return

    # Determine training mode (new or resume)
    action = utils.get_training_action()
    if action == 'n':
        # Get model and architecture from the user
        model_path, model_arch = utils.get_model()
        if model_arch:
            # Load a new model with a custom architecture
            model = YOLO(model_arch).load(model_path)
        else:
            # Load a new model with the default architecture
            model = YOLO(model_path)

        e_nums = utils.get_epochs()
        results = model.train(data=config_path, epochs=e_nums, device=devices, imgsz=864, project="runs/detect")

    elif action == 'r':
        # Resume training from last checkpoint
        checkpoint_path = utils.get_checkpoint_path()
        if checkpoint_path is None:
            return
        model = YOLO(checkpoint_path)  # Load model from checkpoint
        results = model.train(data=config_path, device=devices, imgsz=864, resume=True)
