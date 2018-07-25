import sys
import os
import os.path
import glob

flatName = 'flat'
sensorName = 'sensor_list.txt'
cmdName = 'commands.txt'
indirName = 'inputs'
workdirName = 'work'
outdirName = 'output'
rundirName = 'run'

runBase = 'run_%03d.sh'
stdoutBase = 'stdout_%s.txt'
stderrBase = 'stderr_%s.txt'

bindirName = 'bin'
datadirName = 'data'

def setup_visit(phosimdir, threads, visitdir):
    pdir = os.path.abspath(phosimdir) + '/'
    bdir = pdir + bindirName + '/'
    ddir = pdir + datadirName + '/'
    vdir = os.path.abspath(visitdir) + '/'
    rdir = vdir + rundirName + '/'
    os.symlink(pdir + 'phosim', rdir + 'phosim')
    os.symlink(pdir + 'phosim.py', rdir + 'phosim.py')
    idir = vdir + indirName + '/'
    odir = vdir + outdirName + '/'
    f = open(idir + sensorName, 'r')
    sl = f.readlines()
    f.close()
    for i in xrange(len(sl)):
        sensor = sl[i].strip()
        wdir = vdir + workdirName + '/' + sensor + '/'
        runName = (rdir + runBase)%i
        stdoutName = (odir + stdoutBase)%sensor
        stderrName = (odir + stderrBase)%sensor
        f = open(runName, 'w')
        f.write('#! /bin/bash\n')
        f.write('./phosim \\\n%s \\\n-c %s \\\n-w %s \\\n-o %s \\\n-b %s \\\n-d %s \\\n-t %d \\\n-e 0 \\\n1> %s \\\n2> %s\n' % (idir+flatName, idir+cmdName, wdir, odir, bdir, ddir, threads, stdoutName, stderrName) )
        f.close()
        os.chmod(runName,0755)
    return

def setup_series(phosimdir, threads, prefix):
    dl = glob.glob(prefix+'/5??????')
    for d in dl:
        setup_visit(phosimdir, threads, d)
    return

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('USAGE: %s <phosimdir> <threads> <prefix>'%sys.argv[0])
        sys.exit(-1)
    phosimdir = sys.argv[1]
    threads = int(sys.argv[2])
    prefix = sys.argv[3]
    setup_series(phosimdir, threads, prefix)
