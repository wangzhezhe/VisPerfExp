from scipy.optimize import least_squares
import numpy as np
import matplotlib.pyplot as plt



def sample_y(theta, t):
    # this is a logistic function
    return theta[0] / (1 + np.exp(- theta[1] * (t - theta[2])))

ts = np.linspace(0, 1)
K = 1; r = 10; t0 = 0.5; noise = 0.1
raw_y = sample_y([K, r, t0], ts) + noise * np.random.rand(ts.shape[0])
#print(raw_y)

def sample_fun(theta):
    return sample_y(theta, ts) - raw_y

def ls_sample():

    # train the model
    theta0 = [1,2,3]
    res1 = least_squares(sample_fun, theta0)

    print(res1.x)

    f_predicted = sample_y(res1.x, ts)

    fig, ax = plt.subplots()

    ax.plot(raw_y)
    ax.plot(f_predicted)

    plt.savefig("sample_least_square.png",bbox_inches='tight')


# x is procs number
# theta are other parameters

def rr_model(theta, proc_num):
    #return theta[0]*pow(theta[1],-proc_num)
    #return theta[0]+theta[1]*proc_num+theta[2]*pow(proc_num,2)
    return theta[0]*pow(theta[1],-proc_num)+ theta[2] / (1 + np.exp(-(proc_num - theta[3])))
    #return theta[0]*pow(theta[1],-proc_num)+ theta[2] / (1 + np.exp(-theta[3]*(proc_num - theta[4])))
    
def rr_fun(theta):
    proc_num=np.array([2,3,4,5,6,7,8,9,10])
    raw_y=np.array([6.95506,4.00497,3.19588,2.15126,1.15601,0.931642,0.852762,0.90412,1.05902])
    return rr_model(theta, proc_num) - raw_y

def ls_render_resources():

    #theta0 = [1.0,2]
    theta0 = [1.0,1,2,8]
    #theta0 = [1.0,1,2,0.2,8]
    #theta0 = [1.0,1,2,0.2,16]
    res1 = least_squares(rr_fun, theta0)
    print(res1.x)
    proc_num=np.array([2,3,4,5,6,7,8,9,10])
    rr_predicted = rr_model(res1.x, proc_num)

    #print(f_predicted)

    fig, ax = plt.subplots()
    dist = 1.0
    offset=0
    xindex=[]
    for i in range (0,9):
        xindex.append(offset+i*dist)
    ax.set_xticks(xindex)

    ax.set_xticklabels(('4','8','16','32','64','128', '256','512','1024'), fontsize='large')

    #ax.plot(raw_y)
    rr_raw_y=np.array([6.95506,4.00497,3.19588,2.15126,1.15601,0.931642,0.852762,0.90412,1.05902])
    ax.plot(rr_raw_y)
    ax.plot(rr_predicted,linestyle='--')
    
    plt.savefig("ls_render_resources.png",bbox_inches='tight')

    return


if __name__ == "__main__":
    #ls_sample()
    ls_render_resources()
