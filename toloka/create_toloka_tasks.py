"""Script to create tsv files for Toloka tasks from direct links in imgbb"""
import numpy as np

# Experiment group name depends on what images are shown in Task 2
groups = ['control', 'concepts', 'examples']

# For how many tolokers should the tsv be conceived? Every user gets a total of 30 images.
num_users = 100

# Read URLs
f = open('bees/images/links_tasks13.txt', 'r')
links_t13 = np.asarray(f.readlines())
f.close()
links_t2, tsv_files = {}, {}
for group in groups:
    f = open('bees/images/links_task2_' + group + '.txt', 'r')
    links_t2[group] = np.asarray(f.readlines())
    f.close()
    tsv_files[group] = open('bees/experiment_100_2/bees_tasks123_' + group + '_100.tsv', 'w')
    tsv_files[group].write("INPUT:image\tGOLDEN:result\n")

# Get indexes of hard and easy samples
hard_t13, easy_t13 = [i for i in range(len(links_t13)) if 'hard' in links_t13[i]], \
                     [i for i in range(len(links_t13)) if 'easy' in links_t13[i]]
hard_t2,  easy_t2  = [i for i in range(len(links_t2['control'])) if 'hard' in links_t2['control'][i]], \
                     [i for i in range(len(links_t2['control'])) if 'easy' in links_t2['control'][i]]

for i in range(num_users):
    # Shuffle link ids
    np.random.shuffle(hard_t13)
    np.random.shuffle(easy_t13)
    np.random.shuffle(hard_t2)
    np.random.shuffle(easy_t2)

    # Compile tasks 1 and 3
    task1 = np.concatenate((links_t13[hard_t13[:5]],   links_t13[easy_t13[:5]]))
    task3 = np.concatenate((links_t13[hard_t13[5:10]], links_t13[easy_t13[5:10]]))

    # Reshuffle tasks 1 + 3 for every group (same images, different order)
    # Compile task 2 for every group
    # Write urls in tsv (every 30 images will be assigned to one user in Toloka)
    for group in groups:
        np.random.shuffle(task1)
        np.random.shuffle(task3)
        task2 = np.concatenate((links_t2[group][hard_t2[:5]], links_t2[group][easy_t2[:5]]))
        np.random.shuffle(task2)
        tasks_123 = np.concatenate((task1, task2, task3))
        for link in tasks_123:
            tsv_files[group].write(link.strip() + '\t' + link.split('-')[1] + '\n')

for group in groups:
    tsv_files[group].close()