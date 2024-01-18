"""Script to create tsv files for Toloka tasks from direct links in imgbb"""
import numpy as np
import glob

# Experiment group name depends on what images are shown in Task 2
groups = ['control', 'concepts', 'examples']

# For how many tolokers should the tsv be conceived? Every user gets a total of 30 images.
num_users = 5

# Get list of all img names in the sampling pool for Toloka
task123_paths = glob.glob('./fungi/images/task13_imgs/*.JPG')
task123_ids = np.asarray([img.split('/')[-1].split('_')[0] for img in task123_paths]) # get image ids only i.e. 2237915051-225385

# Read URLs
f = open('fungi/images/links_tasks13.txt', 'r')
links_t13 = np.asarray(f.readlines())
f.close()
links_t2, tsv_files = {}, {}
for group in groups:
    f = open('fungi/images/links_task2_' + group + '.txt', 'r')
    links_t2[group] = np.asarray(f.readlines())
    f.close()
    tsv_files[group] = open('fungi/experiment_100_2/fungi_tasks123_' + group + '_100.tsv', 'w')
    tsv_files[group].write("INPUT:image\tGOLDEN:result\n")

# Get indexes of hard and easy samples
hard = [i for i in range(len(task123_paths)) if 'hard' in task123_paths[i]]
easy = [i for i in range(len(task123_paths)) if 'easy' in task123_paths[i]]

for i in range(num_users):
    # Shuffle link ids
    np.random.shuffle(hard)
    np.random.shuffle(easy)

    # Compile tasks 1, 2 and 3
    task1 = np.concatenate((task123_ids[hard[:5]],    task123_ids[easy[:5]]))
    task2 = np.concatenate((task123_ids[hard[5:10]],  task123_ids[easy[5:10]]))
    task3 = np.concatenate((task123_ids[hard[10:15]], task123_ids[easy[10:15]]))

    # Reshuffle tasks for every group (same images, different order)
    # Compile lists of ibb links according to group
    # Write urls in tsv (every 30 images will be assigned to one user in Toloka)
    for group in groups:
        np.random.shuffle(task1)
        np.random.shuffle(task2)
        np.random.shuffle(task3)
        tasks_123 = np.concatenate((task1, task2, task3))

        for i, id in enumerate(tasks_123):
            if 9 < i < 20: # images for task 2
                # Get ibb link for images with AI hint
                for link in links_t2[group]:
                    if id in link:
                        tsv_files[group].write(link.strip() + '\t' + link.split('-')[2] + '\n')
                        break
            else: # images in task 1 and 3
                # Get ibb link for images without AI hint
                for link in links_t13:
                    if id in link:
                        tsv_files[group].write(link.strip() + '\t' + link.split('-')[2] + '\n')
                        break

for group in groups:
    tsv_files[group].close()