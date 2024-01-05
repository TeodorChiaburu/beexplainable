"""Script to identify unattentive/uninterested Tolokers that have submitted too many wrong answers"""
import pandas as pd

PATH_EXP = 'bees/Toloka_Bees_Control_100_all.csv'
stats = pd.read_csv(PATH_EXP)

review = open('bees/Toloka_Bees_Control_100_reviews.tsv', 'w')
review.write('ASSIGNMENT:assignment_id\tACCEPT:verdict\tACCEPT:comment\n')

# Note: since the overlapping in Toloka is 1, every worker_id will be matched with a unique assignment_id
num_rejected = 0
for assign_id, group in stats.groupby(by='ASSIGNMENTassignment_id'):

    # Look at every user and divide their answers into Tasks 1-2-3
    t1, t2, t3 = group.iloc[:10, 1:4], group.iloc[10:20, 1:4], group.iloc[20:30, 1:4]
    num_corr_t1 = (t1['OUTPUTresult'] == t1['GOLDENresult']).sum()
    num_corr_t2 = (t2['OUTPUTresult'] == t2['GOLDENresult']).sum()
    num_corr_t3 = (t3['OUTPUTresult'] == t3['GOLDENresult']).sum()

    # A user will be rejected, if they didn't get at least 4 correct answers per task
    # Rejected users get a '-' as verdict and a comment. Accepted users get a '+'
    if num_corr_t1 < 4 or num_corr_t2 < 4 or num_corr_t3 < 4:
        review.write(assign_id + '\t' + '-' + '\t' +
                     'Sorry, you had too many wrong answers. We expect at least 4 correct answers out of 10 in each task.\n')
        num_rejected += 1
    else:
        review.write(assign_id + '\t' + '+' + '\t' + '\n')

print('Out of ' + str(stats['ASSIGNMENTassignment_id'].nunique()) + ' users, ' + str(num_rejected) + ' will be rejected.')
review.close()