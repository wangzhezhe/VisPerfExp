import queue
import threading
from threading import Thread
import time

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
# for the streaming io such as SST, the sim will block when it comes
# to the limitation of the queue, it is the producer-consumer pattern
queue_length=[1,2,3,4,5,6]
num_proc_per_node_sim=1
num_proc_per_node_ana=1

# Task related information 
# For the fixed visualization parameters, how exec time change with step can be the baseline
# It contains the information of data size
# datasize_multiplier indicates the data size compared with the baseline
total_step=5

def compute_sim_time(step, procs_num, datasize_multiplier):
    return 5

def compute_ana_time(step, procs_num, datasize_multiplier, workload_multiplier):
    return 5
# for the inline case, the data transfer time can be assumed as 0
def compute_transfer_time(step, procs_num, datasize_multiplier):
    return 1

# TODO, more detailed model can get the performance model based on workload and datasize direactly.
# instead of using the change of the step as the baseline
# which means we can also vary the workload parameter 
# or have different multiplier, such as data size multiplier, seeds number multiplier, etc 
# from small scale to large scale

def describe_distribution():
    print("todo describe_distribution")


def compute_plans():
    print("todo compute_plans")


# time division
def compute_inline():
    exec_time_inline=0
    procs_num=1
    datasize_multiplier=1
    workload_multiplier=1
    frequency=1
    
    step = 1
    # using total_step+1 to check the last step
    while step < total_step+1:
        exec_time_inline+=compute_sim_time(step,procs_num,1)
        if step%frequency==0:
            exec_time_inline+=compute_ana_time(step,procs_num,1,1)
        step+=1

    print("compute_inline exect time ", exec_time_inline)


class DataNode:
     def __init__(self, step, data_generated_time):
         self.step = step
         self.data_generated_time = data_generated_time

# refer to https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# space division
need_to_process_len = 0
queue_len_limit=1
procs_num=1
frequency_transfer=1
frequency_anavisit=1

datasize_multiplier=1
workload_multiplier=1


exec_simtime_intran= 0
exec_anatime_intran= 0

def compute_intran():

    temp_ana_start=0

    lock = threading.Lock()
    
    data_staging_queue = queue.Queue()

    #sim_exec = ThreadWithReturnValue(target=doing_sim_computation, args=(data_staging_queue,lock))
    sim_exec = threading.Thread(target=doing_sim_computation, args=(data_staging_queue,lock))
    sim_exec.start()
    #ana_exec = ThreadWithReturnValue(target=doing_ana_computation, args=(data_staging_queue,lock))
    ana_exec = threading.Thread(target=doing_ana_computation, args=(data_staging_queue,lock))
    ana_exec.start()
    
    ana_exec.join()
    sim_exec.join()


    print("exec_simtime_intran is ", exec_simtime_intran)
    print("exec_anatime_intran is ", exec_anatime_intran)
    sim_wait = exec_simtime_intran-exec_anatime_intran
    if exec_simtime_intran<exec_anatime_intran:
        sim_wait=0
    print("sim wait time at last step is ", exec_anatime_intran-exec_simtime_intran)

def doing_sim_computation(data_staging_queue,lock):
    # start from the first step
    step_sim = 1
    temp_sim_start=0
    global need_to_process_len
    global queue_len_limit
    global exec_anatime_intran
    global exec_simtime_intran
    sim_waited = False
    # the step here is the simulation iteration step
    # visit frequency might be different with the data transfer frequency
    while step_sim < total_step+1:
        # for sim
        # there are two decisions
        # 1> do the next step sim computation (look at transfering the data to ana program)
        # 2> wait the ana program
        
        # if this is the first step after the sim wait
        # we need to adjust the start time
        if sim_waited==True:
            # only update the sim start when it waited previously

            # also need to add previous data transfer time
            # Maybe also need to consider the time to get the data for the ana
            # this transfer time happens only when the block is resoved by ana
            temp_sim_start=temp_sim_start+compute_transfer_time(step_sim,procs_num,datasize_multiplier)
            temp_sim_start=max(temp_sim_start,exec_anatime_intran)
            
            sim_waited = False
            # the sim continue to work
        
        exec_simtime_intran=temp_sim_start+compute_sim_time(step_sim,procs_num,1)
        print("step ", step_sim, " after sim, the time is ", exec_simtime_intran)
        # check if to do the data transfer
        if step_sim%frequency_transfer == 0:
            if need_to_process_len<queue_len_limit:
                # sim move forward
                exec_simtime_intran=exec_simtime_intran+compute_transfer_time(step_sim,procs_num,datasize_multiplier)
                # one step data need to be processed
                lock.acquire()
                need_to_process_len+=1
                lock.release()
                # push the data information into the queue
                print("step ", step_sim, " exec_simtime_intran ", exec_simtime_intran, "need_to_process_len ", need_to_process_len)
                data_staging_queue.put(DataNode(step_sim, exec_simtime_intran))
            elif need_to_process_len==queue_len_limit:
                # sim wait here, wait the ana to execute
                print("sim wait at step ", step_sim, " need_to_process_len " , need_to_process_len, " queue_len_limit ", queue_len_limit, "qsize", data_staging_queue.qsize())
                sim_waited=True
                time.sleep(0.1)
            else:
                print("error: need_to_process_len is supposed to large or equal to 0")
                break
            
        # sim can move forward anyway, it stops only when it visit the transfer part
        # and to see if it needs 
        temp_sim_start = exec_simtime_intran
        step_sim += 1

def doing_ana_computation(data_staging_queue,lock):
    # continue fetching the data from the queue until getting the last step
    # complete subsequent tasks if there are remaining things
    # the ana need to complete subsequent tasks
    # if the queue length is a really large number
    global exec_anatime_intran
    global need_to_process_len
    temp_ana_start = 0
    complete_processing = False
    while complete_processing==False:
        while data_staging_queue.empty()==False:
            data_info = data_staging_queue.get()
            temp_ana_start = max(exec_anatime_intran, data_info.data_generated_time)
            exec_anatime_intran=temp_ana_start+compute_ana_time(data_info.step,procs_num,datasize_multiplier,workload_multiplier)
            lock.acquire()
            need_to_process_len-=1
            print("step ",data_info.step," exec_anatime_intran ", exec_anatime_intran)
            print("ana need_to_process_len ", need_to_process_len)
            lock.release()
            if data_info.step==total_step:
                complete_processing=True
        # wait the sim to generate the data
        time.sleep(0.1)    

# hybird space and time division
def compute_hybrid():
    print("todo, compute hybrid")


def test1():
    total_step=10
    compute_inline()
    compute_intran()

if __name__ == "__main__":
    # todo use multiple test here
    test1()