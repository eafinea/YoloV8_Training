import os
import yaml

# Function to check if a directory exists
def check_directory(path):
    if not os.path.isdir(path):
        print(f"Directory not found: {path}")
        return False
    return True

# Check for PyTorch installation and whether GPU is available
def check_pytorch():
    try:
        import torch
        available_devices = []
        if torch.cuda.is_available():
            available_devices.extend([f"cuda:{i}" for i in range(torch.cuda.device_count())])
        else:
            print("No CUDA devices available. Defaulting to CPU.")

        print("Available GPU(s):")
        for i, device in enumerate(available_devices):
            print(f"{i}: {device}")

        while True:
            choices = input(
                "Select GPU number(s) to use for training (e.g., 0 for singular GPU, or 1,2 for multiple GPUs, leave blank for CPU): ")
            try:
                if choices.strip() == "":
                    return "cpu"

                choice_indices = [int(choice) for choice in choices.split(',')]
                if all(0 <= choice < len(available_devices) for choice in choice_indices):
                    selected_devices = ",".join([available_devices[choice] for choice in choice_indices])
                    print(f"Selected devices: {selected_devices}")
                    return selected_devices
                else:
                    print("Invalid choice. Please enter numbers corresponding to the available devices.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")

    except ImportError:
        print("PyTorch is not installed. Please install it to proceed.")
        return None

# Load and parse config.yaml
def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Validate dataset directories
def validate_directories(config):
    try:
        base_path = config['path']
        train_images_path = os.path.join(base_path, config['train'])
        valid_images_path = os.path.join(base_path, config['val'])
        train_labels_path = train_images_path.replace('images', 'labels')
        valid_labels_path = valid_images_path.replace('images', 'labels')

        if not (check_directory(train_images_path) and
                check_directory(valid_images_path) and
                check_directory(train_labels_path) and
                check_directory(valid_labels_path)):
            print("Error: One or more required directories are missing.")
            return None, None  # Return None if directories are missing
        return train_images_path, valid_images_path  # Return paths
    except KeyError as e:
        print(f"Error: Missing key in config.yaml: {e}")
        return None, None  # Return None if key is missing

# Confirming training and validation dataset path is correct
def confirm_paths(train_images_path, valid_images_path):
    print("Please confirm the following dataset locations:")
    print(f"Training dataset location: {train_images_path}")
    print(f"Validation dataset location: {valid_images_path}")
    while True:
        confirmation = input("Are these paths correct? (yes/no): ").lower()
        if confirmation == 'yes' or confirmation == 'y':
            return True
        elif confirmation == 'no' or confirmation == 'n':
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Getting user choice for training
def get_training_action():
    while True:
        action = input("Do you want to (n)ew train a model or (r)esume training? (n/r): ").lower()
        if action in ['n', 'r']:
            return action
        else:
            print("Invalid input. Please enter 'n' for new training or 'r' for resuming training.")

# Getting the model
def get_model():
    model_path = input(
        "Please enter the path to your desired model checkpoint (or press Enter to use the default 'yolov8n.yaml'): ")
    if model_path == '':
        model_path = "yolov8n.yaml"

    while True:
        option = input("Do you want to use a different model architecture? (yes/no): ").lower()
        if option in ['yes', 'y']:
            model_arch = input("Please enter the path to your desired model architecture YAML file: ")
            if not os.path.isfile(model_arch):
                print("Model architecture file not found. Please try again.")
                continue
            return model_arch, model_path
        elif option in ['no', 'n']:
            return model_path, None
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Getting Checkpoint for resuming training
def get_checkpoint_path():
    checkpoint_path = input("Enter the path to the last checkpoint: ")
    if not os.path.isfile(checkpoint_path):
        print("Checkpoint file not found. Exiting...")
        return None
    return checkpoint_path

# Getting epochs to train
def get_epochs(default=100):
    while True:
        try:
            epochs_input = input(f"Number of epochs (default {default}): ")
            if epochs_input == '':
                return default
            epochs = int(epochs_input)
            if epochs <= 0:
                print("Number of epochs must be greater than 0. Using default value.")
                return default
            return epochs
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Checking for location validation, get devices
def prepare_training(config_path):
    # Load and parse config.yaml
    config = load_config(config_path)

    # Validate dataset directories
    train_images_path, valid_images_path = validate_directories(config)
    if train_images_path is None or valid_images_path is None:
        print("Error validating directories. Exiting...")
        return None, None, None

    # Print full paths and confirm
    if not confirm_paths(train_images_path, valid_images_path):
        print("User canceled. Exiting...")
        return None, None, None

    # Check PyTorch and get device
    devices = check_pytorch()
    if devices is None:
        return None, None, None

    print("All required directories found. Proceeding with training...")

    return config, train_images_path, valid_images_path, devices