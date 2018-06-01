
class Parameter(object):
    def __init__(self):

        self.exp_len = 10000                                # maximum duration of one experiment


        self.res_num = 2                                # number of resources in the cluster
        self.res_slot = 100                            # maximum number of resource slots

        self.mac_num = 50                               # number of machines in the cluster
        self.mac_max_slot = self.res_slot               # maximum number of resource slots of machine


        self.job_queue_num = 100000                        # maximum number of jobs in the queue
        self.job_process_num = 100                       # maximum number of jobs that can be processed at one time
        self.job_max_len = 675                         # maximum duration of jobs
        self.job_max_slot = self.res_slot               # maximum number of requested resource
        self.job_interval = 3                           # average inter-arrival time
        self.job_seed = 77                              # random seed for job generating


        # usage: job_max_len * 4 / 45 / interval / mac_num