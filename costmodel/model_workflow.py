import queue
import threading
from threading import Thread
import time
import model_components

# Algorithm associted parameters
# seeds, image size, number of surface values

# Workflow design params
#proximity=["inline","intransit"]
# the frequency that the ana visit the sim data
#visit_freq=[1,2,3,4,5]
#proc_num_sim=[1,2,3,4,5,6]
#proc_num_ana=[1,2,3,4,5,6]
# queue length
# the length of the caching queue
# for the file io, we can assume the queue length is infinity
# for the streaming io such as SST, the sim will block when it comes
# to the limitation of the queue, it is the producer-consumer pattern
#queue_length=[1,2,3,4,5,6]
#num_proc_per_node_sim=1
#num_proc_per_node_ana=1

# Task related information 
# For the fixed visualization parameters, how exec time change with step can be the baseline
# It contains the information of data size
# datasize_multiplier indicates the data size compared with the baseline
# total_step=5

# TODO, more detailed model can get the performance model based on workload and datasize direactly.
# instead of using the change of the step as the baseline
# which means we can also vary the workload parameter 
# or have different multiplier, such as data size multiplier, seeds number multiplier, etc 
# from small scale to large scale

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

class DataNode:
     def __init__(self, step, data_generated_time):
         self.step = step
         self.data_generated_time = data_generated_time

# space division

