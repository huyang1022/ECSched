import numpy as np
import matplotlib.pyplot as plt


def read_data(agent):
    ret_list= list()
    in_file = open("data/%s" % agent, "r")
    while True:
        line = in_file.readline()
        line = line.split()
        if not line: break
        ret_list.append(float(line[1]))

    return ret_list

def cmp_agent(agent1, agent2):
    l = list()
    sum_ratio = 0
    max_ratio = 0
    min_ratio = 1
    for i in xrange(len(agent1)):
        a = agent1[i]
        b = agent2[i]
        ratio = b * 1.0 / a - 1
        # ratio = 1 - a * 1.0 / b
        l.append(ratio)
        sum_ratio += ratio
        max_ratio = max(ratio, max_ratio)
        min_ratio = min(ratio, min_ratio)

    l.sort()
    print "Total: ", len(l)
    print "Reduction: ", len([x for x in l if x > 0])
    print "Increment: ", len([x for x in l if x < 0])
    print "Maximum Improve: ", max_ratio * 100
    print "Minimum Improve: ", min_ratio * 100
    print "Average Improve: ", sum_ratio / len(l) * 100
    return l

def plot_data(l):
    dx = 0.01
    sx = -1
    fx = 5
    i = 0
    y =[]
    while sx + dx * i < fx:
        y.append(len([x for x in l if sx + dx * i <= x < sx + dx * (i + 1)]))
        i += 1

    y = np.array(y)
    x = np.arange(sx,fx,dx)

    plt.plot(x, y.cumsum())


def run():

    agent_data = dict()
    agent = ["ecs_ml", "ecs_dp", "swarm", "k8s"]
    for i in agent:
        agent_data[i] = read_data(i)

    print "=============  ecs_dp vs. k8s  ================"
    l = cmp_agent(agent_data["ecs_dp"], agent_data["k8s"])
    plt.subplot(2, 1, 1)
    plot_data(l)
    print "=============  ecs_ml vs. k8s  ================"
    l = cmp_agent(agent_data["ecs_ml"], agent_data["k8s"])
    plot_data(l)
    plt.legend(["dp-k8s","ml-k8s"])

    print "=============  ecs_dp vs. swarm  ================"
    l = cmp_agent(agent_data["ecs_dp"], agent_data["swarm"])
    plt.subplot(2, 1, 2)
    plot_data(l)
    print "=============  ecs_ml vs. swarm  ================"
    l = cmp_agent(agent_data["ecs_ml"], agent_data["swarm"])
    plot_data(l)
    plt.legend(["dp-swarm","ml-swarm"])
    plt.show()


if __name__ == "__main__":
    run()