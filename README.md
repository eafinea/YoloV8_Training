# About
A program to train/validate/test a YOLOV8 model
- All codes are in Python unless stated otherwise
- Also included virtual environment used to run, and a requirements.txt to install necessary libraries
- Run with `ultralytics` version 8.2.31 and `Pytorch` version 2.3.1 - CUDA 11.8
- Made for `YOLOV8 Detection` task
- Click [HERE](https://drive.google.com/drive/folders/1s-enTyxErsBaa1rL-_wFNld7F0JyeuBO?usp=sharing) to check for prediction output

# Folder information
- `Code`: A folder to store the codes used in the program
- `Data`: A folder containing dataset
- `runs`: A folder containing results after running the program

# How to use

## 0. Go to `config.yaml` or `config_test.yaml` and change the `path` parameter to the absolute path to the dataset folder (must be absolute or there will be errors). Import `requirements.txt` for libraries used.

## 1. Run `main.py` and choose to train/validate/predict.

## 2. For each mode: All modes will ask if the user wants to run using CPU or GPU(s).

### 2.1. Train Model
- Can either train a new model (with default/custom model architecture) or resume training from the last checkpoint.
- Result is saved in `runs/detect/train`.

### 2.2. Validation
- Put in the path to the desired model for validation and run.
- Result is saved in `runs/detect/val`, and includes a few metrics for further analysis.

### 2.3. Predict
- Put the path to the desired model and the path to the test images folder/file.
- Result is saved in `runs/predict`, including a heatmap for detected features.

### Dataset used
This project uses the [Hoist](https://supreethn.github.io/research/hoistformer/index.html) dataset.

### MISCELLANOUS
- `Picture_Processing`: Used for collecting all images from the dataset to one appropriate folder, and for extracting & converting labels to YOLOV8 accepted format
    + `Picture_Extractor.exe`: Image extractor, code in C#
    + `Annotation_Extractor.py`: Label extractor, made to accomodate the label JSON file included in the dataset
    + `result_checker_all.py` & `result_checker_single.py`: For checking if labels are correctly extracted
- `HOIST`: Folder contain the original dataset
