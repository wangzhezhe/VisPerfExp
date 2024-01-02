






if __name__ == "__main__":
    if len(sys.argv)!=5:
        print("<binary> <dataset name> <runDirPath> <num_rank> <num_test_points>",flush=True)
        exit()
    dataset_name=sys.argv[1]
    dirPath=sys.argv[2]
    num_rank=int(sys.argv[3])
    num_test_points=int(sys.argv[4])