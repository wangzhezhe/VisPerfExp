# This file is created by David Pugmire

import os, sys, random
import itertools, tempfile

bbox_min = [0.01,0.01,0.01]
bbox_max = [0.99, 0.99, 0.99]
clover_step_size = 0.05
syn_step_size = 0.0005
syn_step_size = 0.005
astro_step_size = 0.005
fishtank_step_size = 0.001
fusion_step_size = 0.005

DATA_INFO = {}
DATA_INFO['clover'] = {'DATA_NAME' : 'clover',
#                       'STEP_SIZE' : 0.05}
                       'STEP_SIZE' : 0.01}                       
DATA_INFO['syn'] = {'DATA_NAME' : 'syn',
                    'STEP_SIZE' : 0.0005}
                    #'STEP_SIZE' : 0.0005}
DATA_INFO['astro'] = {'DATA_NAME' : 'astro',
#                      'STEP_SIZE' : 0.01}
                      'STEP_SIZE' : 0.005}
DATA_INFO['fusion'] = {'DATA_NAME' : 'fusion',
                       'STEP_SIZE' : 0.005}
DATA_INFO['fishtank'] = {'DATA_NAME' : 'fishtank',
                         'STEP_SIZE' : 0.001}
BOX_INFO = {}
BOX_INFO['clover'] = {'B'  : (bbox_min, bbox_max),
                      'B0' : ((1,1,2), (3,3,6)),
                      'B1' : ((1.5,1.5,4), (2.5, 2.5,5)),
                      'B2' : ((2,2,5), (2.4,2.4,5.8)),
                      'B3' : ((2,2,5), (2.2,2.2,5.4)),
                      'L'  : ((2.1,2.1,1), (2.1,2.1,7)),
                      'P'  : ((1,1,5), (3,3,5)),
                      }
BOX_INFO['syn'] = {'B'  : (bbox_min, bbox_max),
                   'B0' : ((25,25,25), (75,75,75)),
                   'B1' : ((20,15,15), (45,40,40)),
                   'B2' : ((15,15,15), (25,25,25)),
                   'B3' : ((15,15,15), (20,20,20)),
                   'L'  : ((70,70,10), (70,70,90)),
                   'P'  : ((70,70,10), (90,70,90)),
                   'G' : ((0.55, 0.55, 0.2), (0.55, 0.55, 0.2)),
                   'H' : ((0.55, 0.55, 0.2), (0.55, 0.55, 0.2)),                   
                   }
BOX_INFO['fusion'] = {'B'  : (bbox_min, bbox_max),
                      'B0' : ((.2, .2, .2), (.8,.8,.8)),
                      'B1' : ((.2, .2, .2), (.45,.45,.45)),
                      'B2' : ((.2, .2, .2), (.3,.3,.3)),
                      'B3' : ((.2, .2, .2), (.25,.25,.25)),
                      'L'  : ((.2, .2, .1), (.2,.2,.9)),
                      'P'  : ((.7, .6, .1), (.9,.6,.9)),
                      }
# The B means the whole bounding box
# The B0 B1 B2 B3 means the selected smaller bounding box
# The L means the line of the bbx
# Th P means the plane of the bbx
# The A and C means the specific position of the particle we want to trace
# One is the particle with the longest execution time
# Another one is the particle with the highest number of block traversing
BOX_INFO['astro'] = {'B'  : (bbox_min, bbox_max),
                      'B0' : ((.2, .2, .2), (.8,.8,.8)),
                      'B1' : ((.40, .40, .40), (.65,.65,.65)),
                      'B2' : ((.45, .45, .45), (.55,.55,.55)),
                      'B3' : ((.1, .47, .47), (.15,.52,.52)),
                      'L'  : ((.1, .5, .5), (.9,.5,.5)),
                      'P'  : ((.1, .5, .1), (.9,.5,.9)),
                      'A'  : ((0.560722,0.534309,0.475521), (0.560722,0.534309,0.475521)), ##long particle, long life
                      'C'  : ((0.352697,0.501353,0.47291),(0.352697,0.501353,0.47291)), ##long particle, short life
                      }
