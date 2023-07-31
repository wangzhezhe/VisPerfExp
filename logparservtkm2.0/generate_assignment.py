



if __name__ == "__main__":
    procs = 8
    outputfile = "assign_options.config"
    with open(outputfile, 'w') as f:
        for rank in range(0,procs,1):
            f.write(str(rank))
            cycle=2
            if rank % cycle ==0:
                for i in range(1,cycle,1):
                    f.write(" "+str(rank+i))
            f.write('\n')        