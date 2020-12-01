#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE
import glob
import shutil
import ROOT
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
(options, args) = parser.parse_args()

inputPath = options.inputPath
card      = options.card
threshold = options.threshold
def getQuantiles(inputShapesL):
    tfilein = ROOT.TFile(inputShapesL, "READ")
    bgs = ROOT.TH1F()
    x_final = np.array([0.])
    n = 0
    for nkey, key in enumerate(tfilein.GetListOfKeys()) :
        name = key.GetName()
        if not ('signal' in name or 'CMS' in name or 'fakes_mc' in name or 'data_obs' in name):
            print name
            obj = key.ReadObj()
            #obj.Sumw2()
            if n is 0:
                bgs = obj.Clone()
            else:
                bgs.Add(obj)
            n = n + 1
    quantileFound = False
    print bgs.Integral()
    for i in range(20):
        if quantileFound: continue
        nq=20-i
        if nq < 5: continue
        bgs_test=bgs.Clone()
        y = []
        x = []
        for j in range(nq):
            y.append(j*(1./nq))
            x.append(0.)
        y = np.array(y)
        x = np.array(x)
        quant= bgs_test.GetQuantiles(nq,x,y)
        x = np.append(x,np.array([1.]))
        #print nq, x, len(x)
        bgs_test= bgs_test.Rebin(nq,bgs_test.GetName() ,x)
        quantileOk= True
        for j in range(bgs_test.GetNbinsX()):
            #print bgs_test.GetBinError(j)/bgs_test.GetBinContent(j), bgs_test.GetBinContent(j), bgs_test.GetBinError(j)
            #print  nq, bgs_test.GetBinContent(j+1)
            if(bgs_test.GetBinContent(j+1)>0):
                quantileOk = quantileOk and bgs_test.GetBinError(j+1)/bgs_test.GetBinContent(j+1)<threshold
        if quantileOk or nq is 5:
            #print nq, y, len(y), x, len(x)
            x_final = x
            quantileFound = True
        del bgs_test, x,y
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
        print bins
        rebin(prepareDatacard,prepareDatacardNew, bins)
    print ("done", prepareDatacardNew)
