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
parser.add_option("--quantSig", action='store_true',dest="quantSig", default=False)
(options, args) = parser.parse_args()

inputPath = options.inputPath
card      = options.card
threshold = options.threshold
quantSig = options.quantSig
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
        if ('signal' in name and 'CMS' not in name):
            print name
            obj = key.ReadObj()
            if ns is 0:
                sig = obj.Clone()
            else:
                sig.Add(obj)
            ns = ns + 1
    #quantileFound = False
    possible_quantiles=[]
    print bgs.Integral()
    for i in range(30):
        #if quantileFound: continue
        nq=30-i
        if nq < 5: continue
        bgs_test=bgs.Clone()
        sig_test=sig.Clone()
        y = []
        x = []
        for j in range(nq):
            y.append(j*(1./nq))
            x.append(0.)
        y = np.array(y)
        x = np.array(x)
        quant = None
        if quantSig:
            quant= sig_test.GetQuantiles(nq,x,y)
        else:
            quant= bgs_test.GetQuantiles(nq,x,y)
        x = np.append(x,np.array([1.]))
        #binstomask = np.ones(len(x), dtype=bool)
        # for en in range(len(x)-1):
        #     if (bgs_test.FindBin(x[en]) is bgs_test.FindBin(x[en+1])):
        #         binstomask[en +1] =False
        # print binstomask
        # x = x[binstomask]
        #print nq, x, len(x)
        #print "-------"
        #print bgs_test.Integral()
        low_bins = []
        for en in range(len(x)-1):
            low_bins.append(bgs_test.FindBin(x[en]))
        low_bins = sorted(list(set(low_bins)))
        better_x = []
        for b in low_bins:
            better_x.append(bgs_test.GetBinLowEdge(b))
        better_x[0] = 0.
        better_x=np.array(better_x)
        x = np.append(better_x,np.array([1.]))
        quantileOk= True
        bgs_test= bgs_test.Rebin(len(x)-1,bgs_test.GetName() ,x)
        sig_test= sig_test.Rebin(len(x)-1,sig_test.GetName() ,x)
        #print bgs_test.Integral()
        #print "-------"
        for j in range(bgs_test.GetNbinsX()):
            #print bgs_test.GetBinError(j)/bgs_test.GetBinContent(j), bgs_test.GetBinContent(j), bgs_test.GetBinError(j)
            #print  nq, bgs_test.GetBinContent(j+1)
            #print sig_test.GetBinContent(j+1)
            if(bgs_test.GetBinContent(j+1)>0):
                quantileOk = quantileOk and bgs_test.GetBinError(j+1)/bgs_test.GetBinContent(j+1)<threshold
        if quantileOk or nq is 5:
            possible_quantiles.append(x)
            #print nq, y, len(y), x, len(x)
            #x_final = x
            #quantileFound = True
        del bgs_test, x,y
        
    for binning in possible_quantiles:
        bgs_test=bgs.Clone()
        sig_test=sig.Clone()
        bgs_test= bgs_test.Rebin(len(binning)-1,bgs_test.GetName() ,binning)
        sig_test= sig_test.Rebin(len(binning)-1,sig_test.GetName() ,binning)
        score = 0
        for j in range(bgs_test.GetNbinsX()):
            #score = score + sig_test.GetBinContent(j+1)*sig_test.GetBinContent(j+1)/bgs_test.GetBinContent(j+1)*(bgs_test.GetBinError(j+1)*bgs_test.GetBinError(j+1)/(bgs_test.GetBinContent(j+1)*bgs_test.GetBinContent(j+1)))
            score = score + sig_test.GetBinContent(j+1)*sig_test.GetBinContent(j+1)/bgs_test.GetBinContent(j+1)
            #score = score + math.sqrt(sig_test.GetBinContent(j+1)*sig_test.GetBinContent(j+1)/bgs_test.GetBinContent(j+1))
            #if math.sqrt(sig_test.GetBinContent(j+1)*sig_test.GetBinContent(j+1)/bgs_test.GetBinContent(j+1))>score:
            #    score = math.sqrt(sig_test.GetBinContent(j+1)*sig_test.GetBinContent(j+1)/bgs_test.GetBinContent(j+1))
        score = math.sqrt(score)
        if score > bestscore:
            bestscore = score
            x_final = binning
    tfilein.Close()
    return x_final

def rebin (inputShapesL, inputShapesLnew, bins) :
    ## it assumes no subdirectories in the preparedatacards file,
    tfilein1 = ROOT.TFile(inputShapesL, "READ")
    tfileout2 = ROOT.TFile(inputShapesLnew, "RECREATE")
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
        nominal.Write()
        tfilein1.cd()
    tfilein1.Close()
    tfileout2.Close()


inputPathNew = "%s/rebinned_quantile/" % (inputPath)
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
    if ('Counter' not in str(prepareDatacardNew)):
        bins = getQuantiles(prepareDatacard)
        print bins, len(bins)
        rebin(prepareDatacard,prepareDatacardNew, bins)
    print ("done", prepareDatacardNew)