BOX_INFO['fishtank'] = {'B'  : (bbox_min, bbox_max),
                        'B0' : ((.2, .2, .4), (.7,.7,.9)),
                        'B1' : ((.35, .35, .5), (.7,.7,.75)),
                        'B2' : ((.4, .4, .7), (.5, .5,.8)),
                        'B3' : ((.65, .45, .01), (.7,.5,.05)),
                        'L'  : ((.65, .65, .05), (.65,.65,.95)),
                        'P'  : ((.1, .1, .5), (.9,.9,.5)),
                        }

checkIfRun = True
OUT_DIR = './trophyData'
OUT_DIR = './trophyDataWithGetActive'
OUT_DIR = './weak-weak-output2'
DATA_DIR = '../visit_files'
#DATA_DIR = '../resample2'
DATA_DIR='/gpfs/alpine/csc143/proj-shared/pugmire/forJay/VisPerfExp/ubuntu_cpu_vtkm2.0/runDIR/resample2'

# blocks : [(nodes, ranks), ...]
INSITU_BLOCKS = {
 8 : [(1, 8)],
 16 : [(1, 16)],
 32 : [(1, 32)],
 64 : [(2, 64)],
 128 : [(4, 128)],
 256 : [(8, 256)],
 512 : [(16, 512)], 
 }

#blocks : [(nodes, rank), ...]
INTRANSIT_BLOCKS = {
#32 : [(1,16), (1,8)],
#64 : [(1,32), (1,16), (1,8)],
128 : [(2,64), (1,32), (1,16)],
}

BLOCKS_NODES = {
             32 :  [1, 2, 4, 8, 16],
             64 :  [2, 4, 8, 16, 32],
             128 : [4, 8, 16, 32, 64],
             256 : [16,32,64,128],
             }
INTRANSIT_BLOCKS_NODES = {
             64 :  [1],
             128 : [1,2],
             256 : [1,2,4,8],
             256 : [1,2,4,8,16],             
             }             


CMD = \
'../visitReaderAdev ' \
'--vtkm-device serial ' \
'--file=%s ' \
'--advect-num-steps=%d ' \
'--advect-num-seeds=%d ' \
'--seeding-method=domainrandom ' \
'--advect-seed-box-extents=%f,%f,%f,%f,%f,%f ' \
'--field-name=velocity ' \
'--advect-step-size=%f ' \
'--record-trajectories=false ' \
'--output-results=false ' \
'--sim-code=cloverleaf ' \
'--assign-strategy=roundroubin ' \
'--communication=%s &> readerlog.out'

CMD_GANG = \
'../visitReaderAdev ' \
'--file=%s ' \
'--advect-num-steps=%d ' \
'--advect-num-seeds=%d ' \
'--seeding-method=boxrandom ' \
'--advect-seed-box-extents=%f,%f,%f,%f,%f,%f ' \
'--field-name=velocity ' \
'--advect-step-size=%f ' \
'--record-trajectories=false ' \
'--output-results=false ' \
'--sim-code=cloverleaf ' \
'--assign-strategy=roundroubin ' \
'--communication=%s &> readerlog.out'

#'--random-seed=%d '
#'--output-results=true ' \
#'--seeding-method=boxsample ' \
#'--seeding-sample=10,10,20 ' \


BSUB_FILES = {1 : 'run1.bsub',
              2 : 'run2.bsub',
              4 : 'run4.bsub',
              8 : 'run8.bsub',
              16 : 'run16.bsub',
              32 : 'run32.bsub',
              64 : 'run64.bsub',
              128 : 'run128.bsub',
              256 : 'run256.bsub',                            
              }

