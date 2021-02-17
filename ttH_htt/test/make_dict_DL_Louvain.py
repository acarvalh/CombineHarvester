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
    "--fitdiag_folder",
    dest="fitdiag_folder",
    help="Folder that contain the fitdiagnosis.root file(s)",
    )
parser.add_argument(
    "--output_dict",
    dest="output_dict",
    help="Full path for output Dictionary",
    )
args = parser.parse_args()



list_SL_cards = [
    [
        "DY_VVVnode",
        ["DY_VVVnode"],
        "[[\" \"]]",
        "[0]",
        "DY + VVV node"
    ],
    [
        "TT_ST_TTVX_Rarenode",
        ["TT_ST_TTVX_Rarenode"],
        "[ [\" \"] ]",
        "[2.5]",
        "TT + ST + TTVX + Rare node"
    ],
    [
        "GGFnode",
        ["resolved1b_GGFnode", "resolved2b_GGFnode", "boosted1b_GGFnode" ],
        "[[\"res 1b\"], [\"res 2b\"], [\"b.\"]]",
        "[8, 23, 30]",
        "GGF HH node"
    ],
    [
        "VBFnode",
        ["resolved1b_VBFnode", "resolved2b_VBFnode", "boosted1b_VBFnode", ],
        "[[\"res 1b\"], [\"res 2b\"], [\"b.\"]]",
        "[2, 8, 12.5]",
        "VBF HH node"
    ],
    [
        "Hnode",
        [ "resolved1b_Hnode", "resolved2b_Hnode", "boosted1b_Hnode",],
        "[[\"res 1b\"], [\"res 2b\"], [\"boosted\"], ]",
        "[1, 5, 10]",
        "single H node"
    ],
]
fitdiagDL = args.fitdiag_folder