class WorkflowModel:
    def __init__(self, components_model):
        self.m_components_model = components_model
        self.queue_len_limit=1
        self.need_to_process_len = 0
        # for processing the need_to_process_len
        self.lock = threading.Lock()
        self.frequency_transfer=1
        self.frequency_anavisit=1
        self.exec_simtime_intran= 0
        self.exec_anatime_intran= 0
        self.sim_datasize_multiplier=1


    def init_wflow_parameters(self,total_step,queue_len_limit):
        self.total_step=total_step
        self.queue_len_limit=queue_len_limit

    # time division
    def compute_inline(self):
        exec_time_inline=0
        procs_num=1
        datasize_multiplier=1
        workload_multiplier=1
        frequency=1
    
        step = 1
        # using total_step+1 to check the last step
        while step < self.total_step+1:
            exec_time_inline+=self.m_components_model.compute_sim_time(step,procs_num,1)
            if step%frequency==0:
                exec_time_inline+=self.m_components_model.compute_ana_time(step,procs_num,1,1)
            step+=1
            
        return exec_time_inline

    def doing_sim_computation(self,data_staging_queue):
        # start from the first step
        
        step_sim = 1
        temp_sim_start=0
        sim_waited = False
        # this might be a function
        procs_num=1
        waited_transfer_time=0
        # the step here is the simulation iteration step
        # visit frequency might be different with the data transfer frequency
        while step_sim < (self.total_step+1):
            # for sim
            # there are two decisions
            # 1> do the next step sim computation (look at transfering the data to ana program)
            # 2> wait the ana program
            
            # if this is the first step after the sim wait
            # we need to adjust the start time
            #if sim_waited==True:

            #    # continue check, the block section happens to the transfer part
            #    if self.need_to_process_len==self.queue_len_limit:
            #        time.sleep(0.01)
            #        continue
            #    else:
                    # only update the sim start when it waited previously
                    # also need to add previous data transfer time
                    # Maybe also need to consider the time to get the data for the ana
                    # this transfer time happens only when the block is resoved by ana
            #        temp_sim_start=temp_sim_start+self.m_components_model.compute_sim_time(step_sim,procs_num,self.sim_datasize_multiplier)
            #        temp_sim_start=max(temp_sim_start,self.exec_anatime_intran)
            #        sim_waited = False
                # the sim continue to work
            if sim_waited==True:
                # only update the temp_sim_start when it waits
                temp_sim_start=max(temp_sim_start,self.exec_anatime_intran)
                # reset the flag to False
                sim_waited=False
                # the wait is resolved now we can transfer the data
                temp_sim_start = temp_sim_start+waited_transfer_time
                waited_transfer_time=0
                # put the data into the queue for the block case for the last step
                # push the previous data, after the wait is resolved??
                data_staging_queue.put(DataNode(step_sim-1, temp_sim_start))

            else:
                temp_sim_start=self.exec_simtime_intran
                
            self.exec_simtime_intran=temp_sim_start+self.m_components_model.compute_sim_time(step_sim,procs_num,1)
            #print("step ", step_sim, " after sim, the time is ", self.exec_simtime_intran)

            # check if to do the data transfer
            if step_sim%(self.frequency_transfer) == 0:
                if self.exec_simtime_intran<self.exec_anatime_intran:
                   # sim need to wait here until the ana complete
                   # for the case ana is longer than sim
                   self.exec_simtime_intran = self.exec_anatime_intran

                if self.need_to_process_len<self.queue_len_limit:
                    # sim move forward
                    self.exec_simtime_intran=self.exec_simtime_intran+self.m_components_model.compute_transfer_time(step_sim,procs_num,self.sim_datasize_multiplier)
                    
                    # push the data information into the queue when transfer 
                    # print("step ", step_sim, " exec_simtime_intran ", self.exec_simtime_intran, "need_to_process_len ", self.need_to_process_len)
                    data_staging_queue.put(DataNode(step_sim, self.exec_simtime_intran))
                    
                    # after the transfer operation
                    # one step data need to be processed
                    self.lock.acquire()
                    self.need_to_process_len+=1
                    self.lock.release()

                    # TODO wait some time for consumer to get data, use the notify here
                    time.sleep(0.02)
                    # only move to next step when put data into the queue
                    # do nothing when the sim is in waiting status
                elif self.need_to_process_len==self.queue_len_limit:
                    # or (self.exec_simtime_intran<self.exec_anatime_intran):
                    # sim wait here, wait the ana to execute
                    # print("sim wait after step ", step_sim, " need_to_process_len " , self.need_to_process_len, " queue_len_limit ", self.queue_len_limit, "qsize", data_staging_queue.qsize(), "self.exec_simtime_intran ", self.exec_simtime_intran, "self.exec_anatime_intran ",self.exec_anatime_intran)
                    sim_waited = True
                    while self.need_to_process_len==self.queue_len_limit:
                        time.sleep(0.01)
                        continue
                    # we need to transfer the data for this time when the wait is resolved
                    waited_transfer_time = self.m_components_model.compute_transfer_time(step_sim,procs_num,self.sim_datasize_multiplier)

                else:
                    print("error: need_to_process_len is supposed to less or equals to 0")
                    break
                
            # sim can move forward anyway, it stops only when it visit the transfer part
            # and to see if it needs 
            # temp_sim_start = self.exec_simtime_intran
            step_sim += 1

        # TODO also need to put the data generated by the last step into the staging queue\
        # print("doing_sim_computation completes processing at ", self.exec_simtime_intran)

    def doing_ana_computation(self,data_staging_queue):
        # continue fetching the data from the queue until getting the last step
        # complete subsequent tasks if there are remaining things
        # the ana need to complete subsequent tasks
        # if the queue length is a really large number
        procs_num=1
        datasize_multiplier=1
        workload_multiplier=1
        temp_ana_start = 0
        complete_processing = False
        while complete_processing==False:
            while data_staging_queue.empty()==True:
                # wait here until there is data in queue
                # make this time more frequent then the sim wait time
                # TODO, use wait notify here
                time.sleep(0.001)   
                continue
                # process the data step by step
            while data_staging_queue.empty()==False:
                data_info = data_staging_queue.get()
                temp_ana_start = data_info.data_generated_time
                #print("---ana get the start time ", temp_ana_start)
                self.exec_anatime_intran=temp_ana_start+self.m_components_model.compute_ana_time(data_info.step,procs_num,datasize_multiplier,workload_multiplier)
                
                self.lock.acquire()
                self.need_to_process_len-=1
                #print("step ",data_info.step," exec_anatime_intran ", self.exec_anatime_intran)
                #print("ana need_to_process_len ", self.need_to_process_len)
                self.lock.release()
                
                if data_info.step==self.total_step:
                    complete_processing=True
                #print("cdata_info.step inner ", data_info.step)

        #print("doing_ana_computation completes processing")
    
    def compute_intran(self):

        temp_ana_start=0
        data_staging_queue = queue.Queue()

        #sim_exec = ThreadWithReturnValue(target=doing_sim_computation, args=(data_staging_queue,lock))
        sim_exec = threading.Thread(target=self.doing_sim_computation, args=(data_staging_queue,))
        sim_exec.start()
        #ana_exec = ThreadWithReturnValue(target=doing_ana_computation, args=(data_staging_queue,lock))
        ana_exec = threading.Thread(target=self.doing_ana_computation, args=(data_staging_queue,))
        ana_exec.start()
        
        ana_exec.join()
        sim_exec.join()


        #print("exec_simtime_intran is ", self.exec_simtime_intran)
        #print("exec_anatime_intran is ", self.exec_anatime_intran)
        sim_wait = self.exec_anatime_intran-self.exec_simtime_intran
        if sim_wait<0:
            sim_wait=0
        #print("sim wait time at last step is ", sim_wait)
