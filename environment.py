import numpy as np

from parameter import Parameter
from element import Machine, Job, Action

class Environment(object):
    def __init__(self, pa):
        # type: (Parameter) -> object
        self.pa = pa
        self.current_time = -1

        self.macs = []          # set of machines in the cluster
        self.mac_count = 0      # number of machines
        self.jobs = []          # set of jobs in the queue
        self.job_count = 0      # number of jobs
        self.running_jobs = []  # set of running jobs
        self.finished_jobs = [] # set of finished jobs

    def add_machine(self, mac):
        # type: (Machine) -> None
        self.macs.append(mac)
        self.mac_count += 1
        assert self.mac_count <= self.pa.mac_num


    def add_job(self, job):
        # type: (Job) -> None
        self.jobs.append(job)
        self.job_count += 1
        assert self.job_count <= self.pa.job_queue_num

    def pop_job(self, job_id):
        job_index = [x.id for x in self.jobs].index(job_id)
        self.jobs.pop(job_index)
        self.job_count -= 1

    def check_act(self, act): #act = [job_x, mac_y]  allocate job x to machine y
        # type: (Action) -> None
        job_index = [x.id for x in self.jobs].index(act.job_id)
        mac_index = [x.id for x in self.macs].index(act.mac_id)
        for i in xrange(self.pa.res_num):
            res_avail = (self.macs[mac_index].state[i] == 0)
            if res_avail.sum() < self.jobs[job_index].res_vec[i]:
                return False
        return True

    def take_act(self, act):
        # type: (Action) -> None
        job_index = [x.id for x in self.jobs].index(act.job_id)
        mac_index = [x.id for x in self.macs].index(act.mac_id)
        for i in xrange(self.pa.res_num):
            res_avail = (self.macs[mac_index].state[i] == 0)
            self.macs[mac_index].state[i, res_avail] = self.jobs[job_index].state[i, :res_avail.sum()]

        self.running_jobs.append(self.jobs[job_index])
        self.running_jobs[-1].start(self.current_time)



    def step(self): #act = [job_x, mac_y]  allocate job x to machine y
        # type: (Environment) -> None
        self.current_time += 1
        for mac in self.macs:
            mac.step()

        for job in self.running_jobs:
            job.step()
            # if job.status == "Finished":
            #     print "ID: ",               job.id
            #     print "Submission Time: ",  job.submission_time
            #     print "Starting Time",      job.starting_time
            #     print "Execution time: ",   job.execution_time
            #     print "======================================="
        self.finished_jobs.extend([job for job in self.running_jobs if job.status == "Finished"])
        self.running_jobs = [job for job in self.running_jobs if job.status != "Finished"]

    def status(self):
        # type: (Environment) -> str
        if self.running_jobs:
            return "Running"
        if self.jobs:
            return "Pending"
        return "Idle"

    def show(self):
        print "Time =",self.current_time, "  Pending =", self.job_count, "  Running =",len(self.running_jobs), "  Finished =",len(self.finished_jobs), "============================"
        # print "Machine: =========================================================="
        # for i in xrange(self.mac_count):
        #     self.macs[i].show()
        # print "Job: ==============================================================\n"
        # for i in xrange(self.job_count):
        #     self.jobs[i].show()


