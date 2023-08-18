import subprocess

def kill_jupyter_notebook(kill=True):
    ''' function that gets a list of active jupyter notebook(s) and the corresponding port(s) 
    to identify and terminate the PID(s) of jupyter notebook(s).
    '''
    # get stdout and split string into parts
    jpynb_list = subprocess.run(['jupyter', 'notebook', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('/')
    # get all parts with localhost entry
    localhost_entries = [entry for entry in jpynb_list if 'localhost:' in entry]
    # extract ports from localhost entries
    ports = [port.split(':')[1] for port in localhost_entries]
    
    # get PID for corresponding port
    for i, port in enumerate(ports): 
        # stdout from lsof command, split into parts
        PIDs_out = subprocess.run(['lsof', '-n', '-i4TCP:{}'.format(port)], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ')
        # find (indices + 1) of parts list with jupyter string in it
        PID_indices = [index + 1 for index, string in enumerate(PIDs_out) if 'jupyter' in string]
        jpyter_PID = list(set([PIDs_out[i] for i in PID_indices]))[0]
        print('Active jupyter notebook # {} at port {} with PID {}'.format(i, port, jpyter_PID))
        
        # kill corresponding PID
        if kill:
            subprocess.run(['kill', '-9', jpyter_PID], stdout=subprocess.PIPE).stdout.decode('utf-8')