"""Script to replace non_consecutive file ids with consecutive ones"""

with open('./5_species/image_class_labels_cleaned.txt', 'r') as file:
    data = file.readlines()

for i, line in enumerate(data):
    split_line = line.split(' ')
    data[i] = str(i+1) + ' ' + split_line[1]

with open('./5_species/image_class_labels_cleaned.txt', 'w') as file:
    file.writelines( data )