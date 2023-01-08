import os

# the number of inline procs
procs=4

# the number of in-transit procs
group_limit =2

# a list which has length of procs
proclist = list(range(0,procs))
count=0

dir_name_all="./assignment_all_"+str(procs)+"_"+str(group_limit)

def outputAssignment(index, assignPlan):
    
    if not os.path.isdir(dir_name_all):
        print('The directory is not present. Creating a new one..')
        os.mkdir(dir_name_all)

    f = open(dir_name_all+"/assign_options.config_"+str(index),'w')
    for option in assignPlan:
        option_str=""
        for index, blockid in enumerate(option):
            if index==0:
                option_str=str(blockid)
            else:
                option_str=option_str+" "+str(blockid)
        f.write(option_str+"\n")
    f.close() 

# this is the way to go through all partitions
# refer to this solution
# https://stackoverflow.com/questions/39192777/how-to-split-a-list-into-n-groups-in-all-possible-combinations-of-group-length-a
def partition(collection):
    # there is only one element in the list
    # print("show collection",collection)
    if len(collection) == 1:
        yield [ collection ]
        return

    # get the first element of the collection
    first = collection[0]
    # the remaining part is collection[1:]
    #print("partition collection",first, collection[1:])

    # this is the dfs search
    for smaller in partition(collection[1:]):
        # for each case in the second part of the partition
        # there are two combinations

        # insert `first` in each of the subpartition's subsets
        # smaller is an list of combinations
        # the first can be in any one of this group
        # for the case out of the box, the smaller[] returns null
        for n, subset in enumerate(smaller):
            #print("smaller",smaller, "n", n, "smaller[:n]", smaller[:n], "smaller[n+1:]",smaller[n+1:], "len(smaller)", len(smaller))
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        
        # the first can be an extra element
        # put `first` in its own subset 
        if len(smaller)>=group_limit:
            # do not further search when the group number is larger than limitation
            # trim some unwanted partitions, which has a longer length
            continue
        else:
            yield [ [ first ] ] + smaller


# go through all the combinations
for n, p in enumerate(partition(proclist), 1):
    sorted_p_list=sorted(p)
    #print(sorted_p_list)
    if len(sorted_p_list)==group_limit:
        # output the option if the number of group satisfies results
        outputAssignment(count, sorted_p_list)
        count=count+1

print("Total assignment plan",count)

# output type

# static rr continuous
# all options (8 inline, 4 or less intran is a resonable evaluation case)

# output other assignment type
# maybe based on heuristics approach

'''
16 in line procs
4 in tran procs
Group cases 171798901

8 inline procs
4 intran procs
Group cases 1701

4 inline procs
2 in tran procs
Group cases 7

m inline procs
n intran procs
each procs can go to n different slots
total combinations are n^m
Maybe using the rl to find a good solution?
'''