def clearBSUB() :
    for f in BSUB_FILES.values() :
        if os.path.exists(f) : os.system('rm %s' % f)

#2 nodes, 16 tasks per socket: jsrun -n
#n4 4 nodes         
#r2 2 resources per node
#a16 16 MPI tasks (c21 take all cpus and asign 1 core to MPI)

def MakeLaunch(numNodes, numRanks) :

  ## (numRanks, numNodes) : 'jsrun ....'
  launchMap = {}
  launchMap[(8,1)]  = 'jsrun -n2 -r2 -a4 -c4 -g1 -bpacked:1'
  launchMap[(16,1)]  = 'jsrun -n2 -r2 -a8 -c8 -g1 -bpacked:1'
  launchMap[(32,1)]  = 'jsrun -n2 -r2 -a16 -c16 -g1 -bpacked:1'
  launchMap[(32,2)]  = 'jsrun -n4 -r2 -a8 -c8 -g1 -bpacked:1'
  launchMap[(32,4)]  = 'jsrun -n8 -r2 -a4 -c4 -g1 -bpacked:1'
  launchMap[(32,8)]  = 'jsrun -n16 -r2 -a2 -c2 -g1 -bpacked:1'
  launchMap[(32,16)] = 'jsrun -n32 -r2 -a1 -c1 -g1 -bpacked:1'

  launchMap[(64,2)]  = 'jsrun -n4 -r2 -a16 -c16 -g1 -bpacked:1'
  launchMap[(64,4)]  = 'jsrun -n8 -r2 -a8 -c8 -g1 -bpacked:1'
  launchMap[(64,8)]  = 'jsrun -n16 -r2 -a4 -c4 -g1 -bpacked:1'
  launchMap[(64,16)] = 'jsrun -n32 -r2 -a2 -c2 -g1 -bpacked:1'
  launchMap[(64,32)] = 'jsrun -n64 -r2 -a1 -c1 -g1 -bpacked:1'

  launchMap[(128,4)] = 'jsrun -n8 -r2 -a16 -c16 -g1 -bpacked:1'
  launchMap[(128,8)] = 'jsrun -n16 -r2 -a8 -c8 -g1 -bpacked:1'
  launchMap[(128,16)] = 'jsrun -n32 -r2 -a4 -c4 -g1 -bpacked:1'
  launchMap[(128,32)] = 'jsrun -n64 -r2 -a2 -c2 -g1 -bpacked:1'
  launchMap[(128,64)] = 'jsrun -n128 -r2 -a1 -c1 -g1 -bpacked:1'

  launchMap[(256,8)] = 'jsrun -n16 -r2 -a16 -c16 -g1 -bpacked:1'
  launchMap[(256,16)] = 'jsrun -n32 -r2 -a8 -c8 -g1 -bpacked:1'
  launchMap[(256,32)] = 'jsrun -n64 -r2 -a4 -c4 -g1 -bpacked:1'
  launchMap[(256,64)] = 'jsrun -n128 -r2 -a2 -c2 -g1 -bpacked:1'
  launchMap[(256,128)] = 'jsrun -n256 -r2 -a1 -c1 -g1 -bpacked:1'

  launchMap[(512,16)] = 'jsrun -n32 -r2 -a16 -c16 -g1 -bpacked:1'

  return launchMap[(numRanks, numNodes)]

def writeToBSUB(cmd, numBlocks, numNodes, numRanks) :
    fName = BSUB_FILES[numNodes]
    if not os.path.exists(fName) :
        f = open(fName, 'w')
        f.write(makeHeader(numNodes))
    else:
        f = open(fName, 'a')

    f.write('\n\n')
    f.write('%s\n' % cmd[1])
    f.write('%s %s\n' % (MakeLaunch(numNodes, numRanks), cmd[0]))
    f.write('%s\n' % cmd[2])
    f.close()

