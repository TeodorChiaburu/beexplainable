"""Script to create tsv files for Toloka tasks from direct links in imgbb"""
import numpy as np

# Experiment group name depends on what images are shown in Task 2 (control, concepts, examples)
group = 'control'

# For how many tolokers should the tsv be conceived? Every user gets a total of 30 images.
num_users = 100

# Read URLs
f = open('../toloka/bees/links_tasks13.txt', 'r')
links_t13 = f.readlines()
f.close()
f = open('../toloka/bees/links_task2_' + group + '.txt', 'r')
links_t2 = f.readlines()
f.close()

# Get indexes of hard and easy samples
hard_t13, easy_t13 = [link.strip() for link in links_t13 if 'hard' in link], [link.strip() for link in links_t13 if 'easy' in link]
hard_t2,  easy_t2  = [link.strip() for link in links_t2  if 'hard' in link], [link.strip() for link in links_t2  if 'easy' in link]

# Open tsv file
tsv_file = open('../toloka/bees/bees_tasks123_' + group + '_100.tsv', 'a')

for i in range(num_users):
    # Shuffle links
    np.random.shuffle(hard_t13)
    np.random.shuffle(easy_t13)
    np.random.shuffle(hard_t2)
    np.random.shuffle(easy_t2)

    # Compile tasks
    task1 = hard_t13[:5] + easy_t13[:5]
    np.random.shuffle(task1)
    task2 = hard_t2[:5] + easy_t2[:5]
    np.random.shuffle(task2)
    task3 = hard_t13[5:10] + easy_t13[5:10]
    np.random.shuffle(task3)
    tasks_123 = task1 + task2 + task3

    # Write urls in tsv (every 30 images will be assigned to one user in Toloka)
    for link in tasks_123:
        tsv_file.write('\n' + link + '\t' + link.split('-')[1])

tsv_file.close()