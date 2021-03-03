import numpy as np

MAX_COST = 99999999

def get_max_time(jobs_costs):
    return np.sum(jobs_costs)

def get_available_jobs(njobs, nmachines, jobs_machines, ant_machines_status, ant_jobs_status):
    available_jobs = {x : [] for x in range(nmachines)} # Save available jobs to each machine
    for job in range(njobs):
        cur_operation = ant_jobs_status[job]
        if ant_machines_status[jobs_machines[job][cur_operation]] != 0 or cur_operation+1 >= len(jobs_machines[job]):
            continue # Current operation is not done or Job is already completed
        machine = jobs_machines[job][cur_operation+1]
        if ant_machines_status[machine] == 0: # If required machine is available
            available_jobs[machine].append(job)
    return available_jobs

def aco(njobs, nmachines, jobs_machines, jobs_costs, nants, aco_iterions, pheromones_max, pheromones_min, alpha, beta, evaporation_rate):
    max_time = get_max_time(jobs_costs)
    # Create pheromone matrix
    pheromones = np.ones((njobs, max_time)) * pheromones_max
    # Initialize best solution
    best_ant_path = None
    best_ant_cost = MAX_COST
    # Main loop
    history = {}
    for aco_i in range(aco_iterions):
        # Create ants representations
        ants_machines_status = np.zeros((nants, nmachines), dtype="int") # Save status of each machine, that is the amount of time until idle. If idle, value is 0
        ants_jobs_status = np.ones((nants, njobs), dtype="int") * -1 # Save the id of current operation on the job
        ants_results = np.zeros(nants, dtype="int") # Save the makespan found by each ant
        ants_paths = {x : [] for x in range(nants)}
        
        ### Build solutions ###
        for ant in range(nants):
            # Update each ant
            for t in range(max_time):
                # Update machines status
                ants_machines_status[ant] -= 1
                ants_machines_status[ant][ants_machines_status[ant] < 0] = 0 # Remove negative values
                # Check if all tasks are done
                if np.array_equal(ants_jobs_status[ant], np.array([len(x)-1 for x in jobs_machines])) and np.count_nonzero(ants_machines_status[ant]) == 0:
                    # Update ant makespan
                    ants_results[ant] = t
                    break
                # Select jobs to run in each machine
                available_jobs = get_available_jobs(njobs, nmachines, jobs_machines, ants_machines_status[ant], ants_jobs_status[ant])
                for m in range(nmachines):
                    if len(available_jobs[m]) > 0:
                        # Select jobs based on desirability and pheromones
                        probs = []
                        for j in available_jobs[m]:
                            j_operation = ants_jobs_status[ant][j]+1
                            desirability = 1.0/jobs_costs[j][j_operation] # Desirability is given by 1/cost of current operation
                            pheromone = pheromones[j][t] # Get pheromone associated with job at the current time
                            probs.append((pheromone**alpha) + (desirability**beta))
                        # Normalize probs into range [0, 1]
                        probs = np.array(probs)/np.sum(probs)
                        # Choose which job to run in this machine, based on probabilities
                        chosen_job = np.random.choice(available_jobs[m], p=probs)
                        # Execute job
                        ants_jobs_status[ant][chosen_job] += 1
                        ants_machines_status[ant][m] = jobs_costs[chosen_job][ants_jobs_status[ant][chosen_job]]
                        ants_paths[ant].append((t, m, chosen_job))
            # Update best solution
            if best_ant_path is None or ants_results[ant] < best_ant_cost:
                best_ant_path = ants_paths[ant]
                best_ant_cost = ants_results[ant]

        ### Update pheromones with Max-Min ###
        # Pheromone evaporation
        pheromones *= (1 - evaporation_rate)
        # Update pheromones with best result
        for time, machine, job in best_ant_path:
            pheromones[job][time] += (1.0 / best_ant_cost) # Update with the inverse of the cost of the best solution found so far
        # Check for limits
        np.clip(pheromones, pheromones_min, pheromones_max)

        history[aco_i] = {
            "ants_results": ants_results,
            "ants_paths": ants_paths
        }

        print(f"Iteration [{aco_i+1}/{aco_iterions}]: {ants_results}")
    
    return best_ant_cost, history
