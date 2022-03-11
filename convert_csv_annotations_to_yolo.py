
import os
import numpy as np
from csv import reader


directory = r'D:\Dataset\Automatically_annotated_file_list\Automatically_annotated_file_list\automatically_annotated.csv'                     # Set path for where to find annotations
new_anno_path = r'D:\Dataset\Automatically_annotated_yolo'                  # Where to put new annotation files

#f = open(directory)

# open file in read mode
with open(directory, 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        #print(row[0], row[6])

        subDirectory_filepath = row[0]
        if row[0] is not 'subDirectory_filepath':
            data = subDirectory_filepath.split('/')
            print(data[1])

        # Face location
        #x_center = 0
        #y_center = 0
        #width = 0
        #height = 0

        #

        # Create a new file and write to it
        #f = open(f"{new_anno_path}\{image}.txt", "w")
        #f.write(f"{data[1]} {x_center} {y_center} {width} {height}")
        #f.close()

        #print(row)