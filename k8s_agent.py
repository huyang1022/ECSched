from environment import Environment
from element import Action

def schedule(env):
    # type: (Environment) -> object

    job_num = min(env.job_count, env.pa.job_process_num)
    act_list = []


    for i in xrange(job_num):
        max_score = 0
        act = None
        for j in xrange(env.mac_count):
            res_frac = []
            score = 0
            for k in xrange(env.pa.res_num):
                res_avail = (env.macs[j].state[k] == 0)
                if res_avail.sum() < env.jobs[i].res_vec[k]:
                    break
                res_frac.append(env.jobs[i].res_vec[k] * 1.0 / res_avail.sum())

            if len(res_frac) == env.pa.res_num:
                for a in xrange(env.pa.res_num):
                    score += 1 - res_frac[a]
                    for b in xrange(a + 1, env.pa.res_num):
                        score += 2 * (1 - abs(res_frac[a] - res_frac[b]))

            if score > max_score:
                max_score = score
                act = Action(env.jobs[i].id, env.macs[j].id)

        if act is not None:
            act_list.append(act)
            act.show()
            env.take_act(act)
            break

    for i in act_list:
        env.pop_job(i.job_id)

    return act_list
