from abc import ABC, abstractmethod

class ComponentsCostModel(ABC):
    @abstractmethod
    def compute_sim_time(self, step, procs_num, datasize_multiplier):
        pass
    @abstractmethod
    def compute_ana_time(self, step, procs_num, datasize_multiplier, workload_multiplier):
        pass
    # for the inline case, the data transfer time can be assumed as 0
    @abstractmethod
    def compute_transfer_time(self, step, procs_num, datasize_multiplier):
        pass