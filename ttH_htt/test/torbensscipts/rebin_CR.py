#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE
import glob
import shutil
import ROOT
import math
from collections import OrderedDict
import numpy as np
# python test/rename_procs.py --inputPath /home/acaan/hhAnalysis/2016/hh_bb1l_23Jul_baseline_TTSL/datacards/hh_bb1l/prepareDatacards/ --card prepareDatacards_hh_bb1l_hh_bb1l_cat_jet_2BDT_Wjj_BDT_SM_HbbFat_WjjFat_HP_e.root
"""
<ggHHsamplename>_<whatever>_Hbb_HZZ
<ggHHsamplename>_<whatever>_Hbb_Htt
"""
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputPath", type="string", dest="inputPath", help="Full path of where prepareDatacards.root are ")
parser.add_option("--card",      type="string", dest="card",      help="name of prepareDatacards.root. In not given will pick all from the inputPath", default="none")
parser.add_option("--threshold",      type="float", dest="threshold",      help="relativ bin error threshold", default=0.3)
parser.add_option("--maxX",      type="float", dest="maxX",      help="Maximum x axis range", default=0.)
parser.add_option("--quantSig", action='store_true',dest="quantSig", default=False)
(options, args) = parser.parse_args()

inputPath = options.inputPath
card      = options.card
threshold = options.threshold
quantSig = options.quantSig
maxX      = options.maxX
def getQuantiles(inputShapesL):
    tfilein = ROOT.TFile(inputShapesL, "READ")
    bgs = ROOT.TH1F()
    sig = ROOT.TH1F()
    x_final = np.array([0.])
    bestscore = 0
    nb = 0
    ns = 0
    for nkey, key in enumerate(tfilein.GetListOfKeys()) :
        name = key.GetName()
        if not ('signal' in name or 'CMS' in name or 'fakes_mc' in name or 'data_obs' in name):
            print name
            obj = key.ReadObj()
            #obj.Sumw2()
            if nb is 0:
                bgs = obj.Clone()
            else:
                bgs.Add(obj)
            nb = nb + 1
    attempt = 0
    print bgs.Integral(), bgs.GetNbinsX()
    sumEvents = 0
    minEvents = 20.
    low_bins=[bgs.GetBinLowEdge(1)]
    for j in range(bgs.GetNbinsX()):
        sumEvents = sumEvents +  bgs.GetBinContent(j+1);
        if sumEvents>minEvents:
            if (j + 2) <= bgs.GetNbinsX()+1:
                low_bins.append(bgs.GetBinLowEdge(j+2))
            sumEvents=0.
    if abs(low_bins[-1]-bgs.GetXaxis().GetXmax())>0.001:
        low_bins.append(bgs.GetXaxis().GetXmax())
    if maxX > 0.:
        toremove = []
        for i in range(len(low_bins)):
            if low_bins[i]>maxX: toremove.append(low_bins[i])
        for tor in toremove:
            low_bins.remove(tor)
        low_bins.remove(low_bins[-1])
        low_bins.append(maxX)
    attempt = 0
    isOk = True
    print low_bins
    while(attempt <5):
        attempt = attempt + 1
        bgs_test=bgs.Clone()
        x = np.array(low_bins)
        bgs_test= bgs_test.Rebin(len(x)-1,bgs_test.GetName() ,x)
        toremove = []
        for j in range(bgs_test.GetNbinsX()):
            if bgs_test.GetBinError(j+1)/bgs_test.GetBinContent(j+1)>=threshold:
                print 'removing high uncertainty bin'
                if (j+1) < (len(low_bins)-1):
                    toremove.append(bgs_test.GetBinLowEdge(j+2))
                else:
                    toremove.append(bgs_test.GetBinLowEdge(j))
        for tor in toremove:
            low_bins.remove(tor)
    x_final = np.array(low_bins)
    bgs_test=bgs.Clone()
    bgs_test= bgs_test.Rebin(len(x_final)-1,bgs_test.GetName() ,x_final)
    for j in range(bgs_test.GetNbinsX()):
        print bgs_test.GetBinContent(j+1)>0 , (bgs_test.GetBinError(j+1)/bgs_test.GetBinContent(j+1)<threshold)
    tfilein.Close()
    return x_final

def rebin (inputShapesL, inputShapesLnew, bins) :
    ## it assumes no subdirectories in the preparedatacards file,
    tfilein1 = ROOT.TFile(inputShapesL, "READ")
    tfileout2 = ROOT.TFile(inputShapesLnew, "RECREATE")
    print inputShapesLnew
    tfilein1.cd()
    for nkey, key in enumerate(tfilein1.GetListOfKeys()) :
        obj =  key.ReadObj()
        obj_name = key.GetName()
        #if type(obj) is not ROOT.TH1F and type(obj) is not ROOT.TH1D and type(obj) is not ROOT.TH1 and type(obj) is not ROOT.TH1S and type(obj) is not ROOT.TH1C and type(obj) is not ROOT.TH1 :
        if type(obj) is not ROOT.TH1F :
            if type(obj) is ROOT.TH1 :
                print ("data_obs can be be TH1")
                continue
            else :
                print ("WARNING: All the histograms that are not data_obs should be TH1F - otherwhise combine will crash!!!")
                sys.exit()
        tfileout2.cd()
        nominal  = ROOT.TH1F()
        nominal = obj.Rebin(len(bins)-1,obj.GetName() , bins)
        while nominal.GetNbinsX()>20:
            nominal = nominal.Rebin(2, obj.GetName())
        nominal.Write()
        tfilein1.cd()
    tfilein1.Close()
    tfileout2.Close()


inputPathNew = "%s/rebinned/" % (inputPath)
try :
    os.mkdir( inputPathNew )
except :
    print ("already exists: ", inputPathNew)
print ("\n copied \n %s to \n %s \nto have cards with renamed processes" % (inputPath, inputPathNew))

if card == "none" :
    listproc = glob.glob( "%s/*.root" % inputPath)
else :
    listproc = [ "%s/%s" % (inputPath, card) ]

for prepareDatacard in listproc :
    prepareDatacardNew = prepareDatacard.replace(inputPath, inputPathNew)
    bins = getQuantiles(prepareDatacard)
    print bins, len(bins)
    rebin(prepareDatacard,prepareDatacardNew, bins)
    print ("done", prepareDatacardNew)
