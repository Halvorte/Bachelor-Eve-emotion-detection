
import os
import numpy as np
from csv import reader


directory = r'D:\Dataset\Manually_Annotated_file_lists\validation.csv'                     # Set path for where to find annotations
new_anno_path = r'D:\Dataset\Manually_annotated_yolo\validation'                  # Where to put new annotation files

#f = open(directory)

# open file in read mode
with open(directory, 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object

    # Remove the first line of the csv file
    count = 0
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        #print(row[0], row[6])
        if count == 0:
            count += 1
        else:
            subDirectory_filepath = row[0]
            data = subDirectory_filepath.split('/')
            #print(data[1])

            # Face location
            x_top_left = row[1]
            y_top_left = row[2]
            width = row[3]
            height = row[4]

            x_center = (int(width)//2) + int(x_top_left)
            y_center = (int(height)//2) + int(y_top_left)
            expression = row[6]

            image = data[1].strip('.jpg').strip('.JPG').strip('.pn').strip('.jpe')

            # Drop the images with expression none, uncertain and non-face
            if (expression == '8') or (expression == '9') or (expression == '10'):
                print('8, 9 or 10')
            else:
                # Create a new file and write to it
                f = open(f"{new_anno_path}\{image}.txt", "w")
                f.write(f"{expression} {x_center} {y_center} {width} {height}")
                f.close()

                #print(f'{image} {x_center} {y_center} {width} {height} {expression}')