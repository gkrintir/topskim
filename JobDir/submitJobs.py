#!/usr/bin/env python
import os,sys
import optparse
import commands
import time

#python scripts/submitJobs.py -q 1nh -j 2 -n 10000 -f 1 -o /afs/cern.ch/user/g/gkrintir/github/HI/CMSSW_7_5_7_patch2/src/UserCode/diall/first_result_HighPtMuon


usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-q', '--queue'      ,dest='queue'  ,help='batch queue'          ,default='')
parser.add_option('-j', '--jobs'       ,dest='jobs'   ,help='number of jobs'       ,default=1,   type=int)
parser.add_option('-f', '--files'      ,dest='files'  ,help='files per job'        ,default=5,   type=int)
parser.add_option('-o', '--output'     ,dest='output' ,help='output directory'     ,default='')
(opt, args) = parser.parse_args()


workBase=os.getcwd()

#loop over the required number of jobs
scriptFile1 = open('submitJobs.sh', 'w')


for n in xrange(1,opt.jobs+1):

    #create a wrapper for standalone job
    scriptFile = open('runJob_%d.sh'% n, 'w')
    scriptFile.write('#!/bin/bash\n')
    scriptFile.write('export OUTDIR=%s\n' % opt.output)
    scriptFile.write('cd /afs/cern.ch/user/g/gkrintir/PbPb_Top1/topskim/\n')#cd %s\n'%workBase)
    #scriptFile.write('cd - \n')
    scriptFile.write('root -l  -q -b makeEMuSkim_OnBatch2.C\'("data.txt", %d, %d, "test_data.root", false)\'\n' % ((n-1)*opt.files,(n-1)*opt.files+opt.files) )
    scriptFile.write('export OUTPUT=AnaResults_%d.root\n' % n)
    scriptFile.write('cp test_data.root $OUTDIR/$OUTPUT\n')
    scriptFile.write('rm test_data.root\n')
    scriptFile.close()

    if opt.queue=='':
        print 'Job #%d will run locally' % n
        os.system('runJob_%d.sh' % n )
    else:
        print 'Job #%d will run remotely' % n
        #print "bsub -q %s -J runJob_%d -o runJob_%d.log < runJob_%d.sh" % (opt.queue,n,n,n)
        scriptFile1.write("bsub -q %s -J runJob_%d -o runJob_%d.log < runJob_%d.sh\n" % (opt.queue,n,n,n) )

        #bsub -q 1nd -J runJob_1 -o runJob_1.log < runJob_1.sh
scriptFile1.close()

#prepare to run it
os.system('chmod u+rwx submitJos.sh')