for node in ["Hnode", "GGFnode", "VBFnode"] :
    local_merged = "%s/fitDiagnostics_shapes_combine_%s_2018.root" % (fitdiagDL, node)
    if not os.path.exists(local_merged) :
        cmd = "hadd fitDiagnostics_shapes_combine_%s_2018.root fitDiagnostics_shapes_combine_*_%s_2018.root" % (node, node)
        print ("cd %s ; %s; cd -" % (fitdiagDL, cmd))
        proc=subprocess.Popen(["cd %s ; %s" % (fitdiagDL, cmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    else :
        print ("file %s already exists" % local_merged )

dictionary = args.output_dict #"%s/dict_SL.dat" % fitdiagDL
ff = open(dictionary, "w")
ff.write(unicode('{\n'))

for tt, teste_class in enumerate(list_SL_cards) :
    for ee, era in enumerate([2016, 2017, 2018]) :
        #if teste_class[0] in ["Hnode", "GGFnode", "VBFnode"] :
        #    continue
        if not era == 2018 :
            continue
        print(teste_class[0])
        ff.write(unicode("    \"%s_%s\" : {\n" % (teste_class[0], str(era))))
        ff.write(unicode("        \"fitdiagnosis\"       : \"%s/fitDiagnostics_shapes_combine_%s_%s.root\",\n" % (fitdiagDL, teste_class[0], str(era)) ))
        ff.write(unicode("        \"bin_name_original\"  : \"none\",\n" ))
        ff.write(unicode("        \"datacard_original\"  : \"none\",\n" ))
        ff.write(unicode("        \"minY\"               : 0.1,\n" ))
        ff.write(unicode("        \"maxY\"               : 100000000000.,\n" ))
        ff.write(unicode("        \"minYerr\"            : -0.28,\n" ))
        ff.write(unicode("        \"maxYerr\"            : 0.28,\n" ))
        ff.write(unicode("        \"useLogPlot\"         : True,\n" ))
        ff.write(unicode("        \"era\"                : %s ,\n" % str(era) ))
        ff.write(unicode("        \"labelX\"             : \"MVA bin #\",\n" ))
        ff.write(unicode("        \"header_legend\"          : \"%s\",\n"  % teste_class[4] ))
        ff.write(unicode("        \"number_columns_legend\" : 3,\n" ))
        align_cats_string = "        \"align_cats\" : ["
        #ff.write(unicode("        \"align_cats\" : [ \"mumu_%s_%s\", \"emu_%s_%s\", \"ee_%s_%s\"],\n" % (teste_class, str(era), teste_class, str(era), teste_class, str(era)) ))
        for catsbins in teste_class[1] :
            align_cats_string  = align_cats_string + "\"" + catsbins + "_" +str(era) + "\","
        align_cats_string = align_cats_string + "],\n"
        ff.write(unicode(align_cats_string ))

        ff.write(unicode("        \"align_cats_labels\" : %s,\n" % teste_class[2] ))
        ff.write(unicode("        \"align_cats_labelsX\" : %s,\n" % teste_class[3] ))
        ff.write(unicode("        \"cats_labels_height\" : 1000000.,\n" ))
        ff.write(unicode("        \"single_H_major\" : \"ttH_hww\",\n" ))
        ff.write(unicode("        \"procs_plot_options_bkg\" : OrderedDict(\n" ))
        ff.write(unicode("            [\n" ))
        ff.write(unicode("            (\"Other_bbWW\",       {\"color\" : 205, \"fillStype\"   : 1001, \"label\" : \"others\"           , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"VV\",          {\"color\" : 823, \"fillStype\"   : 1001, \"label\" : \"ZZ + WZ\"          , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"VVV\",          {\"color\" : 6, \"fillStype\"   : 1001, \"label\" : \"VVV\"          , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"ST\",         {\"color\" : 822, \"fillStype\" : 1001, \"label\" : \"single top\"         , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"Fakes\",  {\"color\" :  12, \"fillStype\" : 3345, \"label\" : \"Fakes\"  , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"DY\",          {\"color\" : 221, \"fillStype\" : 1001, \"label\" : \"DY\"         , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"WJets\",           {\"color\" : 5, \"fillStype\" : 1001, \"label\" : 'W + jets'   , \"make border\" : True}),\n" ))
        ff.write(unicode("            (\"TT\",          {\"color\" : 17, \"fillStype\"  : 1001, \"label\" : 't#bar{t} + jets'   , \"make border\" : True})\n" ))
        ff.write(unicode("            ]\n" ))
        ff.write(unicode("        ),\n" ))
        ff.write(unicode("        \"procs_plot_options_sig\" : OrderedDict(\n" ))
        ff.write(unicode("            [\n" ))
        ff.write(unicode("            ( \"GGF_SM\",\n" ))
        ff.write(unicode("              {\n" ))
        ff.write(unicode("              \"processes\" : [\"ggHH_kl_1_kt_1_hbbhww2l\", \"ggHH_kl_1_kt_1_hbbhtt\"],\n" ))
        ff.write(unicode("              \"color\" : 5, \"fillStype\"  : 3351, \"label\" : 'GGF HH SM', \"scaleBy\" : 1.\n" ))
        ff.write(unicode("              }\n" ))
        ff.write(unicode("            ),\n" ))
        ff.write(unicode("            ( \"GGF_kl5\",\n" ))
        ff.write(unicode("              {\n" ))
        ff.write(unicode("              \"processes\" : [\"ggHH_kl_5_kt_1_hbbhww2l\", \"ggHH_kl_5_kt_1_hbbhtt\"],\n" ))
        ff.write(unicode("              \"color\" : 221, \"fillStype\"  : 3351, \"label\" : 'GGF HH #kappa#lambda = 5', \"scaleBy\" : 1.\n" ))
        ff.write(unicode("              }\n" ))
        ff.write(unicode("            ),\n" ))
        ff.write(unicode("            ( \"GGF_kl2p45\",\n" ))
        ff.write(unicode("              {\n" ))
        ff.write(unicode("              \"processes\" : [\"ggHH_kl_2p45_kt_1_hbbhww2l\", \"ggHH_kl_2p45_kt_1_hbbhtt\"],\n" ))
        ff.write(unicode("              \"color\" : 2, \"fillStype\"  : 3351, \"label\" : 'GGF HH #kappa#lambda = 2.45', \"scaleBy\" : 1.\n" ))
        ff.write(unicode("              }\n" ))
        ff.write(unicode("            ),\n" ))
        ff.write(unicode("            ( \"VBF_SM\",\n" ))
        ff.write(unicode("              {\n" ))
        ff.write(unicode("              \"processes\" : [\"qqHH_CV_1_C2V_1_kl_1_hbbhtt\", \"qqHH_CV_1_C2V_1_kl_1_hbbhww2l\"],\n" ))
        ff.write(unicode("              \"color\" : 8, \"fillStype\"  : 3351, \"label\" : 'VBF HH SM', \"scaleBy\" : 1.\n" ))
        ff.write(unicode("              }\n" ))
        ff.write(unicode("            )\n" ))
        ff.write(unicode("            ]\n" ))
        ff.write(unicode("        ),\n" ))
        ff.write(unicode("    },\n" ))


ff.write(unicode('}\n'))
ff.close()

print("created %s" % dictionary)
