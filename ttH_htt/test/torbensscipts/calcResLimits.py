#!/usr/bin/env python
import os, shlex
import subprocess
import glob
import shutil
import ROOT
from collections import OrderedDict


from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputPath", type="string", dest="inputPath", help="Full path of where prepareDatacards.root are ")
parser.add_option("--outPath", type="string", dest="outPath", help="Full path of where the cards should be created ")
parser.add_option("--spinCase", type="string", dest="spinCase", help="The spin case either spin0 or spin2")
parser.add_option("--channel", type="string", dest="channel", help="The multilepton channel, either 0l_4tau, 1l_3tau, 2lss, 2l_2tau, 3l, 3l_1tau, 4l")
parser.add_option("--era", type="string", dest="era", help="The data taking period.")
(options, args) = parser.parse_args()

inputPath = options.inputPath
outPath = options.outPath
spinCase = options.spinCase
channel = options.channel
era = options.era

listproc = glob.glob( "%s/*.txt" % inputPath)
combinecommands = []
cleancommands =[] 
for card in listproc:
    cardname = card.split("/")[-1]
    mass = cardname.split('_')[-1].strip('.txt')
    label = "multilepton_%s_%s_%s_%s" %(era, channel, spinCase, mass)
    command1 = "combine -M Asymptotic -m 125 -n %s %s --run blind"% (label,card)
    command2 = "mv higgsCombine%s.Asymptotic.mH125.root %s"%(label, outPath)
    combinecommands.append(command1)
    cleancommands.append(command2)

reorderedCombineCommands = [combinecommands[i:i + 4] for i in range(0, len(combinecommands), 4)]
for combineBlock in reorderedCombineCommands:
    commands = []
    for command in combineBlock:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        commands.append([command,p])
    for command in commands:
        print command[0]
        for line in command[1].stdout.readlines():
            print line.rstrip("\n")
        command[1].wait()
        print 'done'
for command in cleancommands:
    print command
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line.rstrip("\n")
    print 'done'
    retval = p.wait()

