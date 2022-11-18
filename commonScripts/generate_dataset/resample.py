import vtk
import os

SPACING = (99,99,99)
ORIGIN = (0,0,0)


def writeDS(fname, ds) :
    writer = vtk.vtkDataSetWriter()
    writer.SetFileVersion(4)
    #writer.SetFileTypeToASCII()
    writer.SetFileTypeToBinary()
    writer.SetFileName(fname)
    writer.SetInputData(ds)
    writer.Update()
    writer.Write()

def readDS(fname) :
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(fname + '.vtk')
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()
    ds = reader.GetOutput()
    return ds


def decompose(ds, nB, outNm, bsize) :
    numBlocks = []
    if type(nB) == int : numBlocks = [nB, nB, nB]
    else : numBlocks = nB

    blockString = '.%d_%d_%d.%d_%d_%d' % (numBlocks[0], numBlocks[1], numBlocks[2], bsize[0], bsize[1], bsize[2])


    outNm = outNm + blockString
    print('******************** ', outNm)
    os.system('mkdir %s' % outNm)

    ptDims = ds.GetDimensions()
    cellDims = (ptDims[0]-1, ptDims[1]-1, ptDims[2]-1)
    print(cellDims)
    dX = int(cellDims[0] / numBlocks[0])
    dY = int(cellDims[1] / numBlocks[1])
    dZ = int(cellDims[2] / numBlocks[2])

    x0,y0,z0 = (0,0,0)
    x1,y1,z1 = (dX, dY, dZ)
    print('dXYZ= ', dX, dY, dZ)
    cnt = 0
    fnames = []
    for i in range(numBlocks[0]) :
        for j in range(numBlocks[1]) :
            for k in range(numBlocks[2]) :
                x0 = i * dX
                x1 = x0 + dX
                y0 = j * dY
                y1 = y0 + dY
                z0 = k * dZ
                z1 = z0 + dZ
                print((i,j,k), (x0,x1), (y0,y1), (z0,z1))

                eg = vtk.vtkExtractVOI()
                voi = (x0,x1, y0,y1, z0,z1)
                eg.SetVOI(voi)
                eg.SetSampleRate(1,1,1)
                eg.SetInputData(ds)
                eg.Update()
                out = eg.GetOutput()
                blockNm = '%s/output.%03d.vtk'%(outNm, cnt)
                writeDS(blockNm, out)
                fnames.append(blockNm)
                cnt = cnt+1
    #make .visit file
    f = open('%s.visit' % outNm, 'w')
    f.write('!NBLOCKS %d\n' % cnt)
    for x in fnames :
        f.write(x + '\n')
    f.close()

def resampleDS(ds, dims) :
    nx = dims[0]
    ny = dims[1]
    nz = dims[2]
    dx = SPACING[0] / (nx-1.0)
    dy = SPACING[1] / (ny-1.0)
    dz = SPACING[2] / (nz-1.0)

    ugrid = vtk.vtkUniformGrid()
    ugrid.SetOrigin(ORIGIN)
    ugrid.SetDimensions(nx, ny, nz)
    ugrid.SetSpacing(dx, dy, dz)
    #writeDS('ugrid.vtk', ugrid)

    #sample SOURCE onto input
    resamp = vtk.vtkProbeFilter()
    resamp.SetSourceData(ds)
    resamp.SetInputData(ugrid)
    resamp.Update()

    return resamp.GetOutput()


#FILES = ['cloverleafRaw_128_128_256.640']
FILES = ['sample_image_100_100_100WithVarVector']
#DIMS = [(33,33,66)]
#BLOCKS = [(2,2,2), (2,2,4)]

BLOCKS = [(4,4,4)]
BLOCK_SIZE_LIST = [(32,32,32)]

'''
for f in FILES :
    for d in DIMS :
        for b in BLOCKS :
            ds = readDS(f)
            r_ds = resampleDS(ds, d)
            decompose(r_ds, b, 'x_' + f)
'''

for f in FILES :
    for b in BLOCKS :
        for BLOCK_SIZE in BLOCK_SIZE_LIST :
            print(b)
            print(BLOCK_SIZE)
            d = [BLOCK_SIZE[0] * b[0], BLOCK_SIZE[1] * b[1], BLOCK_SIZE[2] * b[2]]
            print ("total dims:",d)
            ds = readDS(f)
            r_ds = resampleDS(ds, d)
            outF = 'x_' + f
            print('writing to: ', outF)
            decompose(r_ds, b, outF, BLOCK_SIZE)
