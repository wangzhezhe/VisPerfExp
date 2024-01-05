# input is the number of wokrload for each rank
# output is the plan with the 
# associated strategy for bin packing problem https://en.wikipedia.org/wiki/Bin_packing_problem#Comparison_table
# approach to find outlier
# https://stackoverflow.com/questions/57161413/is-there-function-that-can-remove-the-outliers
# the detected outliers mgiht have ping-pong issues
# for workload within the range using round-roubin or approximation approach
# redistributed these outlaiers among other processes
# or using k means, and the same type are assigned by round roubine way

import numpy
import copy
import sys

min_variance=sys.float_info.max
optimized_plan=[]

def set_optimized_plan(optimized_plan):
    return optimized_plan

def find_plan(assign_plan, original_plan, remain_blocks):
    #print(assign_plan, original_plan, remain_blocks)
    # exit condition
    global min_variance
    global optimized_plan
    if remain_blocks==0:
        # check the variance of assign_plan
        # keep the optimized plan
        assign_plan_work_list=[]
        for plan in assign_plan:
            sum_workload=0
            for index in plan:
                sum_workload+=original_plan[index]
            assign_plan_work_list.append(sum_workload)
        
        var = numpy.std(assign_plan_work_list)
        #print("---check assign_plan_work_list",assign_plan_work_list, " var", var, "min_variance",min_variance)

        if  var<min_variance:
            # update the plan
            min_variance=var
            optimized_plan=copy.deepcopy(assign_plan)
            # print("debug assign_plan",assign_plan,"optimized_plan",optimized_plan)

        return

    # for current one, go through each possible position in assigned plan
    curr_work_index = len(original_plan)-remain_blocks
    for i in range(len(assign_plan)):
        assign_plan[i].append(curr_work_index)
        # go to next layer
        # def find_plan(assign_plan, original_plan, remain_blocks, optimized_plan, min_variance):
        find_plan(assign_plan,original_plan,remain_blocks-1)

        # pop last element 
        assign_plan[i].pop()
    

workload_list=[200,210,220,205,190,195,198,190]
#workload_list=[200,210,220,250]
targeted_rank=4
plan=[]

for i in range(targeted_rank):
    plan.append([])

find_plan(plan,workload_list,len(workload_list))
print("optimized_plan ",optimized_plan,"optimal variance", min_variance)
# associated workload
optimized_plan_workload_list=[]
optimized_plan_workload_sum=[]

for plan in optimized_plan:
    sum_workload=0
    plan_workload=[]
    for index in plan:
        sum_workload+=workload_list[index]
        plan_workload.append(workload_list[index])
    optimized_plan_workload_sum.append(sum_workload)
    optimized_plan_workload_list.append(plan_workload)
print("optimized_plan_workload_sum",optimized_plan_workload_sum)
print("optimized_plan_workload_list",optimized_plan_workload_list)


