procs=4
intransit_proc_num=2
proclist = list(range(0,procs))
count=0

# TODO, how to do the trim operation here?
def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]

    # this is the dfs search
    for smaller in partition(collection[1:]):
        # do not continue the search if the smaller is already large then intran proc number
        if len(smaller)>=intransit_proc_num:
            return


        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller


# go through all the combinations
for n, p in enumerate(partition(proclist), 1):
    sorted_p_list=sorted(p)
    print(sorted_p_list)
    if len(sorted_p_list)==intransit_proc_num:
        count=count+1
print(count)