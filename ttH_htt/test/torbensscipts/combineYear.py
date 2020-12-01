#!/usr/bin/env python
import os, shlex
import subprocess
import glob
import shutil
import ROOT
from collections import OrderedDict

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputPath", type="string", dest="inputPath", help="Full path of where datacards are ")
(options, args) = parser.parse_args()
inputPath = options.inputPath

path16 = inputPath + "2016/"
path17 = inputPath + "2017/"
path18 = inputPath + "2018/"
pathRun2 = inputPath + "RUN2/"

commands = []
commands.append('rm %s*'%(pathRun2))
commands.append('cp %s*.root %s'%(path16,pathRun2))
commands.append('cp %s*.root %s'%(path17,pathRun2))
commands.append('cp %s*.root %s'%(path18,pathRun2))

listproc = glob.glob( "%s/*.txt" % path16)
for card in listproc:
    cardbasename=card.split("/")[-1]
    card16=card
    card17=path17+cardbasename.replace('2016','2017') 
    card18=path18+cardbasename.replace('2016','2018') 
    cardRun2=pathRun2+cardbasename.replace('2016','Run2') 
    commands.append('combineCards.py %s %s %s >> %s'%(card16,card17,card18,cardRun2))

for command in commands:
    print command
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line.rstrip("\n")
    print 'done'
    retval = p.wait()


