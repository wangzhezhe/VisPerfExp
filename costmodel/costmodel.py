# Algorithm associted parameters
# seeds, image size, number of surface values

# Workflow design params
proximity=["inline","intransit"]
# the frequency that the ana visit the sim data
visit_freq=[1,2,3,4,5]
proc_num_sim=[1,2,3,4,5,6]
proc_num_ana=[1,2,3,4,5,6]
# queue length
# the length of the caching queue
# for the file io, we can assume the queue length is infinity
# for the streaming io such as SST, the code will block when it comes
# to the limitation of the queue.
queue_length=[1,2,3,4,5,6]
num_proc_per_node_sim=1
num_proc_per_node_ana=1

# Task related information 
# How exec time change with step is the baseline
# It contains the information of data size
# datasize_multiplier indicates the data size compared with the baseline
int step=100
def compute_sim_time(step, procs_num, datasize_multiplier):

def compute_ana_time(step, procs_num, datasize_multiplier, workload):

# for the inline case, the data transfer time can be assumed as 0
def compute_transfer_time(step, procs_num, datasize_multiplier):




def describe_distribution():
    step=100


def compute_plans():



if __name__ == "__main__":
    describe_distribution()
    compute_plans()