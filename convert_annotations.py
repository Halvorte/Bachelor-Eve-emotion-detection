# Convert annotations from AffectNet dataset to YOLO-labels
# Paper for dataset: https://arxiv.org/abs/1708.03985
# Website for dataset: http://mohammadmahoor.com/affectnet/

# YOLO format
#bilder 224x224, 15% boundry expansion of detected face
# classe nummer, x-center, y-center, width, height
# center is always same center because images are same size and only face, 112px = 0.5
# Width and height => 100% - 15% = 85% of width and height
#
# class, 0.5, 0.5, 0.85, 0.85


import os
import numpy as np

directory = r'E:\Dataset-emotion\train_set\annotations'                         # Set path for where to find annotations
new_anno_path = r'E:\Dataset-emotion\train_set\annotations\YOLO-annotations'    # Where to put new annotation files

for filename in os.listdir(directory):
    if filename.endswith("_exp.npy"):
        f = os.path.join(directory, filename)
        data = np.load(f)

        # Get image number.
        image = filename.replace('_exp.npy', '')
        #print(f'{new_anno_path}\{image}.txt')

        # Create a new file and write to it
        f = open(f"{new_anno_path}\{image}.txt", "w")
        f.write(f"{data} 0.5 0.5 0.85 0.85")
        f.close()

