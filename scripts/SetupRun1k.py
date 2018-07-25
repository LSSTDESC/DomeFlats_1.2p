import sys
import os
import os.path

rundirName = 'run'
runBase = 'run_%03d.sh'

nodeBase = 'node_%04d.sh'
submitName = 'submit.sh'

def setup_node(outDir, visitDirList, nodeID):
    nodeName = nodeBase % nodeID
    outName = outDir + '/' + nodeName
    f = open(outName, 'w')
    f.write('#! /bin/bash\n')
    for visitDir in visitDirList:
        vdir = os.path.abspath(visitDir) + '/'
        rdir = vdir + rundirName
        runName = runBase % nodeID
        f.write('cd %s\n'%rdir)
        f.write('./%s\n'%runName)
    f.close()
    os.chmod(outName,0755)
    return

def setup_run(outDir, visitDirList):
    os.makedirs(outDir)
    for i in xrange(189):
        setup_node(outDir, visitDirList, i)
    outName = outDir + '/' + submitName
    f = open(outName, 'w')
    f.write('#! /bin/bash\n')
    f.write('#COBALT -t 03:00:00\n')
    f.write('#COBALT -n 189\n')
    f.write('#COBALT -q default\n')
    f.write('#COBALT -A LSSTADSP_DESC\n')
    for i in xrange(189):
        nodeName = nodeBase % i
        f.write('aprun -n 1 -N 1 -d 256 -j 4 ./%s &\nsleep 1\n' % nodeName)
    f.write('wait\n')
    f.close()
    os.chmod(outName, 0755)
    return

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('USAGE: %s <outDir> <visitDir1> [visitDir2] ...\n'%sys.argv[0])
        sys.exit(-1)
    outDir = sys.argv[1]
    visitDirList = sys.argv[2:]
    setup_run(outDir, visitDirList)
