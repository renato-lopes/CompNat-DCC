
INSTANCES = ("ft06", "la01", "la29", "la40")
BEST_MAKESPAN = {"ft06": 55, "la01": 666, "la29": 1157, "la40": 1222}

def get_instances(filepath):
    instances_data = {}
    with open(filepath, "r") as f:
        lines = f.readlines()
    lines = [' '.join(x.replace('\n', '').strip().split()) for x in lines[51:]]
    i = 0
    while i < len(lines):
        if lines[i].startswith("instance"):
            cur_instance = lines[i].split(' ')[-1]
            i += 4
            njobs, nmachines = int(lines[i].split(' ')[0]), int(lines[i].split(' ')[1])
            if not cur_instance in INSTANCES:
                i += (njobs + 1)
            else:
                jobs_machines = []
                jobs_costs = []
                for j in range(njobs):
                    i += 1
                    machines = []
                    costs = []
                    operations = lines[i].split(' ')
                    for k in range(0, len(operations), 2):
                        machines.append(int(operations[k]))
                        costs.append(int(operations[k+1]))
                    jobs_machines.append(machines)
                    jobs_costs.append(costs)
                instances_data[cur_instance] = {
                    "njobs": njobs,
                    "nmachines": nmachines,
                    "jobs_machines": jobs_machines,
                    "jobs_costs": jobs_costs
                }
                i += 1
        else:
            i += 1
    return instances_data
