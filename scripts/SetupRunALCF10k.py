import sys
import os
import os.path

rundirName = 'run'
runBase = 'run_%03d.sh'

nodeBase = 'node_%04d.sh'
submitName = 'submit.sh'

hostBase = 'host_%04d.txt'

def setup_visit(outDir, visitDir, nnodespervisit, nodeoffset):
    for sensor in xrange(nnodespervisit):
        nodeID = nodeoffset + sensor
        nodeName = nodeBase % nodeID
        hostName = hostBase % nodeID
        outName = outDir + '/' + nodeName
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

def setup_run(allocation, queue, time, nnodespervisit, outDir, visitDirList):
    os.makedirs(outDir)
    nvisit = len(visitDirList)
    for i in xrange(nvisit):
        setup_visit(outDir, visitDirList[i], nnodespervisit, nnodespervisit*i)
    outName = outDir + '/' + submitName
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

if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('USAGE: %s <allocation> <queue> <time> <nnodespervisit=189> <outDir> <visitDir1> [visitDir2] ...' % sys.argv[0])
        sys.exit(-1)
    allocation = sys.argv[1]
    queue = sys.argv[2]
    time = sys.argv[3]
    nnodespervisit = int(sys.argv[4])
    outDir = sys.argv[5]
    visitDirList = sys.argv[6:]
    setup_run(allocation, queue, time, nnodespervisit, outDir, visitDirList)
