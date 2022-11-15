import vtk
import os

SPACING = (4.25, 4.25, 8.25)
ORIGIN = (-.125, -.125, -.125)


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


def decompose(ds, nB, outNm) :
    numBlocks = []
    if type(nB) == int : numBlocks = [nB, nB, nB]
    else : numBlocks = nB

    blockString = '.%d_%d_%d' % (numBlocks[0], numBlocks[1], numBlocks[2])


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

def resampleDS(inDS, dims) :
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


#FILES = ['clover.0700', 'clover.2200']
FILES = ['clover_650']
#The size of each blocks
DIMS = [(33,33,66)]
#BLOCKS = [(2,2,2), (2,2,4)]
#How many blockid in each dimension
BLOCKS = [(2,2,2)]

for f in FILES :
    for d in DIMS :
        for b in BLOCKS :
            ds = readDS(f)
            r_ds = resampleDS(ds, d)
            decompose(r_ds, b, 'x_' + f)