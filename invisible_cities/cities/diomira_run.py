from __future__ import print_function
from __future__ import absolute_import

class NoAdequateTests(Exception):
    pass

raise NoAdequateTests("Please write some tests for this code!")

from glob import glob
import os
from time import time

from invisible_cities.core.configure import configure
from invisible_cities.cities.diomira import Diomira

ffile = os.environ['ICDIR'] + '/database/test_data/electrons_40keV_z250_RWF.h5'
try:
    os.system("rm -f {}".format(ffile))
except(IOError):
    pass

ffile = os.environ['ICDIR'] + '/config/diomira.conf'
CFP = configure(['DIOMIRA','-c',ffile])
fpp = Diomira()
files_in = glob(CFP['FILE_IN'])
files_in.sort()
fpp.set_input_files(files_in)
fpp.set_output_file(CFP['FILE_OUT'],
                        compression=CFP['COMPRESSION'])
fpp.set_print(nprint=CFP['NPRINT'])
fpp.set_sipm_noise_cut(noise_cut=CFP["NOISE_CUT"])

nevts = CFP['NEVENTS'] if not CFP['RUN_ALL'] else -1
t0 = time()
nevt = fpp.run(nmax=nevts)
t1 = time()
dt = t1 - t0
print("DIOMIRA run {} evts in {} s, time/event = {}".\
      format(nevt, dt, dt/nevt))
