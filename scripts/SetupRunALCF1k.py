import sys
import os
import os.path

rundirName = 'run'
runBase = 'run_%03d.sh'

nodeBase = 'node_%04d.sh'
submitName = 'submit.sh'

hostBase = 'host_%04d.txt'

def setup_node(outDir, visitDirList, nodeID):
    nodeName = nodeBase % nodeID
    hostName = hostBase % nodeID
    outName = outDir + '/' + nodeName
    f = open(outName, 'w')
    f.write('#! /bin/bash\n')
    f.write('cat /etc/hostname > %s\n' % hostName)
    for visitDir in visitDirList:
        vdir = os.path.abspath(visitDir) + '/'
        rdir = vdir + rundirName
        runName = runBase % nodeID
        f.write('cd %s\n'%rdir)
        f.write('./%s\n'%runName)
    f.close()
    os.chmod(outName,0755)
    return

def setup_run(allocation, queue, time, nnodes, outDir, visitDirList):
    os.makedirs(outDir)
    for i in xrange(nnodes):
        setup_node(outDir, visitDirList, i)
    outName = outDir + '/' + submitName
    f = open(outName, 'w')
    f.write('#! /bin/bash\n')
    f.write('#COBALT -A %s\n' % allocation)
    f.write('#COBALT -q %s\n' % queue)
    f.write('#COBALT -t %s\n' % time)
    f.write('#COBALT -n %d\n' % nnodes)
    for i in xrange(nnodes):
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
        print('USAGE: %s <allocation> <queue> <time> <nnodes> <outDir> <visitDir1> [visitDir2] ...' % sys.argv[0])
        sys.exit(-1)
    allocation = sys.argv[1]
    queue = sys.argv[2]
    time = sys.argv[3]
    nnodes = int(sys.argv[4])
    outDir = sys.argv[5]
    visitDirList = sys.argv[6:]
    setup_run(allocation, queue, time, nnodes, outDir, visitDirList)
