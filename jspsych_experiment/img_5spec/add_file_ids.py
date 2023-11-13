"""Script to add file ids to a file containing image paths only"""

with open('pool_tasks123.txt', 'r') as file:
    data = file.readlines()

for i, line in enumerate(data):
    data[i] = str(i+1) + ' ' + line

with open('pool_tasks123.txt', 'w') as file:
    file.writelines( data )