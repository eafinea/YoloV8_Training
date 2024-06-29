import json
import os

# Load the JSON file
with open('../HOIST/test.json') as f:
    data = json.load(f)

# Create the output directory if it doesn't exist
output_dir = 'yolov8_annotations'
os.makedirs(output_dir, exist_ok=True)

# Iterate over the videos
for video in data['videos']:
    video_id = video['id']
    file_names = video['file_names']

    # Find annotations for the current video_id
    annotations = [ann for ann in data['annotations'] if ann['video_id'] == video_id]

    # Process each frame in the video
    for frame_idx, file_name in enumerate(file_names):
        frame_annotations = []

        # Check each annotation if it has a bounding box for the current frame
        for ann in annotations:
            if frame_idx < len(ann['bboxes']):
                bbox = ann['bboxes'][frame_idx]

                # Skip if the bounding box is null
                if any(v is None for v in bbox):
                    continue

                category_id = ann['category_id'] - 1  # Adjust category ID to start from 0
                # Normalize the bounding box coordinates
                x_center = (bbox[0] + bbox[2] / 2) / video['width']
                y_center = (bbox[1] + bbox[3] / 2) / video['height']
                width = bbox[2] / video['width']
                height = bbox[3] / video['height']

                # Append the formatted annotation
                frame_annotations.append(f"{category_id} {x_center} {y_center} {width} {height}")

        # Generate the output file name
        base_name = os.path.basename(file_name)  # Extract the file name from the path
        base_name_no_ext = os.path.splitext(base_name)[0]  # Remove the file extension
        output_file_name = f"{base_name_no_ext}.txt"
        frame_file_name = os.path.join(output_dir, output_file_name)

        # Write the annotations to a text file
        if frame_annotations:
            with open(frame_file_name, 'w') as f:
                f.write('\n'.join(frame_annotations))
        else:
            # Create an empty file if there are no annotations for the frame
            open(frame_file_name, 'w').close()

print("Annotations have been successfully extracted.")
