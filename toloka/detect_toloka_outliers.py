"""Script to identify unattentive/uninterested Tolokers that have submitted too many wrong answers"""
import pandas as pd

exp_group = 'Examples_RepPoint' # Control, Control_Conf, Concepts_KNN, Concepts_TCAV, Examples_GradSim or Examples_RepPoint
PATH_EXP = 'fungi/experiment_200_1/Toloka_Fungi_' + exp_group + '_200_1_all.tsv'
stats = pd.read_csv(PATH_EXP, sep = '\t')

review = open('fungi/experiment_200_1/Toloka_Fungi_' + exp_group + '_200_1_reviews.tsv', 'w')
review.write('ASSIGNMENT:assignment_id\tACCEPT:verdict\tACCEPT:comment\n')

# Note: since the overlapping in Toloka is 1, every worker_id will be matched with a unique assignment_id
num_rejected = 0
min_answers  = 3 # min. number of correct answers in every task to pass
for assign_id, group in stats.groupby(by='ASSIGNMENT:assignment_id'):

    # Look at every user and divide their answers into Tasks 1-2-3
    t1, t2, t3 = group.iloc[:10,:], group.iloc[10:20,:], group.iloc[20:30,:]
    num_corr_t1 = (t1['OUTPUT:result'] == t1['GOLDEN:result']).sum()
    num_corr_t2 = (t2['OUTPUT:result'] == t2['GOLDEN:result']).sum()
    num_corr_t3 = (t3['OUTPUT:result'] == t3['GOLDEN:result']).sum()

    # A user will be rejected, if they didn't get at least 4 correct answers per task
    # Rejected users get a '-' as verdict and a comment. Accepted users get a '+'
    if num_corr_t1 < min_answers or num_corr_t2 < min_answers or num_corr_t3 < min_answers:
        review.write(assign_id + '\t' + '-' + '\t' +
                     'Sorry, you had too many wrong answers. We expect at least ' +  str(min_answers) +  ' correct answers out of 10 in each task.\n')
        num_rejected += 1
    else:
        review.write(assign_id + '\t' + '+' + '\t' + '\n')

print('Out of ' + str(stats['ASSIGNMENT:assignment_id'].nunique()) + ' users, ' + str(num_rejected) + ' will be rejected.')
review.close()