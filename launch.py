from environment import Environment
from parameter import Parameter
from mac_generator import MacGenerator
from job_generator import JobGenerator
from element import Machine, Job
import pack_agent
import ecs_agent
import k8s_agent
import ecs_ml_agent
import ecs_dp_agent
import swarm_agent
import plot

def run(agent):

    Machine.reset()
    Job.reset()

    pa = Parameter()
    env = Environment(pa)

    mac_gen = MacGenerator(pa)
    job_gen = JobGenerator(pa)


    for i in mac_gen.mac_sequence:
        env.add_machine(i)

    job_idx = 0
    current_time = 0


    while True:

        env.show()
        env.step()

        while job_gen.job_sequence[job_idx] is not None:
            if (job_gen.job_sequence[job_idx].submission_time == current_time):   #  add job to environment
                env.add_job(job_gen.job_sequence[job_idx])
                job_idx += 1
            else:
                break

        if agent == "ecs":
            ecs_agent.schedule(env)
        elif agent =="k8s":
            k8s_agent.schedule(env)
        elif agent == "pack":
            pack_agent.schedule(env)
        elif agent == "ecs_dp":
            ecs_dp_agent.schedule(env)
        elif agent == "ecs_ml":
            ecs_ml_agent.schedule(env)
        elif agent == "swarm":
            swarm_agent.schedule(env)

        if job_gen.job_sequence[job_idx] is None:
            if env.status() == "Idle": # finish all jobs
                break
        current_time += 1


    env.finished_jobs.sort(key = lambda x: x.id)
    file_path = "data/%s" % (agent)
    out_file = open(file_path, "w")
    for i in env.finished_jobs:
        out_file.write("%d %d \n" % (i.id, i.starting_time - i.submission_time + i.execution_time))




def main():
    run("ecs_dp")
    run("ecs_ml")
    run("k8s")
    run("swarm")
    plot.run()
    # run("pack")

if __name__ == "__main__":
    main()