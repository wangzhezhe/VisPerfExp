# Use the some functions in RankParticiption code written by Dave Pugmire

import sys
import os
import matplotlib.pyplot as plt

def cmp (x) :
    v = int(x.split('.')[2][1:])
    #print('x=',v)
    return v
def BLOCK_CMP(x) :
    v = int(x.split('.')[2][1:])
    return v
def STEP_CMP(x) :
    v = int(x.split('.')[5].split('_')[2][1:])
    return v
def CMP(x) :
    X = x.split('.')
    Y = X[5].split('_')
    B = int(X[2][1:])
    R = int(X[4][1:])
    S = int(Y[2][1:])
    #v = '%s.%s.%s' % (X[2][1:], X[4][1:], Y[2][1:])
    v = S + 10000*R + 1000000*B
    print(x, '-->', v)
    return v
                       
def MATCH(sel, value, prefix) :
    #print('MATCH', sel, value, prefix)
    if sel == None : return True
    if type(sel) == type([]) :
        for s in sel :
            #print('%s%d' % (prefix, s), value)
            if '%s%d' % (prefix,s) == value : return True
    elif '%s%d' % (prefix,sel) == value : return True
    return False


def GET_RUNS(dataDir, fSel, blockSel=None, boxSel='B', stepSel=None, commSel='A', parSel=5000, rankSel=None) :
    # list files in current dir
    # parse the file name separately
    allFiles = os.listdir(dataDir)
    res = []
    for f in allFiles :
        x = f.split('.')
        if len(x) != 6 : continue
        
        (DS, COMM, BLOCKS, NODES, RANKS) = (x[0], x[1], x[2], x[3], x[4])
        y = x[5].split('_')
        (BOX, PARTICLES, STEPS) = (y[0], y[1], y[2])
        
        if DS != fSel : continue
        if COMM != commSel : continue
        if not MATCH(blockSel, BLOCKS, 'b') : continue
        if not MATCH(rankSel, RANKS, 'r') : continue
        if boxSel and BOX != boxSel : continue
        if not MATCH(stepSel, STEPS, 's') : continue
        if not MATCH(parSel, PARTICLES, 'p') : continue
        
        res.append(f)
    if len(res) > 0 :
        #res = sorted(res, key=CMP)
        if blockSel != None  : res = sorted(res, key=STEP_CMP)
        elif stepSel != None : res = sorted(res, key=BLOCK_CMP)
        
    return res

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
            #print(x)
            event = x[0].split('_')[0]
            step = int(x[0].split('_')[-1])
            time = float(x[1])
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

def calcParticipation(pdata, TIMES, numBins, imageNm, drawPlots=True) :
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
        fig, ax = plt.subplots(figsize=(7,6))
        #ax.title.set_text('%s Avg= %f' %(imgLabel, participationRate))
        ax.set_ylim([0.0, 1.1])
        ax.set_xlabel('Time (ms)', fontsize="large")
        ax.set_aspect('auto')
        ax.set_ylabel('Rank Participation', fontsize="large")
        ax.plot(X, pdata, linewidth=lwidth)
        fig.savefig("rank_participation_"+imageNm + '.png',bbox_inches='tight')
    return (participationRate, X, pdata)


def parseAndPlotParticipation(logPath, logName, numRanks, numBins, drawPlots=True):
    #print(fname)
    fname = logPath+"/"+logName
    TIMES, EVENTS = readTimeTrace(fname, numRanks)
    #print('T0= ', TIMES[0])
    ALLBINS = participationBins(TIMES, numBins)
    #print('ALLBINS[0]=', ALLBINS[0])
    #print('***', TIMES[0])
    #print('ALLBINS[1]=', ALLBINS[1])
    #print('***', TIMES[1])

    #print('ALLBINS[31]=', ALLBINS[1])

    PARTICIPATION = computeParticipation(ALLBINS, numRanks, numBins)
    (pr, X, binData) = calcParticipation(PARTICIPATION, TIMES, numBins, logName, drawPlots)
    #print(PARTICIPATION)
    return (pr, X, binData)


