"""Script to identify unattentive/uninterested Tolokers that have submitted too many wrong answers"""
import pandas as pd

PATH_EXP = 'bees/Toloka_Bees_Control_100_all.csv'
stats = pd.read_csv(PATH_EXP)

outlier_ids = []
for worker_id, group in stats.groupby(by='ASSIGNMENTworker_id'):

    # Look at every user and divide their answers into Tasks 1-2-3
    t1, t2, t3 = group.iloc[:10, 1:4], group.iloc[10:20, 1:4], group.iloc[20:30, 1:4]
    num_corr_t1 = (t1['OUTPUTresult'] == t1['GOLDENresult']).sum()
    num_corr_t2 = (t2['OUTPUTresult'] == t2['GOLDENresult']).sum()
    num_corr_t3 = (t3['OUTPUTresult'] == t3['GOLDENresult']).sum()

    # A user will be removed, if they didn't get at least 4 correct answers per task
    if num_corr_t1 < 4 or num_corr_t2 < 4 or num_corr_t3 < 4:
        outlier_ids.append(worker_id)

print('Out of ' + str(stats['ASSIGNMENTworker_id'].nunique()) + ' users, ' + str(len(outlier_ids)) + ' will be removed.')

with open('Toloka_Bees_Control_100_outliers', 'w') as f:
    for id in outlier_ids:
        f.write(id + '\n')