"""Script to create tsv files for Toloka tasks from direct links in imgbb"""
import numpy as np

# For how many tolokers should the tsv be conceived (every user gets a total of 30 images)
num_users = 5

# Read URLs
f = open('../toloka/bees/links_tasks13.txt', 'r')
links_t13 = np.asarray(f.readlines())
f.close()
f = open('../toloka/bees/links_task2_control.txt', 'r')
links_t2 = np.asarray(f.readlines())
f.close()

for i in range(num_users):
    # Shuffle links
    np.random.shuffle(links_t13)
    np.random.shuffle(links_t2)

print(links_t13)