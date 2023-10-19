if __name__ == "__main__":
    procs = 128
    outputfile = "assign_options.config"
    with open(outputfile, 'w') as f:
        for rank in range(0,procs,1):
            f.write(str(rank))
            cycle=1
            if rank % cycle ==0:
                for i in range(1,cycle,1):
                    f.write(" "+str(rank+i))
            if rank%2==0:
                f.write(" "+str(76))
            else:
                f.write(" "+str(77))
            f.write('\n')