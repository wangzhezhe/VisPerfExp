import os, sys, random
import itertools, tempfile


bbox_min = [0,0,0]
bbox_max = [0.98, 0.98, 0.98]
clover_step_size = 0.05
syn_step_size = 0.075
astro_step_size = 0.01
fishtank_step_size = 0.001
fusion_step_size = 0.005

DATA_INFO = {}
DATA_INFO['clover'] = {'DATA_NAME' : 'clover',
                       'STEP_SIZE' : 0.05}
DATA_INFO['syn'] = {'DATA_NAME' : 'syn',
                    'STEP_SIZE' : 0.075}
DATA_INFO['astro'] = {'DATA_NAME' : 'astro',
                      'STEP_SIZE' : 0.01}
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
                   }
BOX_INFO['fusion'] = {'B'  : (bbox_min, bbox_max),
                      'B0' : ((.2, .2, .2), (.8,.8,.8)),
                      'B1' : ((.2, .2, .2), (.45,.45,.45)),
                      'B2' : ((.2, .2, .2), (.3,.3,.3)),
                      'B3' : ((.2, .2, .2), (.25,.25,.25)),
                      'L'  : ((.2, .2, .1), (.2,.2,.9)),
                      'P'  : ((.7, .6, .1), (.9,.6,.9)),
                      }
