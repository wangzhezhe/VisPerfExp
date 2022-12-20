

# TODO, how to do the trim operation here?
def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller

procs=16
intransit_proc_num=4
proclist = list(range(0,procs))
count=0

for n, p in enumerate(partition(proclist), 1):
    sorted_p_list=sorted(p)
    if len(sorted_p_list)==intransit_proc_num:
        count=count+1
print(count)