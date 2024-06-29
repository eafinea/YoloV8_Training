import cv2
import os

def visualize_yolo_bbox(image_path, yolo_annotations, color=(0, 255, 0), thickness=2):
    """
    Visualize bounding boxes in an image, given YOLO-format annotations.

    Parameters:
    - image_path: Path to the image file.
    - yolo_annotations: List of tuples, each representing a bounding box in YOLO format.
      Each tuple is (class_id, x_center, y_center, width, height), where each value is relative to the image dimensions.
    - color: Bounding box color.
    - thickness: Bounding box line thickness.
    """

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

    return image

def process_images(source_image_dir, label_dir, output_image_dir):
    """
    Process all images in the source directory, draw bounding boxes, and save to the output directory.

    Parameters:
    - source_image_dir: Directory containing the source images.
    - label_dir: Directory containing the YOLO-format label files.
    - output_image_dir: Directory to save the processed images.
    """

    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)

    for image_name in os.listdir(source_image_dir):
        if image_name.endswith(('.jpg', '.jpeg', '.png')):  # Adjust the extensions based on your images
            image_path = os.path.join(source_image_dir, image_name)
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

            # Visualize bounding boxes
            processed_image = visualize_yolo_bbox(image_path, yolo_annotations)

            # Save the processed image
            output_image_path = os.path.join(output_image_dir, image_name)
            cv2.imwrite(output_image_path, processed_image)
            print(f"Processed and saved: {output_image_path}")

source_image_dir = input('Enter source image directory: ')
label_dir = input('Enter YOLO-format label directory: ')
output_image_dir = input("Enter path to save the processed images: ")
process_images(source_image_dir, label_dir, output_image_dir)
