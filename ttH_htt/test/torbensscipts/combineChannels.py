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
parser.add_option("--channels", type="string", dest="channels", help="channels to combine seperated by :")
parser.add_option("--outChannel", type="string", dest="outChannel", help="Name of the output channel")
parser.add_option("--outPath", type="string", dest="outPath", help="Full path to output datacard")
parser.add_option("--era", type="string", dest="era", help="era either 2016/2017/2018/RUN2")
parser.add_option("--analysis", type="string", dest="analysis", help="either nonResLO or Spin0/Spin2")
(options, args) = parser.parse_args()
inputPath = options.inputPath
channels = options.channels.split(":")
outChannel = options.outChannel
outPath = options.outPath
era = options.era
analysis = options.analysis

pathsToCopyFrom = []
for ch in channels:
    pathsToCopyFrom.append((inputPath + "/"+ ch + "/" + era).replace("//","/"))

commands = []
commands.append(('rm %s/*'%(outPath)).replace("//","/"))
for ch in pathsToCopyFrom:
    commands.append(('cp %s/*.root %s'%( ch, outPath)).replace("//","/"))
    


nodenames = []
for f in glob.glob( "%s/*.txt" % pathsToCopyFrom[0]):
    nodenames.append(f.split("_")[-1].strip(".txt"))

for node in nodenames:
    command = "combineCards.py "
    for ch in pathsToCopyFrom:
        command  = command + glob.glob( "%s/*%s.txt" %(ch,node))[0] + " "
    command = command + (">> %s/datacard_%s_%s_%s_%s.txt"%(outPath,outChannel, era, analysis, node)).replace("//","/")
    commands.append(command)

for command in commands:
    print command
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line.rstrip("\n")
    print 'done'
    retval = p.wait()