def BlockString(numBlocks, dataNm) :
    blockString = ''
    if numBlocks == 8 : blockString = '2_2_2'
    elif numBlocks == 16 : blockString = '2_2_4'
    elif numBlocks == 32 : blockString = '2_4_4'
    elif numBlocks == 64 :
      if   dataNm == 'syn2' : blockString = blockString = '2_2_16'
      elif dataNm == 'syn3' : blockString = blockString = '1_2_32'
      elif dataNm == 'syn4' : blockString = blockString = '8_8_1'
      elif dataNm == 'syn5' : blockString = blockString = '1_1_64'            
      else : blockString = '4_4_4'
    elif numBlocks == 128 : blockString = '4_4_8'
    elif numBlocks == 256 : blockString = '4_8_8'
    elif numBlocks == 512 : blockString = '8_8_8'
    return blockString

def OutputDir(dataName, numBlocks, numNodes, numRanks, numP, numS, box, syncComm, pid) :
    syncStr = 'A'
    if syncComm : syncStr = 'S'
    if pid == -1 : return '%s/%s.%s.b%d.n%d.r%d.%s_p%d_s%d' % (OUT_DIR, dataName, syncStr, numBlocks, numNodes, numRanks, box, numP, numS)
    else : return '%s/%s.%s.b%d.n%d.r%d.%s_p%d_s%d_id%d' % (OUT_DIR, dataName, syncStr, numBlocks, numNodes, numRanks, box, numP, numS, pid)

def makeRunCmd(dataDir, dataNm, numBlocks, syncComm, numP, numS, seedBox, outputDir, pid=-1) :
    blockString = BlockString(numBlocks, dataNm)
    syncCommStr = 'async'
    if syncComm : syncCommStr = 'sync'
    dataSet = '%s/%s.%s.visit' % (dataDir, DATA_INFO[dataNm]['DATA_NAME'], blockString)
    CMD_ = CMD
    if doGang : CMD_ = CMD_GANG
    cmd = CMD_ % (dataSet, numS, numP,  ####numP*numBlocks,
                 seedBox[0][0], seedBox[1][0],
                 seedBox[0][1], seedBox[1][1],
                 seedBox[0][2], seedBox[1][2],
                 DATA_INFO[dataNm]['STEP_SIZE'],
                 syncCommStr)
    if pid >= 0 : cmd = cmd + ' --trace_particle_id=%d ' % pid

    tmpDir = tempfile.mkdtemp(dir='./')
    mkdirCmd = 'mkdir -p %s; mkdir -p %s; cd %s' % (outputDir, tmpDir, tmpDir)
    #mvCmd = 'mv *.out *.vtk ../%s; cd ..; rmdir %s' % (outputDir, tmpDir)
    mvCmd = 'mv *.out ../%s; cd ..; rmdir %s' % (outputDir, tmpDir)
    return (cmd, mkdirCmd, mvCmd)


PARTICLE_LIST = [10000]
PARTICLE_LIST = [5000]
#PARTICLE_LIST = [2500, 5000]
#PARTICLE_LIST = [1000]
#STEP_LIST = [50, 100, 500, 1000, 2000]
STEP_LIST = [1000]
#STEP_LIST = [250]
#STEP_LIST = [101]
#PARTICLE_LIST=[101]
PID = -1

doGang = False
if doGang :
   DATA_INFO['syn2'] = DATA_INFO['syn']
   DATA_INFO['syn3'] = DATA_INFO['syn']
   DATA_INFO['syn4'] = DATA_INFO['syn']
   DATA_INFO['syn5'] = DATA_INFO['syn']         
   BOX_INFO['syn2'] = BOX_INFO['syn']
   BOX_INFO['syn3'] = BOX_INFO['syn']
   BOX_INFO['syn4'] = BOX_INFO['syn']
   BOX_INFO['syn5'] = BOX_INFO['syn']         
   PARTICLE_LIST=[1, 10, 100, 1000, 10000]
   STEP_LIST=[1000,2000,4000, 500]
   
