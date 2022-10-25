import sys
import statistics 

data_list = []
real_data_list = []
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

for line in sys.stdin:
    new_list = [(elem) for elem in line.split()]
    if(len(new_list)>0):
      data_list.append(new_list[0])

if __name__ == "__main__":
    labelstr = str(sys.argv[1])
    #print (data_list)
    # delete useless string
    for d in (data_list):
        if isfloat(d):
            real_data_list.append(float(d))


    if len(real_data_list)==0:
        exit(0)

    #print (real_data_list)
    #print ("len", len(real_data_list))
    print (labelstr+ " avg", statistics.mean(real_data_list))
    print (labelstr+" min", min(real_data_list) )
    print (labelstr+" max", max(real_data_list) )
    #print ("std",statistics.stdev(real_data_list))
    #print ("sum",sum(real_data_list))