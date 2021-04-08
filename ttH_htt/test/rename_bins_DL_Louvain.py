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

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
parser = ArgumentParser(
    description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--cards_folder",
    dest="cards_folder",
    help="Folder that contains the datacard.txt/root.",
    )
parser.add_argument(
    "--one_fitdiag_per_bin",
    action="store_true",
    dest="one_fitdiag_per_bin",
    help="Rename bins for each datacard.",
    default=False
    )
args = parser.parse_args()

mom_datacards = args.cards_folder
one_fitdiag_per_bin = args.one_fitdiag_per_bin

def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)

"""
list_DL_cards = [
    ["DY_VVVnode_2018",          "datacard_HH_cat_DNN10_DY_VVVnode_2018_10_bins_quantiles"],
    ["TT_ST_TTVX_Rarenode_2018", "datacard_HH_cat_DNN10_TT_ST_TTVX_Rarenode_2018_10_bins_quantiles"],
    ["boosted1b_GGFnode_2018",   "datacard_HH_cat_boosted1b_DNN10_GGFnode_2018_2_bins_quantiles"],
    ["boosted1b_Hnode_2018",     "datacard_HH_cat_boosted1b_DNN10_Hnode_2018_5_bins_quantiles"],
    ["boosted1b_VBFnode_2018",   "datacard_HH_cat_boosted1b_DNN10_VBFnode_2018_2_bins_quantiles"],
    ["resolved1b_GGFnode_2018",  "datacard_HH_cat_resolved1b_DNN10_GGFnode_2018_20_bins_quantiles"],
    ["resolved1b_Hnode_2018",    "datacard_HH_cat_resolved1b_DNN10_Hnode_2018_5_bins_quantiles"],
    ["resolved1b_VBFnode_2018",  "datacard_HH_cat_resolved1b_DNN10_VBFnode_2018_7_bins_quantiles"],
    ["resolved2b_GGFnode_2018",  "datacard_HH_cat_resolved2b_DNN10_GGFnode_2018_10_bins_quantiles"],
    ["resolved2b_Hnode_2018",    "datacard_HH_cat_resolved2b_DNN10_Hnode_2018_4_bins_quantiles"],
    ["resolved2b_VBFnode_2018",  "datacard_HH_cat_resolved2b_DNN10_VBFnode_2018_5_bins_quantiles"],
]
"""

list_DL_cards = [
    ["DY_VVVnode_2018",          "outputcard_DNN10_DY_VVV_bbWW_nonres_none"],
    ["TT_ST_TTVX_Rarenode_2018", "outputcard_DNN10_TT_ST_TTVX_Rare_bbWW_nonres_none"],
    ["boosted1b_GGFnode_2018",   "outputcard_boosted1b_DNN10_GGF_bbWW_nonres_none"],
    ["boosted1b_Hnode_2018",     "outputcard_boosted1b_DNN10_Hnode_bbWW_nonres_none"],
    ["boosted1b_VBFnode_2018",   "outputcard_boosted1b_DNN10_VBF_bbWW_nonres_none"],
    ["resolved1b_GGFnode_2018",  "outputcard_resolved1b_DNN10_GGF_bbWW_nonres_none"],
    ["resolved1b_Hnode_2018",    "outputcard_resolved1b_DNN10_Hnode_bbWW_nonres_none"],
    ["resolved1b_VBFnode_2018",  "outputcard_resolved1b_DNN10_VBF_bbWW_nonres_none"],
    ["resolved2b_GGFnode_2018",  "outputcard_resolved2b_DNN10_GGF_bbWW_nonres_none"],
    ["resolved2b_Hnode_2018",    "outputcard_resolved2b_DNN10_Hnode_bbWW_nonres_none"],
    ["resolved2b_VBFnode_2018",  "outputcard_resolved2b_DNN10_VBF_bbWW_nonres_none"],
]

card_all_eras = "combineCards.py "
for era in [2018] : # 2016, 2017,
    card_this_era = "combineCards.py "
    for cards in list_DL_cards :

        bin_name = cards[0].replace(str(2018),str(era))
        card_name = cards[1].replace(str(2018),str(era))
        card_location = mom_datacards #.replace(str(2018),str(era))

        if one_fitdiag_per_bin :
            cmd = "combineCards.py "
            cmd += " %s=%s.txt" % (bin_name, card_name)
            cmd += ">  renamedBin_%s_DL.txt" % bin_name
            runCombineCmd(cmd, card_location)

        card_this_era += " %s=%s.txt" % (bin_name, card_name)
        card_all_eras += " %s=%s.txt" % (bin_name, card_name)

    card_this_era += ">  combo_%s_DL.txt" % str(era)
    runCombineCmd(card_this_era, card_location)
    print  ("%s/combo_%s_DL.txt" % (card_location, str(era)))

card_all_eras += ">  combo_all_eras_DL.txt"
runCombineCmd(card_all_eras, card_location)
print  ("%s/combo_all_eras_DL.txt" % (card_location))
