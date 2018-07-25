from numpy.random import seed, rand
import os
import shutil
import sys

obshistid0 = 5000000
obshistidf =  100000

flatName = 'flat'
sensorName = 'sensor_list.txt'
cmdName = 'commands.txt'
indirName = 'inputs'
workdirName = 'work'
outdirName = 'output'
rundirName = 'run'

base_required = {'minsource' : 0, 'telconfig' : 2, 'nsnap' : 1, 'domewave' : 0.0, 'domeint' : 18.0}

mjd = 59580
base_optional = {'mjd' : mjd, 'raydensity' : 0.0, 'rotationjitter' : 0.0, 'elevationjitter' : 0.0, 'azimuthjitter' : 0.0}
# windjitter?
# shuttererror?

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

# write dictionary to instance catalogs, command files, etc
def dict2catalog(d, outName):
    f = open(outName,'w')
    for i in d.keys():
        f.write(('%s %s\n'%(i,str(d[i]))))
    f.close()
    return

# determine exposure time for e-/pixel in a filter
def ic_counts(band, counts):
    # exposure times for 1k e-/pixel in each band
    # for domeint=18.0 and domewav=0.0
    # experimentally determine with phosim v3.7.15
    t1k = [7.9322, 2.1562, 2.2765, 2.8111, 3.5504, 5.3525]
    vistime = 1.0*t1k[band]*counts/1000.0
    d = {}
    d['vistime'] = vistime
    d['filter'] = band
    return d

# seed from obshistid, draw random angle for telescope rotation
def ic_randoms(obshistid):
    d = {}
    d['obshistid'] = obshistid
    s = int(obshistid)
    d['seed'] = s
    seed(s)
    angle = 360.0*rand()
    d['rottelpos'] = angle
    return d

def ic(obshistid, band, counts, outName):
    d_randoms = ic_randoms(obshistid)
    d_counts = ic_counts(band, counts)
    d = merge_dicts(base_required, d_counts, d_randoms, base_optional)
    dict2catalog(d, outName)
    return

def setup_visit(prefix, sensorFile, cmdFile, band, counts, obshistid):
    topdir = prefix + '/' + str(int(obshistid)) + '/'
    os.makedirs(topdir)
    indir = topdir + '/' + indirName + '/'
    os.makedirs(indir)
    shutil.copy(cmdFile, indir + cmdName)
    shutil.copy(sensorFile, indir + sensorName)
    ic(obshistid, band, counts, indir + flatName)
    workdir = topdir + '/' + workdirName + '/'
    os.makedirs(workdir)
    f = open(sensorFile,'r')
    sl = f.readlines()
    f.close()
    for s in sl:
        os.makedirs(workdir + s.strip())
    outdir = topdir + '/' + outdirName + '/'
    os.makedirs(outdir)
    rundir = topdir + '/' + rundirName + '/'
    os.makedirs(rundir)
    return

def setup_series(prefix, sensorFile, cmdFile, band, counts, offset, n):
    for i in xrange(n):
        obshistid = obshistid0 + band*obshistidf + offset + i
        setup_visit(prefix, sensorFile, cmdFile, band, counts, obshistid)
    return

if __name__ == '__main__':
    if len(sys.argv) < 8:
        print('USAGE: %s <prefix> <sensorFile> <cmdFile> <band> <counts> <offset> <n>'%sys.argv[0])
        sys.exit(-1)
    prefix = sys.argv[1]
    sensorFile = sys.argv[2]
    cmdFile = sys.argv[3]
    band = int(sys.argv[4])
    counts = float(sys.argv[5])
    offset = int(sys.argv[6])
    n = int(sys.argv[7])
    setup_series(prefix, sensorFile, cmdFile, band, counts, offset, n)

# https://bitbucket.org/phosim/phosim_release/wiki/Instance%20Catalog
# https://bitbucket.org/phosim/phosim_release/wiki/Physics%20Commands
