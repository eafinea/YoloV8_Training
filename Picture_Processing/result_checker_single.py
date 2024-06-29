import cv2
import os

def visualize_yolo_bbox(image_path, label_dir, color=(0, 255, 0), thickness=2):
    """
    Visualize bounding boxes in an image, given YOLO-format annotations.

    Parameters:
    - image_path: Path to the image file.
    - label_dir: Directory containing the YOLO-format label files.
    - color: Bounding box color.
    - thickness: Bounding box line thickness.
    """

    # Construct the label file path
    image_name = os.path.basename(image_path)
    label_file_name = os.path.splitext(image_name)[0] + '.txt'
    label_file_path = os.path.join(label_dir, label_file_name)

    # Load YOLO annotations if label file exists
    yolo_annotations = []
    if os.path.exists(label_file_path):
        with open(label_file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                yolo_annotations.append((class_id, x_center, y_center, width, height))

    # Load image
    image = cv2.imread(image_path)
    image_height, image_width = image.shape[:2]

    # Draw each bounding box
    for class_id, x_center, y_center, width, height in yolo_annotations:
        # Convert YOLO bbox coordinates to standard format
        x_center_abs = x_center * image_width
        y_center_abs = y_center * image_height
        width_abs = width * image_width
        height_abs = height * image_height
        x_min = int(x_center_abs - (width_abs / 2))
        y_min = int(y_center_abs - (height_abs / 2))
        x_max = int(x_center_abs + (width_abs / 2))
        y_max = int(y_center_abs + (height_abs / 2))

        # Draw bbox
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)

    # Show image
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = input('Image Path: ')
label_dir = input('Label Path: ')
visualize_yolo_bbox(image_path, label_dir)
