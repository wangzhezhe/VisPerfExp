

import model_components
import model_workflow

# implement naive one
class NaiveModel(model_components.ComponentsCostModel):
    def set_exec(self, sim_exec, ana_exec, transfer):
        self.sim_exec=sim_exec
        self.ana_exec=ana_exec
        self.transfer=transfer

    def compute_sim_time(self, step, procs_num, datasize_multiplier):
        return self.sim_exec
    def compute_ana_time(self, step, procs_num, datasize_multiplier, workload_multiplier):
        return self.ana_exec
    # for the inline case, the data transfer time can be assumed as 0
    def compute_transfer_time(self, step, procs_num, datasize_multiplier):
        return self.transfer

if __name__ == "__main__":
    #logfile = "test_naive_range.log"
    for t in {2,4,6}:
        for sim in range (1,11,1):
            for ana in range (1,11,1):

                #print("sim exec ", sim, "ana exec", ana, "transfer", t,flush=True)
                # create the test classes 
                app_model = NaiveModel()
                app_model.set_exec(sim, ana, t)

                # send application model to workflow model
                wf_model = model_workflow.WorkflowModel(app_model)

                total_step=50
                queue_len_limit=1

                wf_model.init_wflow_parameters(total_step, queue_len_limit)
                compute_inline_time = wf_model.compute_inline()
    
                wf_model.compute_intran()

                exec_simtime_intran = wf_model.exec_simtime_intran
                
                exec_anatime_intran = wf_model.exec_anatime_intran

                               
                print("sim", sim, "ana", ana, "tran", t, "compute_inline_time is", compute_inline_time, flush=True)
                print("sim", sim, "ana", ana, "tran", t, "exec_simtime_intran is", exec_simtime_intran, flush=True)
                print("sim", sim, "ana", ana, "tran", t, "exec_anatime_intran is", exec_anatime_intran, flush=True)
                
                sim_wait = exec_anatime_intran-exec_simtime_intran
                if(sim_wait<0):
                    sim_wait=0
                print("sim", sim, "ana", ana, "tran", t, "sim wait time at last step is", sim_wait, flush=True)
                
                compute_intransit_time = max(exec_simtime_intran,exec_anatime_intran)
                print("sim", sim, "ana", ana, "tran", t, "exec_intran is", compute_intransit_time , flush=True)

                print("sim", sim, "ana", ana, "tran", t, "diff between inline and intransit", compute_inline_time-compute_intransit_time, flush=True)