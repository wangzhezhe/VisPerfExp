# Use the some functions in RankParticiption code written by Dave Pugmire

import sys
import matplotlib.pyplot as plt

def getTimeRange(TIMES) :
    tMin = 1e20
    tMax = -1e20

    for t in TIMES[1:] :
        if len(t) > 1 :
            tMin = min(tMin, t[0])
            tMax = max(tMax, t[-1])
    return (tMin, tMax)

def participationBins(TIMES, numBins) :
    (tMin, tMax) = getTimeRange(TIMES)
    dT = tMax/(numBins)
    #print('************ tMin/Max= ', (tMin, tMax), 'dT= ', dT)

    ALLPT = []
    CNT = 0
    for TIME in TIMES :
        PT = [0] * numBins
        N = len(TIME)
        idx = 0
        while idx < N :
            binIdx0 = int(TIME[idx] / dT)
            binIdx1 = int(TIME[idx+1] / dT)
            if binIdx0 >= numBins : binIdx0 = numBins-1
            if binIdx1 >= numBins : binIdx1 = numBins-1
            #if CNT == 0 : print(idx, ': ******** bins: ', binIdx0, binIdx1, TIME[idx], TIME[idx+1])
            PT[binIdx0] = 1
            for b in range(binIdx0, binIdx1) : PT[b] = 1
            idx = idx+2
        ALLPT.append(PT)
        CNT = CNT + 1
    return ALLPT

def readTimeTrace(fdir, nRanks) :
    TIMES = []
    EVENTS = []
    CNT = 0
    #print('dir=', fdir, 'nRanks=', nRanks)
    for r in range(nRanks) :
        fname = '%s/timetrace.%d.out'% (fdir, r)
        #print('    reading: ', fname)
        f = open(fname, 'r')
        allLines = f.readlines()
        #if r == 1 : print(allLines)

        TIME = []
        ADV = []
        COMM = []
        T0 = -1
        AT0, AT1 = (0,0)
        C0, C1 = (0,0)
        EVENT = []
        for line in allLines :
            x = line.strip().split(' ')
            if "**" in x:
                # new log add ** at the start position
                continue
            event = x[0].split('_')[0]
            step = int(x[0].split('_')[-1])
            # change to ms
            time = float(x[1])/1000
            # do not consider the case when step is 1
            # we only process the case when step is 0
            if step != 0 : continue
            
            #print('x=', x, 'step=',step, 'event=', event)
            if len(TIME) == 0 and event == 'GoStart': T0 = time
            time = time - T0
            if event == 'AdvectStart' : AT0 = time
            if event == 'AdvectEnd' :
                AT1 = time
                if AT1-AT0 > 1 : 
                    TIME.append(AT0)
                    TIME.append(AT1)
                    EVENT.append(['A', 'A'])
            if event == 'CommStart' : C0 = time
            if event == 'SendDataEnd' : 
                C1 = time
                if C1-C0 > 1 :
                    TIME.append(C0)
                    TIME.append(C1)
                    EVENT.append(['C', 'C'])
                    #print('************ COMM = ', (C0,C1))

            #elif event == 'CommStart' :   TIME.append(time)
            #elif event == 'SyncCommStart' : TIME.append(time)
        TIMES.append(TIME)
        EVENTS.append(EVENT)
    return TIMES, EVENTS

def computeParticipation(ALLBINS, nRanks, numBins) :
    PARTICIPATION = [0]*numBins
    for b in range(numBins) :
        for r in range(nRanks) :
            PARTICIPATION[b] += ALLBINS[r][b]
        PARTICIPATION[b] = float(PARTICIPATION[b]) / float(nRanks)
    return PARTICIPATION

def mkLabel(imageNm) :
    #print(imageNm)
    res = imageNm
    res = imageNm.replace('0.clover', '0')
    res = res.replace('.B.', '.WHOLE.')
    res = res.replace('.B0.', '.BOX50.')
    res = res.replace('.B1.', '.BOX25.') 
    res = res.replace('.B2.', '.BOX10.')
    res = res.replace('.B3.', '.BOX05.')

    return res

labelSize = 25
tickSize = 23
lwidth=2.5

def calcParticipation(ax, pdata, TIMES, numBins, imageNm, drawPlots=True) :
    (tMin, tMax) = getTimeRange(TIMES)
    dT = tMax/(numBins)
    #print('************************************* dT= ', dT)
    X = [0]
    for b in range(numBins-1) :
        X.append(X[-1] + dT)
    SUM = sum(pdata)
    
    #print('X=', X, len(X))
    #print('Y=', pdata, len(pdata))
    
    imgLabel = mkLabel(imageNm)
    participationRate = SUM/numBins
    
    if drawPlots :
        #fig, ax = plt.subplots(figsize=(7,6))
        ax.title.set_text(imgLabel)
        ax.title.set_fontsize(labelSize)

        ax.set_ylim([0.0, 1.1])
        #ax.set_xlabel(imageNm, fontsize=labelSize)
        #ax.set_aspect('auto')
        if imageNm=="Tokamak":
            #only label at the first one
            ax.set_ylabel('Rank Participation', fontsize=labelSize)
        else:
            ax.set_yticks([])

        ax.tick_params(axis='y', labelsize=tickSize)
        ax.tick_params(axis='x', labelsize=tickSize)


        ax.plot(X, pdata,linewidth=lwidth)
    return (participationRate, X, pdata)

if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath for all>")
        exit()
    
    numRanks=int(sys.argv[1])
    dirPath=sys.argv[2]

    # dataname=["fusion.A.b128.n4.r128.B_p5000_s2000",
    #           "astro.A.b128.n4.r128.B_p5000_s2000",
    #           "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
    #           "clover.A.b128.n4.r128.B_p5000_s2000",
    #           "syn.A.b128.n4.r128.B_p5000_s2000"]

    dataname=["fusion.A.b128.n4.r128.B_p5000_s2000_id582493",
               "astro.A.b128.n4.r128.B_p5000_s2000_id418463",
               "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
               "clover.A.b128.n4.r128.B_p5000_s2000_id275499",
               "syn.A.b128.n4.r128.B_p5000_s2000_id365728"]

    official_name = ["Tokamak","Supernova","Hydraulics","CloverLeaf3D","Synthetic"]

    fig, axs = plt.subplots(nrows=1, ncols=5,figsize=(7*5,6))

    for index, data in enumerate(dataname):
        dir_path_complete = dirPath+"/"+data
        print("process ", dir_path_complete )
        TIMES, EVENTS = readTimeTrace(dir_path_complete, numRanks)

        numBins = 50

        ALLBINS=participationBins(TIMES,numBins)

        PARTICIPATION = computeParticipation(ALLBINS, numRanks, numBins)
        calcParticipation(axs[index], PARTICIPATION, TIMES, numBins, official_name[index], True)
    
    fig.text(0.5, 0.0, 'Time (ms)', ha='center',fontsize=labelSize+2)
    fig.savefig("rank_participation_all.png",bbox_inches='tight')
    fig.savefig("rank_participation_all.pdf",bbox_inches='tight')
