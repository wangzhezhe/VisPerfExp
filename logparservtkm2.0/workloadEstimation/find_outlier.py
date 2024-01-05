import numpy as np



anomalies = []
def find_anomalies(data):
    # Set upper and lower limit to 3 standard deviation
    data_std = np.std(data)
    data_mean = np.mean(data)
    anomaly_cut_off = data_std * 3

    lower_limit = data_mean - anomaly_cut_off 
    upper_limit = data_mean + anomaly_cut_off

    # Generate outliers
    for outlier in data:
        if outlier > upper_limit or outlier < lower_limit:
            anomalies.append(outlier)
    return anomalies

if __name__ == "__main__":
    #workload_list=[200,210,220,205,1000,2000,3000,10000]
    workload_list=[1,2,10000]
    
    print("test percentile", np.percentile(workload_list, 2))

    print("find_anomalies",find_anomalies(workload_list))


    q1, q3= np.percentile(workload_list,[25,75]) # get percentiles
    iqr = q3 - q1 # the IQR value
    lower_bound = q1 - (1.5 * iqr) # lower bound
    upper_bound = q3 + (1.5 * iqr) # upper bound

    print(lower_bound,upper_bound)