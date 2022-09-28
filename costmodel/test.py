

import model_components
import model_workflow

# implement naive one
class NaiveModelSimGAna(model_components.ComponentsCostModel):

    def compute_sim_time(self, step, procs_num, datasize_multiplier):
        return 10
    def compute_ana_time(self, step, procs_num, datasize_multiplier, workload_multiplier):
        return 5
    # for the inline case, the data transfer time can be assumed as 0
    def compute_transfer_time(self, step, procs_num, datasize_multiplier):
        return 1

class NaiveModelSimLAna(model_components.ComponentsCostModel):

    def compute_sim_time(self, step, procs_num, datasize_multiplier):
        return 5
    def compute_ana_time(self, step, procs_num, datasize_multiplier, workload_multiplier):
        return 15
    # for the inline case, the data transfer time can be assumed as 0
    def compute_transfer_time(self, step, procs_num, datasize_multiplier):
        return 1

class NaiveModelCustomize(model_components.ComponentsCostModel):

    def compute_sim_time(self, step, procs_num, datasize_multiplier):
        return 15
    def compute_ana_time(self, step, procs_num, datasize_multiplier, workload_multiplier):
        return 15
    # for the inline case, the data transfer time can be assumed as 0
    def compute_transfer_time(self, step, procs_num, datasize_multiplier):
        return 1

# supposed to be 55 60
def test_sim_g_ana():
    print("---test test_sim_g_ana---")

    app_model = NaiveModelSimGAna()

    # send application model to workflow model
    wf_model = model_workflow.WorkflowModel(app_model)
    
    # TODO, get these parameters from the input file
    total_step=5
    queue_len_limit=1

    wf_model.init_wflow_parameters(total_step, queue_len_limit)
    compute_inline_time = wf_model.compute_inline()
    
    # TODO, there are still some issues, when we set the wait 
    # time as a really small number
    wf_model.compute_intran()
    print("compute_inline_time is ", compute_inline_time)


# supposed to be 70 85
def test_sim_l_ana():

    print("---test test_sim_l_ana---")
    
    app_model = NaiveModelSimLAna()

    # send application model to workflow model
    wf_model = model_workflow.WorkflowModel(app_model)
    
    total_step=5
    queue_len_limit=1

    wf_model.init_wflow_parameters(total_step, queue_len_limit)
    compute_inline_time = wf_model.compute_inline()
    
    
    wf_model.compute_intran()
    print("compute_inline_time is ", compute_inline_time)


def test_customize():

    print("---test test_customize---")
    
    app_model = NaiveModelCustomize()

    # send application model to workflow model
    wf_model = model_workflow.WorkflowModel(app_model)
    
    total_step=5
    queue_len_limit=1

    wf_model.init_wflow_parameters(total_step, queue_len_limit)
    compute_inline_time = wf_model.compute_inline()
    
    
    wf_model.compute_intran()
    print("compute_inline_time is ", compute_inline_time)

if __name__ == "__main__":
    #test_sim_g_ana()
    #test_sim_l_ana()

    test_customize()

    #test_unlimited_qlen()
    #TODO
    #test_hybrid()