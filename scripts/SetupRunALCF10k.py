import sys
import os
import os.path
import glob

rundirName = 'run'
runBase = 'run_%03d.sh'

nodeBase = 'node_%04d.sh'
submitName = 'submit.sh'

hostBase = 'host_%04d.txt'

batchDirBase = 'batch_%04d'

def setup_visit(batchDir, visitDir, nnodespervisit, nodeoffset):
    for sensor in xrange(nnodespervisit):
        nodeID = nodeoffset + sensor
        nodeName = nodeBase % nodeID
        hostName = hostBase % nodeID
        outName = batchDir + '/' + nodeName
        f = open(outName, 'w')
        f.write('#! /bin/bash\n')
        f.write('cat /etc/hostname > %s\n' % hostName)
        vdir = os.path.abspath(visitDir) + '/'
        rdir = vdir + rundirName
        runName = runBase % sensor
        f.write('cd %s\n'%rdir)
        f.write('./%s\n'%runName)
        f.close()
        os.chmod(outName,0755)
    return

def setup_batch(allocation, queue, time, nnodespervisit, batchDir, visitDirList):
    os.makedirs(batchDir)
    nvisit = len(visitDirList)
    for i in xrange(nvisit):
        setup_visit(batchDir, visitDirList[i], nnodespervisit, nnodespervisit*i)
    outName = batchDir + '/' + submitName
    f = open(outName, 'w')
    f.write('#! /bin/bash\n')
    f.write('#COBALT -A %s\n' % allocation)
    f.write('#COBALT -q %s\n' % queue)
    f.write('#COBALT -t %s\n' % time)
    f.write('#COBALT -n %d\n' % (nnodespervisit*nvisit))
    for i in xrange(nnodespervisit*nvisit):
        nodeName = nodeBase % i
        f.write('date\n')
        f.write('aprun -n 1 -N 1 -d 256 -j 4 ./%s &\n' % nodeName)
        f.write('sleep 1\n')
    f.write('wait\n')
    f.write('date\n')
    f.close()
    os.chmod(outName, 0755)
    return

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def setup_all(prefix, chunksize, nnodespervisit, allocation, queue, time):
    visitDirList = glob.glob(prefix+'/5??????')
    batchID = 0
    for chunk in chunks(visitDirList, chunksize):
        batchDir = prefix + '/' + (batchDirBase % batchID)
        setup_batch(allocation, queue, time, nnodespervisit, batchDir, chunk)
        batchID += 1
    return

if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('USAGE: %s <prefix> <chunksize> <nnodespervisit=189> <allocation> <queue> <time>' % sys.argv[0])
        sys.exit(-1)
    prefix = sys.argv[1]
    chunksize = int(sys.argv[2])
    nnodespervisit = int(sys.argv[3])
    allocation = sys.argv[4]
    queue = sys.argv[5]
    time = sys.argv[6]
    setup_all(prefix, chunksize, nnodespervisit, allocation, queue, time)