BOX_INFO['astro'] = {'B'  : (bbox_min, bbox_max),
                      'B0' : ((.2, .2, .2), (.8,.8,.8)),
                      'B1' : ((.40, .40, .40), (.65,.65,.65)),
                      'B2' : ((.45, .45, .45), (.55,.55,.55)),
                      'B3' : ((.1, .47, .47), (.15,.52,.52)),
                      'L'  : ((.1, .5, .5), (.9,.5,.5)),
                      'P'  : ((.1, .5, .1), (.9,.5,.9)),
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
OUT_DIR = './weak-weak-output'
DATA_DIR = '../visit_files'
DATA_DIR = '../resample'

BLOCKS_NODES = {
             32 :  [1, 2, 4, 8, 16],
             64 :  [2, 4, 8, 16, 32],
             128 : [4, 8, 16, 32, 64],
##             256 : [16,32,64,128],
             }


CMD = \
'../visitReaderAdev ' \
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
'--assign-strategy=roundroubin '

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

def MakeLaunch(numNodes, numBlocks) :
    if numBlocks == 32 :
        if numNodes == 1 :   return 'jsrun -n2 -r2 -a16 -c16 -g0 -bpacked:1'
        elif numNodes == 2 : return 'jsrun -n4 -r2 -a8 -c8 -g0 -bpacked:1'
        elif numNodes == 4 : return 'jsrun -n8 -r2 -a4 -c4 -g0 -bpacked:1'
        elif numNodes == 8 : return 'jsrun -n16 -r2 -a2 -c2 -g0 -bpacked:1'
        elif numNodes == 16 : return 'jsrun -n32 -r2 -a1 -c1 -g0 -bpacked:1'                        
    elif numBlocks == 64 :
        if numNodes == 2 :    return 'jsrun -n4 -r2 -a16 -c16 -g0 -bpacked:1'
        elif numNodes == 4 :  return 'jsrun -n8 -r2 -a8 -c8 -g0 -bpacked:1'
        elif numNodes == 8 :  return 'jsrun -n16 -r2 -a4 -c4 -g0 -bpacked:1'
        elif numNodes == 16 : return 'jsrun -n32 -r2 -a2 -c2 -g0 -bpacked:1'
        elif numNodes == 32 : return 'jsrun -n64 -r2 -a1 -c1 -g0 -bpacked:1'
    elif numBlocks == 128 :
         if numNodes == 4 :    return 'jsrun -n8 -r2 -a16 -c16 -g0 -bpacked:1'
         elif numNodes == 8 :  return 'jsrun -n16 -r2 -a8 -c8 -g0 -bpacked:1'
         elif numNodes == 16 : return 'jsrun -n32 -r2 -a4 -c4 -g0 -bpacked:1'
         elif numNodes == 32 : return 'jsrun -n64 -r2 -a2 -c2 -g0 -bpacked:1'
         elif numNodes == 64 : return 'jsrun -n128 -r2 -a1 -c1 -g0 -bpacked:1'
    elif numBlocks == 256 :
         if numNodes == 8 :  return 'jsrun -n16 -r2 -a16 -c16 -g0 -bpacked:1'
         elif numNodes == 16 : return 'jsrun -n32 -r2 -a8 -c8 -g0 -bpacked:1'
         elif numNodes == 32 : return 'jsrun -n64 -r2 -a4 -c4 -g0 -bpacked:1'
         elif numNodes == 64 : return 'jsrun -n128 -r2 -a2 -c2 -g0 -bpacked:1'
         elif numNodes == 128 : return 'jsrun -n256 -r2 -a1 -c1 -g0 -bpacked:1'
         
    raise('Unsupported launch configuration: numBlocks/numNodes= ', numBlocks, numNodes)

def writeToBSUB(cmd, numBlocks, numNodes) :
    fName = BSUB_FILES[numNodes]
    if not os.path.exists(fName) :
        f = open(fName, 'w')
        f.write(makeHeader(numNodes))
    else:
        f = open(fName, 'a')

    f.write('\n\n')
    f.write('%s\n' % cmd[1])
    f.write('%s %s\n' % (MakeLaunch(numNodes, numBlocks), cmd[0]))
    f.write('%s\n' % cmd[2])
    f.close()

def BlockString(numBlocks) :
    blockString = ''
    if numBlocks == 32 : blockString = '2_4_4'
    elif numBlocks == 64 : blockString = '4_4_4'
    elif numBlocks == 128 : blockString = '4_4_8'
    elif numBlocks == 256 : blockString = '4_8_8'
    elif numBlocks == 512 : blockString = '8_8_8'
    return blockString

def OutputDir(dataName, numBlocks, numNodes, numP, numS, box) :
    blockString = BlockString(numBlocks)
    return '%s/%s.%s.n%d.%s_p%d_s%d' % (OUT_DIR, dataName, blockString, numNodes, box, numP, numS)


def makeRunCmd(dataDir, dataNm, numBlocks, numP, numS, seedBox, outputDir) :
    blockString = BlockString(numBlocks)
    dataSet = '%s/%s.%s.visit' % (dataDir, DATA_INFO[dataNm]['DATA_NAME'], blockString)
    cmd = CMD % (dataSet, numS, numP,  ####numP*numBlocks,
                 seedBox[0][0], seedBox[1][0],
                 seedBox[0][1], seedBox[1][1],
                 seedBox[0][2], seedBox[1][2],
                 DATA_INFO[dataNm]['STEP_SIZE'])

    tmpDir = tempfile.mkdtemp(dir='./')
    mkdirCmd = 'mkdir %s; cd %s' % (outputDir, tmpDir)
    mvCmd = 'mv *.out ../%s; cd ..; rmdir %s' % (outputDir, tmpDir)
    return (cmd, mkdirCmd, mvCmd)


PARTICLE_LIST = [10000]
#PARTICLE_LIST = [5000]
PARTICLE_LIST = [1000]
STEP_LIST = [1000]

def makeHeader(numNodes) :
    hdr = ''
    hdr += '#BSUB -P csc143\n'
    hdr += '#BSUB -W 1:00\n'
    hdr += '#BSUB -nnodes %d\n' % numNodes
    hdr += '#BSUB -J run_%d\n' % numNodes
    hdr += '#BSUB -o run_%d' % numNodes + '.%J.out\n'
    hdr += '#BSUB -e run_%d' % numNodes + '.%J.err\n'
    hdr += '\n\n'
    hdr += 'export OMP_NUM_THREADS=1\n'

    return hdr


############
def createRuns(dataSelect=None, boxSelect=None) :
    clearBSUB()

    if dataSelect == None : dataSelect = list(DATA_INFO.keys())
    if boxSelect == None : boxSelect = list(BOX_INFO[dataSelect[0]].keys())

    blockSelect = BLOCKS_NODES.keys()

    for numBlocks in blockSelect :
        for numNodes in BLOCKS_NODES[numBlocks] :
            for (ds,b,p,s) in itertools.product(dataSelect, boxSelect, PARTICLE_LIST, STEP_LIST) :
                outDir = OutputDir(ds, numBlocks, numNodes, p, s, b)
                if os.path.exists(outDir) and len(os.listdir(outDir)) > 0 :
                    print('skipping %s'%outDir)
                    continue
                    
                runCmd = makeRunCmd(DATA_DIR, ds, numBlocks, p, s, BOX_INFO[ds][b], outDir)
                writeToBSUB(runCmd, numBlocks, numNodes)


#createRuns(['clover', 'fusion'])
createRuns(['clover', 'fishtank', 'fusion', 'astro'], 'B')

sys.exit()

