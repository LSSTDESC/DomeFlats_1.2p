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

def setup_visit(phosimdir, threads, visitdir):
    pdir = os.path.abspath(phosimdir) + '/'
    vdir = os.path.abspath(visitdir) + '/'
    rdir = vdir + rundirName + '/'
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
        f.write('python %sphosim.py \\\n' % pdir)
        f.write('%s \\\n' % (idir+flatName))
        f.write('-c %s \\\n' % (idir+cmdName))
        f.write('-s %s \\\n' % sensor)
        f.write('-w %s \\\n' % wdir)
        f.write('-o %s \\\n' % odir)
        f.write('-t %d \\\n' % threads)
        #f.write('-e 0 \\\n')
        f.write('1> %s \\\n' % stdoutName)
        f.write('2> %s\n' % stderrName)
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
        print('USAGE: %s <prefix> <phosimdir> <threads>'%sys.argv[0])
        sys.exit(-1)
    prefix = sys.argv[1]
    phosimdir = sys.argv[2]
    threads = int(sys.argv[3])
    setup_series(phosimdir, threads, prefix)