def gatherParticipation(outputDir, data, numRanks, steps, numBins) :
    runs = GET_RUNS(outputDir, data, rankSel=numRanks, stepSel=None )
    participationResults = []
    # show each what runs are parsed
    print(runs)

    # the step is x axis
    # the rank participatio is y axis
    for run in runs :
        (pr, X, binData) = parseAndPlotParticipation(outputDir, run,  numRanks, numBins, False)
        participationResults.append((run, pr, X,binData))
    
    
    results = []
    binData = []
    for s in steps :
        for pr in participationResults :
            if '_s%d'%s in pr[0] :
                results.append((pr[1], pr[2], pr[3])) ## PR, X, BinData
                break
    return results
    

def parsePRRanks(outputdir, dataType, ranks, steps, numBins) :
    results = []
    # go through each rank and append results
    for rank in ranks :
        print('parse: ', dataType, 'rank=', rank)
        pr_x_bins = gatherParticipation(outputdir, dataType, rank, steps, numBins)
        results.append(pr_x_bins)
    return results

dataNameMap = {'astro' : 'Supernova',
               'clover' : 'CloverLeaf3D',
               'fishtank' : 'Hydraulics',
               'fusion' : 'Tokamak',
               'syn' : 'Synthetic'}

labelSize = 25
tickSize = 23
lwidth=2.5
legendsize=22

def plotRPRanks(ax, dataName, allData, ranks, steps) :
    #fig, ax = plt.subplots(figsize=(6,6))
    dataTitle = dataNameMap[dataName]
    ax.title.set_text(dataTitle)
    ax.title.set_fontsize(labelSize)

    ax.set_ylim([0.0, 1.1])
    #ax.set_xlabel('Steps', fontsize=labelSize)
    #ax.set_aspect('auto')
    if dataTitle=="Tokamak":
        ax.set_ylabel('Avg rank participation', fontsize=labelSize)
    #ax.set_xscale('log')
    
    ax.tick_params(axis='y', labelsize=tickSize)
    ax.tick_params(axis='x', labelsize=tickSize)
    #print(len(allData), len(steps), len(ranks))
    print(steps)
    for (rank, data) in zip(ranks, allData) :
        #print(rank, len(data))
        X = []
        Y = []
        for (step, ds) in zip(steps, data) :
            #print(step, ds[0])
            X.append(step)
            Y.append(ds[0])
        ax.plot(X, Y, label='%d Ranks'%rank, linewidth=lwidth)
        print(rank)
        print(X)
        #ax.set_xticks(X)
        #ax.xaxis.set_major_locator(mticker.FixedLocator(X))
        #ax.xaxis.set_minor_locator(mticker.FixedLocator(X))
    #ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    
    #ax.ticklabel_format(useOffset=False, style='plain')
    #plt.ticklabel_format(useOffset=False)
    #ax.legend(loc='upper right')
    #plt.show()



if __name__ == "__main__":
    
    if len(sys.argv)!=2:
        print("<binary> <datapath>")
        exit()
    
    outputdir=sys.argv[1]
    
    STEPS = [50,100,500,1000,2000]
    #RankList=[8,16,32,64,128]
    RankList=[8,16,32,64,128]
    
    dir_name_list = ["fusion","astro","fishtank","clover","syn"]

    #TIMES, EVENTS = readTimeTrace(dirPath, numRanks)
    #print(TIMES)
    #print(EVENTS)
    NUM_BINS = 50

    fig, axs = plt.subplots(nrows=1, ncols=5,figsize=(6*5,6))

    # go through RankList
    # for each RankList, go through all steps
    # for each Rank*Step, we have one run
    # for this run, we can get one point
    for index, dataname in enumerate(dir_name_list):
        astroData = parsePRRanks(outputdir, dataname, RankList, STEPS, NUM_BINS)
        plotRPRanks(axs[index], dataname, astroData, RankList, STEPS)
    
    plt.subplots_adjust(top=0.8)

    handles, labels = axs[4].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=5, loc='upper center', fontsize=legendsize)

    fig.text(0.5, 0.0, 'Advection steps', ha='center',fontsize=labelSize+2)

    plt.savefig("rank_participation_gather_all.png",bbox_inches='tight')   
    plt.savefig("rank_participation_gather_all.pdf",bbox_inches='tight')   