#doPID = ''
doPID = 'astro'

if doPID == 'astro' :
  ## astro 128 blocks, 1000 steps
  PID = 45715 ## longest, Box=A
  #PID = 255124   ## early longers, Box=C
  STEP_LIST = [1000]
  #PARTICLE_LIST=[1]
elif doPID == 'clover' :
  ## clover 128, 1000 steps
  PID = 278131
  STEP_LIST = [1000]
elif doPID == 'fishtank' :
  ## fishtank 128, 1000 steps
  PID = 463815
  STEP_LIST = [1000]
elif doPID == 'fusion' :
  ## fusion 128, 1000 steps
  PID = 543021
  STEP_LIST = [1000]


def makeHeader(numNodes) :
    hdr = ''
    hdr += '#BSUB -P csc143\n'
    hdr += '#BSUB -W 1:00\n'
    hdr += '#BSUB -nnodes %d\n' % numNodes
    hdr += '#BSUB -J run_%d\n' % numNodes
    hdr += '#BSUB -o run_%d' % numNodes + '.%J.out\n'
    hdr += '#BSUB -e run_%d' % numNodes + '.%J.err\n'
    hdr += '##BSUB -q debug\n'
    hdr += '\n\n'
    hdr += 'CURRDIR=$(pwd)\n'
    hdr += 'export OMP_NUM_THREADS=1\n'
    hdr += 'cd $MEMBERWORK/csc143\n'
    hdr += 'rm visitReaderAdev\n'
    hdr += 'ln -s $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev'
    
    return hdr


############
def createRuns(BN, syncComm, dataSelect=None, boxSelect=None, checkExists=True) :
    if dataSelect == None : dataSelect = list(DATA_INFO.keys())
    if boxSelect == None : boxSelect = list(BOX_INFO[dataSelect[0]].keys())

    for b in BN.keys() :
      for (N,R) in BN[b] :
        print(b, '-->', (N,R))
    print('SYNC=', syncComm)

    for numBlocks in BN.keys() :
      for (numNodes, numRanks) in BN[numBlocks] :
        for (ds,b,p,s) in itertools.product(dataSelect, boxSelect, PARTICLE_LIST, STEP_LIST) :
          outDir = OutputDir(ds, numBlocks, numNodes, numRanks, p, s, b, syncComm, PID)
          print(outDir)
          if checkExists and os.path.exists(outDir) and len(os.listdir(outDir)) > 0 :
            print('skipping %s'%outDir)
            continue

          runCmd = makeRunCmd(DATA_DIR, ds, numBlocks, syncComm, p, s, BOX_INFO[ds][b], outDir, PID)
          writeToBSUB(runCmd, numBlocks, numNodes, numRanks)


clearBSUB()

doWeakScaling = True

if doWeakScaling :
   OUT_DIR = './weak-weak-output2'

   #INTRANSIT_BLOCKS_NODES
   #INSITU_BLOCKS_NODES
   for syncComm in [False] :
    if PID >= 0 : createRuns(INSITU_BLOCKS, syncComm, [doPID], 'C')
    elif doGang : createRuns(INSITU_BLOCKS, syncComm, ['syn', 'syn2', 'syn3', 'syn4', 'syn5'], 'G', checkExists=False)
    else : createRuns(INSITU_BLOCKS, syncComm, ['astro'], 'B', False)
    #createRuns(INSITU_BLOCKS, syncComm, ['clover', 'fishtank', 'fusion', 'astro'], 'B')
else :
  OUT_DIR = './strong-output'
  syncComm = False
  #INTRANSIT_BLOCKS_NODES
  for syncComm in [False] :
    createRuns(INTRANSIT_BLOCKS, syncComm, ['astro', 'clover', 'fishtank', 'fusion', 'syn'], 'B')


sys.exit()