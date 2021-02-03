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
from io import open

functions = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/python/data_manager_rebin_datacards.py"
class mainprogram():
    def runme(self):
        execfile(functions)
this = mainprogram()
this.runme()
testPrint()

local = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_DNN10_2018_syst/"
era = 2018
hadd_files = True
rebin = True
WriteDatacards = True

fixed_bin_boundaries = [
#["HH_cat_DNN10_DY_VVVnode",          [0.0, 0.26, 0.30, 0.33, 0.36, 0.39, 0.42, 0.45, 0.49, 0.55, 1.0], 10],
#["HH_cat_DNN10_TT_ST_TTVX_Rarenode", [0.0, 0.26, 0.29, 0.31, 0.32, 0.34, 0.36, 0.38, 0.41, 0.45, 1.0], 10],
["HH_cat_boosted1b_DNN10_GGFnode",   [0.0, 0.4946, 1.0], 2],
#["HH_cat_boosted1b_DNN10_Hnode",     [0.0, 0.33, 0.37, 0.41, 0.48, 1.0], 5],
#["HH_cat_boosted1b_DNN10_VBFnode",   [0.0, 0.6, 1.0], 2],
#["HH_cat_resolved1b_DNN10_GGFnode",  [0.0, 0.28, 0.31, 0.33, 0.35, 0.37, 0.39, 0.40, 0.42, 0.44, 0.46, 0.47, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.65, 1.0], 20],
#["HH_cat_resolved1b_DNN10_Hnode",    [0.0, 0.29, 0.33, 0.36, 0.41, 1.0], 5],
#["HH_cat_resolved1b_DNN10_VBFnode",  [0.0, 0.42, 0.50, 0.58, 0.65, 0.72, 0.80, 1.0], 7],
#["HH_cat_resolved2b_DNN10_GGFnode",  [0.0, 0.34, 0.39, 0.43, 0.47, 0.50, 0.53, 0.56, 0.60, 0.64, 1.0], 10],
#["HH_cat_resolved2b_DNN10_Hnode",    [0.0, 0.30, 0.33, 0.37, 0.41, 1.0], 4],
#["HH_cat_resolved2b_DNN10_VBFnode",  [0.0, 0.52, 0.64, 0.74, 1.0], 5]
]

local_merged = "%s/merging/" % local
local_quantiles = "%s/merging/quantiles/" % local
local_datacards = "%s/merging/datacards/" % local

###
# hadd files
if hadd_files :
    if not os.path.exists(local_merged) :
        proc=subprocess.Popen(["mkdir %s" % local_merged],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    ## merge signal nodes by Hbb subcategory
    for Hbb in ["boosted1b", "resolved1b", "resolved2b"] :
        for node in ["GGF", "H", "VBF"] :
            filepath = "%s/HH_cat_%s_DNN10_%snode_%s.root" % (local_merged, Hbb, node, str(era))
            if not os.path.exists(filepath) :
                cmd = "hadd merging/HH_cat_%s_DNN10_%snode_%s.root HH_cat_*_%s_DNN10_%snode_%s.root" % (Hbb, node, str(era), Hbb, node, str(era))
                runCmd(cmd, local)
            else :
                print ("file %s exists already" % filepath)
    ## merge BKG nodes
    filepath = "%s/HH_cat_DNN10_DY_VVVnode_%s.root" % (local_merged, str(era))
    if not os.path.exists(filepath) :
        cmd = "hadd merging/HH_cat_DNN10_DY_VVVnode_%s.root HH_cat_*_DNN10_DYnode_%s.root HH_cat_*_DNN10_VVVnode_%s.root" % (str(era), str(era), str(era))
        runCmd(cmd, local)
    else :
        print ("file %s exists already" % filepath)
    ##
    filepath = "%s/HH_cat_DNN10_TT_ST_TTVX_Rarenode_%s.root" % (local_merged, str(era))
    if not os.path.exists(filepath) :
        cmd = "hadd merging/HH_cat_DNN10_TT_ST_TTVX_Rarenode_%s.root HH_cat_*_DNN10_TTnode_%s.root HH_cat_*_DNN10_STnode_%s.root HH_cat_*_DNN10_TTVXnode_%s.root HH_cat_*_DNN10_Rarenode_%s.root" % (str(era), str(era), str(era), str(era), str(era))
        runCmd(cmd, local)
    else :
        print ("file %s exists already" % filepath)

nameOutFileAdd = "_bins_quantiles"
if rebin :
    if not os.path.exists(local_quantiles) :
        proc=subprocess.Popen(["mkdir %s" % local_quantiles],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()

    for subcat in fixed_bin_boundaries :

        source = "%s/%s_%s_%s%s.root" % (local_quantiles, subcat[0], str(era), str(subcat[2]), nameOutFileAdd)
        if os.path.exists(source) :
            print("file for %s already done, delete it to remake it" % source)
            continue

        histSource = "%s/%s_%s" % (local_merged, subcat[0], str(era))
        nbin = [subcat[2]]
        targetBinning = arr.array('d', subcat[1])
        doplots = False
        BINtype = "quantiles"
        bdtType = "quantiles"

        withFolder = False
        partialCopy = False
        do_signalFlat = False

        print ( "rebining %s" % histSource )
        errOcont = rebinRegular(
            histSource,
            nbin,
            BINtype,
            do_signalFlat,
            targetBinning,
            doplots,
            bdtType,
            local_quantiles,
            nameOutFileAdd,
            withFolder,
            partialCopy
            )



if WriteDatacards :
    if not os.path.exists(local_datacards) :
        proc=subprocess.Popen(["mkdir %s" % local_datacards],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()

    HHtype = "bbWW"
    mass = "nonresNLO"
    signal_type = "nonresNLO"
    channel = "blabla"
    for subcat in fixed_bin_boundaries :
        source = "%s/%s_%s_%s%s.root" % (local_quantiles, subcat[0], str(era), str(subcat[2]), nameOutFileAdd)
        print (source)

        cmd = "WriteDatacards.py "
        cmd += "--inputShapes %s.root " % (source)
        cmd += "--channel %s " % channel
        #cmd += "--output_file %s " % (outfile)
        cmd += "--noX_prefix --era 2017  --no_data --analysis HH "
        cmd += " --signal_type %s "      % signal_type
        cmd += " --mass %s "             % mass
        cmd += " --HHtype %s "           % HHtype
        #cmd += " --shapeSyst"
        log_datacard = "%s_datacard.log" % source
        runCombineCmd(cmd, ".", log_datacard)



# ./rebin_datacards.py --channel "4l_0tau"  --BINtype "regular" --doLimits
