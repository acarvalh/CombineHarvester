#!/usr/bin/env python
import os, subprocess, sys
workingDir = os.getcwd()
import os, re, shlex
from ROOT import *
import numpy as np
import array as arr
from math import sqrt, sin, cos, tan, exp
import glob

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
# python test/rebin_datacards_2.py --channel "bbWW_SL" --BINtype quantiles --signal_type nonresNLO --HHtype bbWW --era 2018
# python test/rebin_datacards_2.py --channel "bbWW_DL_aa" --BINtype quantiles --signal_type nonresNLO --HHtype bbWW --era 2018 --drawLimitsOnly
from io import open

functions = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/python/data_manager_rebin_datacards.py"
class mainprogram():
    def runme(self):
        execfile(functions)
this = mainprogram()
this.runme()
testPrint()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--channel ", type="string", dest="channel", help="The ones whose variables implemented now are:\n   - 1l_2tau\n   - 2lss_1tau\n It will create a local folder and store the report*/xml", default="2lss_1tau")
parser.add_option("--variables", type="string", dest="variables", help="Add convention to file name", default="teste")
parser.add_option("--BINtype", type="string", dest="BINtype", help="regular / ranged / quantiles", default="regular")
parser.add_option("--doPlots", action="store_true", dest="doPlots", help="If you call this will not do plots with repport", default=False)
parser.add_option("--drawLimitsOnly", action="store_true", dest="drawLimitsOnly", help="If you call this will not do plots with repport", default=False)
parser.add_option("--doLimitsOnly", action="store_true", dest="doLimitsOnly", help="If you call this will not do plots with repport", default=False)
parser.add_option(
    "--signal_type",    type="string",       dest="signal_type",
    help="Options: \"noresLO\" | \"nonresNLO\" | \"res\" ",
    default="nonresNLO"
    )
parser.add_option(
    "--mass",           type="string",       dest="mass",
    help="Options: \n nonresNLO = it will be ignored \n noresLO = \"SM\", \"BM12\", \"kl_1p00\"... \n \"spin0_900\", ...",
    default="nonresNLO"
    )
parser.add_option(
    "--HHtype",         type="string",       dest="HHtype",
    help="Options: \"bbWW\" | \"multilep\" ",
    default="bbWW"
    )
parser.add_option(
    "--era", type="int",
    dest="era",
    help="To appear on the name of the file with the final plot. If era == 0 it assumes you gave the path for the 2018 era and it will use the same naming convention to look for the 2017/2016.",
    default=2016
    )
(options, args) = parser.parse_args()

doLimitsOnly   = options.doLimitsOnly
drawLimitsOnly = options.drawLimitsOnly
doPlots    = options.doPlots
channel    = options.channel
BINtype    = options.BINtype
signal_type  = options.signal_type
mass         = options.mass
HHtype       = options.HHtype
era          = options.era

## HH
if channel == "bbWW_DL"   : execfile(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/cards/info_bbWW_DL_datacards.py")
if channel == "bbWW_SL"   : execfile(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/cards/info_bbWW_SL_datacards.py")
if channel == "bbWW_SL_aa"   : execfile(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/cards/info_bbWW_SL_Aachen_datacards.py")
if channel == "bbWW_DL_aa"   : execfile(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/cards/info_bbWW_DL_Aachen_datacards.py")


info = read_from()
print ("Cards to rebin from %s" % channel)

sendToCondor = False
ToSubmit = " "
if sendToCondor :
    ToSubmit = " --job-mode condor --sub-opt '+MaxRuntime = 1800' --task-name"

sources           = []
bdtTypesToDo      = []
bdtTypesToDoLabel = []
bdtTypesToDoFile  = []
sourcesCards      = []

local = info["local"]
import shutil,subprocess
proc=subprocess.Popen(["mkdir %s" % local],shell=True,stdout=subprocess.PIPE)
out = proc.stdout.read()
mom_datacards = "%s/datacards_rebined/" % local
proc=subprocess.Popen(["mkdir %s" % mom_datacards],shell=True,stdout=subprocess.PIPE)
out = proc.stdout.read()

print (info["bdtTypes"])

counter=0
for ii, bdtType in enumerate(info["bdtTypes"]) :
    fileName = info["mom"] + "/" + bdtType + ".root"
    source=local+"/" + bdtType
    print (fileName)
    if os.path.isfile(fileName) :
        proc              = subprocess.Popen(['cp ' + fileName + " " + local],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
        sources           = sources + [source]
        bdtTypesToDo      = bdtTypesToDo +[channel+" "+bdtType]
        bdtTypesToDoLabel = bdtTypesToDoLabel + [bdtType]
        bdtTypesToDoFile  = bdtTypesToDoFile+[bdtType]
        ++counter
        print ("rebinning ", sources[counter])
    else : print ("does not exist ",source)
print ("I will rebin", bdtTypesToDoLabel,"(",len(sources),") BDT options")

if BINtype == "regular" or BINtype == "ranged" :
    binstoDo = info["nbinRegular"]
if BINtype == "quantiles" :
    binstoDo = info["nbinQuant"]
if BINtype == "none" :
    binstoDo=np.arange(1, info["targetBinning"])
print binstoDo

### first we do one datacard.txt / bdtType
for nn, source in enumerate(sources) :
    if BINtype == "regular" :
        outfile = "%s" % (source.replace("prepareDatacards_", "datacard_"))
    if BINtype == "quantiles" or BINtype == "ranged":
        outfile = "%s_%s" % (source.replace("prepareDatacards_", "datacard_"), BINtype )

    cmd = "WriteDatacards.py "
    cmd += "--inputShapes %s.root " % (source)
    cmd += "--channel %s " % channel
    cmd += "--output_file %s " % (outfile)
    cmd += "--noX_prefix --era 2017  --analysis HH " # --no_data
    cmd += " --signal_type %s "      % signal_type
    cmd += " --mass %s "             % mass
    cmd += " --HHtype %s "           % HHtype
    #cmd += " --shapeSyst"
    log_datacard = "%s_datacard.log" % source
    runCombineCmd(cmd, ".", log_datacard)

    didCard = False
    for line in open(log_datacard):
        if "Output file:" in line :
            fileCard = line.split(" ")[3].replace("'","").replace(",","").replace(".txt","") #splitPath(lineL)[1]
            print("done card %s.txt" % fileCard)
            didCard = True
            break
    if didCard == False :
        print ("!!!!!!!!!!!!!!!!!!!!!!!! The WriteDatacards did not worked, to debug please check %s to see up to when the script worked AND run again for chasing the error:" % log_datacard)
        print(cmd)
        sys.exit()
    sourcesCards = sourcesCards + [ fileCard ]

nameOutFileAdd = ""
if BINtype=="none" :
    nameOutFileAdd =  "bins_none"
if BINtype=="regular" or options.BINtype == "mTauTauVis":
    nameOutFileAdd =  "bins"
if BINtype=="ranged" :
    nameOutFileAdd =  "bins_ranged"
if BINtype=="quantiles" :
    nameOutFileAdd = "bins_quantiles"

colorsToDo=['r','g','b','m','y','c', 'fuchsia', "peachpuff",'k','orange','y','c'] #['r','g','b','m','y','c','k']
do_signalFlat = False
#########################################
if not (drawLimitsOnly or doLimitsOnly) :
    ## make rebinned datacards
    fig, ax = plt.subplots(figsize=(5, 5))
    plt.title(BINtype+" in sum of BKG ")
    lastQuant=[]
    xmaxQuant=[]
    xminQuant=[]
    bin_isMoreThan02 = []
    maxplot = -99.
    ncolor = 0
    ncolor2 = 0
    linestyletype = "-"
    isBKG = False

    for nn, sourceL in enumerate(sourcesCards) :
        if "VBFnode" in sourceL or "HHVBF" in sourceL :
            doFlat = "VBFnode"
        elif "GGFnode" in sourceL or "HHGluGlu" in sourceL :
            doFlat = "GGFnode"
        elif "Hnode" in sourceL or "node_H" in sourceL :
            doFlat = "Hnode"
        else :
            doFlat = "BKGnode"
        print("doFlat = %s" % doFlat)

        print ( "rebining %s" % sourceL )
        errOcont = rebinRegular(
            sourceL,
            binstoDo,
            BINtype,
            doFlat,
            info["targetBinning"],
            doPlots,
            bdtTypesToDo[nn],
            mom_datacards,
            nameOutFileAdd,
            info["withFolder"],
            isBKG
            )

        print bdtTypesToDo[nn]
        lastQuant=lastQuant+[errOcont[4]]
        xmaxQuant=xmaxQuant+[errOcont[5]]
        xminQuant=xminQuant+[errOcont[6]]
        bin_isMoreThan02 = bin_isMoreThan02 + [errOcont[7]]

        print (binstoDo,errOcont[2])
        plt.plot(binstoDo, errOcont[2], color=colorsToDo[ncolor],linestyle=linestyletype,label=bdtTypesToDo[nn].replace("ttH_1l_2tau","BDT PAS").replace("output_NN_","NN_").replace("_ttH_tH_3cat_","").replace("1l_2tau","").replace("2lss_1tau_","").replace("_1tau","").replace("2lss","").replace("__","_"))  #.replace("3l_0tau output_NN_3l_ttH_tH_3cat_v8_", "") ) # ,label=bdtTypesToDo[nn]
        ncolor = ncolor + 1
        if ncolor == 10 :
            ncolor = 0
            ncolor2 = ncolor2 + 1
            if ncolor2 == 0 : linestyletype = "-"
            if ncolor2 == 1 : linestyletype = "-."
            if ncolor2 == 2 : linestyletype = ":"
        ax.set_xlabel('nbins')
    maxplot = 1.2
    plt.axis((min(binstoDo),max(binstoDo),0,maxplot*1.2))
    ax.set_ylabel('err/content last bin')
    ax.legend(loc='best', fancybox=False, shadow=False, ncol=1, fontsize=8)
    plt.grid(True)
    namefig = local + '/' + options.variables + '_ErrOcont_' + BINtype + '.pdf'
    fig.savefig(namefig)
    print ("saved",namefig)
    print (bin_isMoreThan02)
    #########################################

if not drawLimitsOnly :
    ## doint Limits
    for nn, sourceL in enumerate(sourcesCards) :
        for nbins in binstoDo :
            fileCardOnlyL = sourceL.split("/")[len(sourceL.split("/")) -1]
            fileCardOnlynBinL = "%s_%s%s" % (fileCardOnlyL, str(nbins), nameOutFileAdd)
            fileCardL = "%s/%s" % (mom_datacards, fileCardOnlynBinL)
            print ("make limit for %s.txt" % fileCardL)
            runCombineCmd("cp %s.txt %s.txt" % (sourceL, fileCardL))
            with open("%s.txt" % fileCardL,'r+') as ff:
                filedata = ff.read()
                filedata = filedata.replace(fileCardOnlyL, fileCardOnlynBinL)
                ff.truncate(0)
                ff.write(filedata)

            cmd = "combineTool.py  -M AsymptoticLimits  -t -1 %s.txt " % (fileCardL)
            if sendToCondor :
                cmd += ToSubmit + " %s_%s%s " % ()
            runCombineCmd(cmd,  local, "%s.log" % fileCardL)

            if nbins in info["makePlotsBin"] :
                # make only HH be considered signal (independent of the card marking)
                FolderOut = "%s/results/" % mom_datacards
                proc=subprocess.Popen(["mkdir %s" % FolderOut],shell=True,stdout=subprocess.PIPE)
                out = proc.stdout.read()

                cmd = "text2workspace.py"
                cmd += " %s.txt  " % (fileCardOnlynBinL)
                cmd += " -o %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL)
                runCombineCmd(cmd, mom_datacards)
                print ("done %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL))

                cmd = "combineTool.py -M FitDiagnostics "
                cmd += " %s_WS.root" % fileCardOnlynBinL
                #if blinded :
                #    cmd += " -t -1 "
                cmd += " --saveShapes --saveWithUncertainties "
                cmd += " --saveNormalization "
                cmd += " --skipBOnlyFit "
                cmd += " -n _shapes_combine_%s" % fileCardOnlynBinL
                runCombineCmd(cmd, FolderOut)
                fileShapes = glob.glob("%s/fitDiagnostics_shapes_combine_%s*root" % (FolderOut, fileCardOnlynBinL))[0]
                print ( "done %s" % fileShapes )

                savePlotsOn = "%s/plots/" % (mom_datacards)
                cmd = "mkdir %s" % savePlotsOn
                runCombineCmd(cmd)

                plainBins = False
                cmd = "python test/makePlots_louvain.py "
                cmd += " --input  %s" % fileShapes
                cmd += " --odir %s" % savePlotsOn
                #if doPostFit         :
                #    cmd += " --postfit "
                if not plainBins :
                    cmd += " --original %s/%s.root"        % (mom_datacards, fileCardOnlynBinL)
                cmd += " --era %s" % str(era)
                cmd += " --nameOut %s" % fileCardOnlynBinL
                #cmd += " --do_bottom "
                cmd += " --channel %s" % channel
                cmd += " --HH --binToRead HH_%s --binToReadOriginal  HH_%s " % (channel, channel)
                #cmd += "--nameLabel %s --labelX %s" % (toRead.replace(filebegin, ""), toRead.replace(filebegin, ""))
                #if not blinded         :
                cmd += " --signal_type %s "      % signal_type
                cmd += " --mass %s "             % mass
                cmd += " --HHtype %s "           % HHtype
                #cmd += " --do_bottom "
                #cmd += " --unblind  "
                cmd += " --nameLabel %s " % bdtTypesToDoLabel[nn]
                plotlog = "%s/%s_plot.log" % (savePlotsOn, fileCardOnlynBinL)
                runCombineCmd(cmd, '.', plotlog)

                didPlot = False
                for line in open(plotlog):
                    if '.pdf' in line and "saved" in line :
                        print(line)
                        didPlot = True
                        break
                if didPlot == False :
                    print ("!!!!!!!!!!!!!!!!!!!!!!!! The makePlots did not worked, to debug please check %s to see up to when the script worked AND run again for chasing the error:" % plotlog)
                    print(cmd)
                    #sys.exit()

#########################################
## make limits
print sources

print "draw limits"
fig, ax = plt.subplots(figsize=(5, 5))
if BINtype == "quantiles" :
    namefig=local+'/'+options.variables+'_fullsim_limits_quantiles'
if BINtype == "regular" or BINtype == "mTauTauVis":
    namefig=local+'/'+options.variables+'_'+options.channel+'_fullsim_limits'
if BINtype == "ranged" :
    namefig=local+'/'+options.variables+'_fullsim_limits_ranged'
file = open(namefig+".csv","w")
#maxlim =-99.
for nn, source in enumerate(sourcesCards) :
    fileCardOnlyL = source.split("/")[len(source.split("/")) -1]
    print(fileCardOnlyL)
    limits = ReadLimits(
        fileCardOnlyL,
        binstoDo,
        BINtype,
        channel,
        mom_datacards,
        0, 0,
        sendToCondor,
        nameOutFileAdd
        )
    print (len(binstoDo),len(limits[0]))
    print 'binstoDo= ', binstoDo
    print limits[0]
    for jj in limits[0] : file.write(unicode(str(jj)+', '))
    file.write(unicode('\n'))
    plt.plot(
        binstoDo,limits[0], color=colorsToDo[nn], linestyle='-',marker='o',
        label=bdtTypesToDoFile[nn].replace("output_NN_", "").replace("_withWZ", "").replace("3l_0tau", "") #.replace("mvaOutput_0l_2tau_deeptauVTight", "mva_legacy")
        )
    plt.plot(binstoDo,limits[1], color=colorsToDo[nn], linestyle='-')
    plt.plot(binstoDo,limits[3], color=colorsToDo[nn], linestyle='-')
ax.legend(
    loc='upper left',
    fancybox=False,
    shadow=False ,
    ncol=1,
    fontsize=8
)
ax.set_xlabel('nbins')
ax.set_ylabel('limits')
maxsum=0
maxlim = info["maxlim"]
minlim = info["minlim"]
plt.axis((min(binstoDo),max(binstoDo), minlim, maxlim))
fig.savefig(namefig+'_ttH.png')
fig.savefig(namefig+'_ttH.pdf')
file.close()
print ("saved",namefig)
