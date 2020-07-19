#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import ROOT
import shutil
import sys, os, re, shlex
from subprocess import Popen, PIPE

import os.path
from os import path

from CombineHarvester.ttH_htt.data_manager import manipulate_cards, lists_overlap, construct_templates, list_proc, make_threshold, checkSyst, check_systematics
sys.stdout.flush()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputShapes",    type="string",       dest="inputShapes", help="Full path of prepareDatacards.root")
parser.add_option("--channel",        type="string",       dest="channel",     help="Channel to assume (to get the correct set of syst)")
parser.add_option("--cardFolder",     type="string",       dest="cardFolder",  help="Folder where to save the datacards (relative or full).\n Default: teste_datacards",  default="teste_datacards")
parser.add_option("--analysis",       type="string",       dest="analysis",    help="Analysis type = 'ttH' or 'HH' (to know what to take as Higgs procs and naming convention of systematics), Default ttH", default="ttH")
parser.add_option("--output_file",    type="string",       dest="output_file", help="Name of the output file.\n Default: the same of the input, substituing 'prepareDatacards' by 'datacard' (+ the coupling if the --couplings is used)", default="none")
parser.add_option("--coupling",       type="string",       dest="coupling",    help="Coupling to take in tH.\n Default: do for SM, do not add couplings on output naming convention", default="none")
parser.add_option("--shapeSyst",      action="store_true", dest="shapeSyst",   help="Do apply the shape systematics. Default: False", default=False)
parser.add_option("--noX_prefix",     action="store_true", dest="noX_prefix",  help="do not assume hist from prepareDatacards starts with 'x_' prefix", default=False)
parser.add_option("--only_ttH_sig",   action="store_true", dest="only_ttH_sig",help="consider only ttH as signal on the datacard -- for single channel tests", default=False)
parser.add_option("--only_tHq_sig",   action="store_true", dest="only_tHq_sig",help="consider only ttH as signal on the datacard -- for single channel tests", default=False)
parser.add_option("--only_BKG_sig",   action="store_true", dest="only_BKG_sig",help="consider only ttH as signal on the datacard -- for single channel tests", default=False)
parser.add_option("--use_Exptl_HiggsBR_Uncs",   action="store_true", dest="use_Exptl_HiggsBR_Uncs",help="Use the exprimental measured Higgs BR Unc.s instead of theoretical ones", default=False)
parser.add_option("--no_data",        action="store_true", dest="no_data",     help="Do not read data_obs, fill it as it would be the sum of the processes (some combine checks ask for it)", default=False)
parser.add_option("--fake_mc",        action="store_true", dest="fake_mc",     help="Use fakes and flips from MC", default=False)
parser.add_option("--era",            type="int",          dest="era",         help="Era to consider (important for list of systematics). Default: 2017",  default=2017)
parser.add_option("--tH_kin",         action="store_true", dest="tH_kin",      help="Cards for studies with tH kinematics have specifics", default=False)
parser.add_option("--HH_kin",         action="store_true", dest="HH_kin",      help="Cards for studies with HH kinematics have specifics", default=False)
parser.add_option("--stxs",           action="store_true", dest="stxs",        help="Cards for stxs", default=False)

(options, args) = parser.parse_args()

inputShapesRaw = options.inputShapes
inputShapes = inputShapesRaw.replace(".root", "_mod.root")
channel     = options.channel
era         = options.era
shape       = options.shapeSyst
analysis    = options.analysis
cardFolder  = options.cardFolder
coupling    = options.coupling
noX_prefix  = options.noX_prefix
only_ttH_sig = options.only_ttH_sig
only_tHq_sig = options.only_tHq_sig
only_BKG_sig = options.only_BKG_sig
fake_mc      = options.fake_mc
no_data      = options.no_data
stxs         = options.stxs
tH_kin       = options.tH_kin
HH_kin       = options.HH_kin
use_Exptl_HiggsBR_Uncs = options.use_Exptl_HiggsBR_Uncs

# output the card
if options.output_file == "none" :
    output_file = cardFolder + "/" + str(os.path.basename(inputShapes)).replace(".root","").replace("prepareDatacards", "datacard")
else :
    output_file = options.output_file

if use_Exptl_HiggsBR_Uncs:
    print("Using Experimental Unc.s on Higgs BRs")
else:
    print("Using Theoretical Unc.s on Higgs BRs")

if not os.path.exists(cardFolder):
    os.makedirs(cardFolder)

syst_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/list_syst.py"
execfile(syst_file)
print ("syst values and channels options taken from: " +  syst_file)

info_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/list_channels.py"
execfile(info_file)
print ("list of signals/bkgs by channel taken from: " +  info_file)

higgs_procs = list_channels(analysis, fake_mc)["higgs_procs"]
list_channel_opt   = list_channels(analysis, fake_mc)["info_bkg_channel"]
bkg_proc_from_data = list_channel_opt[channel]["bkg_proc_from_data"]
bkg_procs_from_MC  = list_channel_opt[channel]["bkg_procs_from_MC"]

# if a coupling is done read the tH signal with that coupling on naming convention
if not (coupling == "none" or coupling == "kt_1_kv_1") :
    higgs_procs = [ [ entry.replace("tHq_", "tHq_%s_" % coupling).replace("tHW_", "tHW_%s_" % coupling) for entry in entries ] for entries in higgs_procs ]

print higgs_procs
higgs_procs_plain = sum(higgs_procs,[])

if only_ttH_sig :
    print ("MC processes -- after chosing to mark as signal only ttH:")
    bkg_procs_from_MC += [ entry for entry in higgs_procs_plain if "ttH_" not in  entry]
    higgs_procs        = [ entries for entries in higgs_procs if "ttH_" in entries[0] ]
    print ("BKG from MC   (new): ", bkg_procs_from_MC)
    print ("signal        (new): ", higgs_procs)
    higgs_procs_plain = sum(higgs_procs,[])
elif only_tHq_sig :
    print ("MC processes -- after chosing to mark as signal only ttH:")
    bkg_procs_from_MC += [ entry for entry in higgs_procs_plain if "tHq_" not in  entry]
    higgs_procs        = [ entries for entries in higgs_procs if "tHq_" in entries[0] ]
    print ("BKG from MC   (new): ", bkg_procs_from_MC)
    print ("signal        (new): ", higgs_procs)
    higgs_procs_plain = sum(higgs_procs,[])
elif only_BKG_sig :
    print ("MC processes -- after chosing to mark as signal only ttH:")
    bkg_procs_from_MC = [ entry for entry in bkg_procs_from_MC if not "TTW" in entry and not "TTZ" in entry ]
    bkg_procs_from_MC += sum(higgs_procs,[])
    #higgs_procs        = [ entries for entries in bkg_procs_from_MC if "TTW" in entry or "TTZ" in entry ]
    print ("BKG from MC   (new): ", bkg_procs_from_MC)
    print ("signal        (new): ", ["TTW", "TTZ"])
    higgs_procs_plain = ["TTW", "TTZ"] #higgs_procs

if tH_kin :
    print ("HH should not be marked as process")
    bkg_procs_from_MC += [ entry for entry in higgs_procs_plain if "HH" in  entry]
    higgs_procs        = [ entries for entries in higgs_procs if not "HH" in entries[0] ]
    print ("BKG from MC   (new): ", bkg_procs_from_MC)
    print ("signal        (new): ", higgs_procs)
    higgs_procs_plain = sum(higgs_procs,[])

pT_bins = {}
if stxs :
    # take ttH_ as the pT bins
    """
    BIN                2016      2017      2018
    -------------------------------------------
    fwd          -> 0.00252   0.00237   0.00260
    pt0to60      -> 0.04617   0.04556   0.04486
    pt120to200   -> 0.05107   0.05146   0.05166
    pt200to300   -> 0.02127   0.02147   0.02189
    pt300to450   -> 0.00767   0.00779   0.00799
    pt60to120    -> 0.07115   0.07108   0.07039
    ptGt300      -> 0.00981   0.00993   0.01020
    ptGt450      -> 0.00214   0.00214   0.00220
    """
    pT_bins            = {
        # pT bin           XS (now the cards are done normalizing ttH in each pT bin is normalized to 1pb)
        "PTH_fwd"       : (0.00252 + 0.00237 + 0.00260)/3.,
        "PTH_0_60"      : (0.04617 + 0.04556 + 0.04486)/3.,
        "PTH_60_120"    : (0.07115 + 0.07108 + 0.07039)/3.,
        "PTH_120_200"   : (0.05107 + 0.05146 + 0.05166)/3.,
        "PTH_200_300"   : (0.02127 + 0.02147 + 0.02189)/3.,
        "PTH_300_infty" : (0.00981 + 0.00993 + 0.01020)/3.
    }
    all_ttH_proc       = ["ttH_htt", "ttH_hww", "ttH_hzz", "ttH_hmm", "ttH_hzg"]
    higgs_procs_plain        = list(set(higgs_procs_plain) - set(all_ttH_proc))
    for pTs in list(pT_bins.keys()) :
      for ttH_proc in all_ttH_proc :
        higgs_procs_plain   = higgs_procs_plain + [ ttH_proc.replace("ttH", "ttH_" + pTs) ]
    print ("higgs_procs == ", higgs_procs_plain)

print ("Do not allow Zero shape systematics variations")
if not path.exists(inputShapes) : # and (tH_kin or HH_kin)
    print("inputShapes = ", inputShapes)
    shutil.copy2(inputShapesRaw, inputShapes)
    print ("\n copied \n %s to \n %s \nto make modifications in problematic bins." % (inputShapesRaw, inputShapes))
    check_systematics(inputShapes, coupling, pT_bins)
    #sys.exit()
else :
    print ("file %s already modified" % inputShapes)

# check a threshold on processes
print ("do not add a process to datacard if the yield is smaller than 0.01")
bkg_proc_from_data = make_threshold(0.01, bkg_proc_from_data,  inputShapes, tH_kin)
bkg_procs_from_MC  = make_threshold(0.01, bkg_procs_from_MC, inputShapes, tH_kin)
higgs_procs_plain  = make_threshold(0.01, higgs_procs_plain, inputShapes, tH_kin)

print ("final list of signal/bkg to add to datacards")
MC_proc = higgs_procs_plain + bkg_procs_from_MC
print ("MC processes:")
print ("BKG from MC  (original)  : ", bkg_procs_from_MC)
print ("BKG from data (original) : ", bkg_proc_from_data)
print ("signal        (original): ", higgs_procs_plain)

specific_syst_list = specific_syst(analysis, list_channel_opt)
print("analysis type        :", analysis)

removeProcs = True
try :
    print (list_channel_opt[channel]["proc_to_remove"][str(era)])
except :
    removeProcs = False

if removeProcs :
    removeProcslist = list_channel_opt[channel]["proc_to_remove"][str(era)]
    if not (coupling == "none" or coupling == "kt_1_kv_1") :
        removeProcslist = [nn.replace("tHq_", "tHq_%s_" % coupling).replace("tHW_", "tHW_%s_" % coupling) for nn in list(removeProcslist) if "tHW" in nn or "tHq" in nn]
    if len(removeProcslist) > 0 :
        print("Removing processes where systematics blow up (found by hand a posteriory using the list hardcoded on configs/list_channels.py)")
        higgs_procs_plain = list(set(list(higgs_procs_plain)) - set(list(removeProcslist)))
        print ("New list of Higgs processes", higgs_procs_plain)
        print ("Removed", list_channel_opt[channel]["proc_to_remove"][str(era)])

###########################################
# start the list of common systematics for all channels
###########################################

cb = ch.CombineHarvester()
cats = [
    (1, "%s_%s" % (analysis, channel))
    ]
masses = ["*"]
if not no_data :
    cb.AddObservations(["*"], ["%sl" % analysis], ["13TeV"], ["*"], cats)
cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], bkg_proc_from_data + bkg_procs_from_MC, cats, False)
cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], higgs_procs_plain, cats, True)

#######################################
print ("Adding lumi syt uncorrelated/year")
# check if we keep the lumis/era correlated or not
cb.cp().process(bkg_procs_from_MC + higgs_procs_plain).AddSyst(cb, "lumi_13TeV_%s" % str(era), "lnN", ch.SystMap()(lumiSyst[era]))
cb.cp().process(bkg_procs_from_MC + higgs_procs_plain).AddSyst(cb, "lumi_13TeV_XY", "lnN", ch.SystMap()(lumi_2016_2017_2018[era]))
if era in [2017, 2018] :
    cb.cp().process(bkg_procs_from_MC + higgs_procs_plain).AddSyst(cb, "lumi_13TeV_LS",  "lnN", ch.SystMap()(lumi_2017_2018[era]))
    cb.cp().process(bkg_procs_from_MC + higgs_procs_plain).AddSyst(cb, "lumi_13TeV_BCC", "lnN", ch.SystMap()(lumi_13TeV_BCC[era]))
if era in [2017, 2016] :
    cb.cp().process(bkg_procs_from_MC + higgs_procs_plain).AddSyst(cb, "lumi_13TeV_BBD", "lnN", ch.SystMap()(lumi_2016_2017[era]))
    cb.cp().process(bkg_procs_from_MC + higgs_procs_plain).AddSyst(cb, "lumi_13TeV_DB",  "lnN", ch.SystMap()(lumi_13TeV_DB[era]))
    cb.cp().process(bkg_procs_from_MC + higgs_procs_plain).AddSyst(cb, "lumi_13TeV_GS",  "lnN", ch.SystMap()(lumi_13TeV_GS[era]))


#######################################
# FIXME: one of the syst is logUniform -- fix
if 0 > 1 : # FIXME: remind why we added that at some point
    print ("Adding rateParam")
    # normalizations floating individually (ttWW correlated with ttW and among signal types)
    # not relevant if you do the fit expliciting things on the text2ws maker -- but it does not hurt
    for proc in bkg_procs_from_MC  :
        if "TTWW" in proc :
            cb.cp().process([proc]).AddSyst(cb, 'scale_TTWW', 'rateParam', ch.SystMap()(("(@0)", "scale_TTW")))
            print ("process: " + proc + " is proportonal to TTW")
        else :
            cb.cp().process([proc]).AddSyst(cb, "scale_%s" % proc, 'rateParam', ch.SystMap()(1.0))
            print ("added rateparam to: " + proc)

    # correlate the rateparam among the Higgs processes
    for hsig in higgs_procs :
        for br, hsbr in enumerate(hsig) :
            if br == 0 :
                cb.cp().process([hsbr]).AddSyst(cb, "scale_%s" % hsbr, 'rateParam', ch.SystMap()(1.0))
                print ("added rateparam to: " + hsbr)
            else :
                cb.cp().process([proc]).AddSyst(cb, 'scale_%s' % hsbr, 'rateParam', ch.SystMap()(("(@0)", "scale_%s" % hsig[0])))
                print ("process: " + hsbr + " is proportonal to", hsig[0])

########################################
# add theory systematics
for specific_syst in theory_ln_Syst :
    procs = theory_ln_Syst[specific_syst]["proc"]
    if len(procs) == 0 :
        continue
    if "HH" in procs[0] :
        for decay in list_channels(analysis, fake_mc)["decays_hh"] :
            procs = procs + [procs[0] + decay]
    elif "H" in procs[0] and analysis == "ttH":
        if tH_kin and ("tHq" in procs[0] or "tHW" in procs[0]) :
            continue
        for decay in list_channels(analysis, fake_mc)["decays"] :
            procs = procs + [procs[0] + decay]
    else :
        if procs[0] not in bkg_procs_from_MC :
            continue
    if specific_syst == "pdf_qg_2" :
        specific_syst_use = "pdf_qg"
    else :
        specific_syst_use = specific_syst
    cb.cp().process(procs).AddSyst(cb,  specific_syst_use, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", procs)

if analysis == "HH" or 1 > 0 :
    ### Uniformize those names at some point
    #"pdf_HH"                      : {"value": 1.04,               "proc" : ["HH"]},
    #"QCDscale_HH"                 : {"value": (0.95 , 1.022),     "proc" : ["HH"]},
    #"TopmassUnc_HH"               : {"value": 1.026,              "proc" : ["HH"]},
    #"pdf_Higgs_ttH"               : {"value": 1.036,              "proc" : ["ttH"]},
    #"QCDscale_ttH"                : {"value": (0.907 , 1.058),    "proc" : ["ttH"]},
    #"pdf_qg"                      : {"value": 1.01,               "proc" : ["tHq"]},
    #"QCDscale_tHq"                : {"value": (0.933, 1.041),     "proc" : ["tHq"]},
    #"QCDscale_WH"                 : {"value": (0.95 , 1.07),      "proc" : ["WH"]},
    #"pdf_WH"                      : {"value": 1.019,              "proc" : ["WH"]},

    specific_syst == "pdf_HH"
    cb.cp().process(higgs_procs_plain).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", higgs_procs_plain)

    specific_syst = "QCDscale_HH"
    cb.cp().process(higgs_procs_plain).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", higgs_procs_plain)

    specific_syst = "TopmassUnc_HH"
    cb.cp().process(higgs_procs_plain).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", higgs_procs_plain)

    specific_syst = "pdf_Higgs_ttH"
    cb.cp().process(["TTH"]).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", ["TTH"])

    specific_syst = "QCDscale_ttH"
    cb.cp().process(["TTH"]).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", ["TTH"])

    specific_syst = "pdf_qg"
    cb.cp().process(["TH"]).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", ["TH"])

    specific_syst = "QCDscale_tHq"
    cb.cp().process(["TH"]).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", ["TH"])

    specific_syst = "QCDscale_WH"
    cb.cp().process(["VH"]).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", ["VH"])

    specific_syst = "pdf_WH"
    cb.cp().process(["VH"]).AddSyst(cb,  specific_syst, "lnN", ch.SystMap()(theory_ln_Syst[specific_syst]["value"]))
    print ("added " + specific_syst + " with value " + str(theory_ln_Syst[specific_syst]["value"]) + " to processes: ", ["VH"])


########################################
# BR syst
for proc in higgs_procs_plain :
    if use_Exptl_HiggsBR_Uncs: BRs = higgsBR_exptl
    else :  BRs = higgsBR_theo
    for key in BRs:
        if key in proc :
            cb.cp().process([proc]).AddSyst(cb, "BR_%s" % key, "lnN", ch.SystMap()(BRs[key]))
            print ("added " + "BR_%s" % key + " uncertanity to process: " + proc + " of value = " + str(BRs[key]))
    if "ttH" in proc or "ZH" in proc or "WH" in proc :
        key = "hbb"
        cb.cp().process([proc]).AddSyst(cb, "BR_%s" % key, "lnN", ch.SystMap()(BRs[key]))
        print ("added " + "BR_%s" % key + " uncertanity to process: " + proc + " of value = " + str(BRs[key]))

########################################
# specifics for cards with tH-kinematics
if tH_kin and analysis == "ttH": # [k for k,v in list_channel_opt.items()
    MC_proc = [ procc.replace(coupling+"_", "") for procc in MC_proc ]
    print (coupling+"_", "MC_proc", MC_proc)
    for proc in ["TTW", "TTZ"] :
        cb.cp().process([proc]).AddSyst(cb, "CMS_ttHl_%s_lnU" % proc, "lnU", ch.SystMap()(3.0))
        print ("added", "CMS_ttHl_%s_lnU" % proc)
    from CombineHarvester.ttH_htt.data_manager import extract_thu
    for proc in ["tHq", "tHW"] :
        # https://twiki.cern.ch/twiki/pub/CMS/SingleTopHiggsGeneration13TeV/tHQ_cross_sections.txt
        # https://twiki.cern.ch/twiki/pub/CMS/SingleTopHiggsGeneration13TeV/tHW_cross_sections.txt
        thuncertainty = extract_thu(proc, coupling)
        if coupling == "kt_1_kv_1" :
            procdecays = [proc + "_htt" , proc + "_hzz", proc + "_hww"]
        else :
            procdecays = [proc + "_" + coupling + "_htt" , proc + "_" + coupling + "_hzz", proc + "_" + coupling + "_hww"]
        cb.cp().process(procdecays).AddSyst(cb, "pdf_qg", "lnN", ch.SystMap()(thuncertainty["pdf"]))
        print ("added", "pdf_qg" , thuncertainty["pdf"], procdecays)
        cb.cp().process(procdecays).AddSyst(cb, "QCDscale_qg", "lnN", ch.SystMap()((thuncertainty["qcddo"], thuncertainty["qcdup"])))
        print ("added", "QCDscale_qg", (thuncertainty["qcddo"], thuncertainty["qcdup"]), procdecays)

########################################
if shape :
    ########################################
    # MC estimated shape syst
    #for MC_shape_syst in MC_shape_systs_uncorrelated + MC_shape_systs_correlated + JES_shape_systs_Uncorrelated :
    #    if era == 2018 and MC_shape_syst == "CMS_ttHl_l1PreFire" : continue
    #    cb.cp().process(MC_proc).AddSyst(cb,  MC_shape_syst, "shape", ch.SystMap()(1.0))
    #    print ("added " + MC_shape_syst + " as shape uncertainty to the MC processes")
    ########################################
    # channel specific estimated shape syst
    specific_shape_systs = specific_syst_list["specific_shape"]
    print("specific_shape_systs", specific_syst_list['specific_shape_to_shape_systs'])
    for specific_syst in specific_shape_systs :
        if era == 2018 and specific_syst == "CMS_ttHl_l1PreFire" :
            continue
        #if "SS" in output_file and ("JER" in specific_syst or "JES" in specific_syst ) and not ( "HEM" in specific_syst )  :
        #    continue
        if ( "HEM" in specific_syst ) and era != 2018:
            print ("skkiping ", specific_syst, "as it is not era 2018")
            continue
        if "HEM" in specific_syst and stxs :
            continue
        if (specific_syst == "CMS_ttHl_Clos_e_shape") and era != 2018:
            continue
        if channel not in specific_shape_systs[specific_syst]["channels"] :
            if ( "HEM" in specific_syst ) : print ("WTF", specific_shape_systs[specific_syst]["channels"])
            continue
        #if specific_shape_systs[specific_syst]["proc"] == "MCproc" :
        #    applyTo = MC_proc
        #else :
        #    applyTo = specific_shape_systs[specific_syst]["proc"]
        procs = list_proc(specific_shape_systs[specific_syst], MC_proc, bkg_proc_from_data + bkg_procs_from_MC, specific_syst)
        # that above take the overlap of the lists
        if len(procs) == 0 :
            continue
        cb.cp().process(procs).AddSyst(cb,  specific_syst, "shape", ch.SystMap()(1.0))
        print ("added " + specific_syst + " as shape uncertainty to ", procs)

########################################
# Specific channels lnN syst
specific_ln_systs  = specific_syst_list["specific_ln_systs"]
for specific_syst in specific_ln_systs :
    if channel not in specific_ln_systs[specific_syst]["channels"] :
        print ("Skipped ", specific_syst , " in ", channel)
        continue
    procs = list_proc(specific_ln_systs[specific_syst], MC_proc, bkg_proc_from_data + bkg_procs_from_MC, specific_syst)
    if len(procs) == 0 :
        continue
    name_syst = specific_syst
    if not specific_ln_systs[specific_syst]["correlated"] :
        name_syst = specific_syst.replace("%sl" % analysis, "%sl%s" % (analysis, str(era - 2000)))
        # assuming that the syst for the HH analysis with have the label HHl
    if not analysis == "HH" :
        if "lnU" in name_syst :
            cb.cp().process(procs).AddSyst(cb,  name_syst, "lnU", ch.SystMap()(specific_ln_systs[specific_syst]["value"]))
        else :
            cb.cp().process(procs).AddSyst(cb,  name_syst, "lnN", ch.SystMap()(specific_ln_systs[specific_syst]["value"]))
    else :
        cb.cp().process(procs).AddSyst(cb,  name_syst, "lnN", ch.SystMap()(specific_ln_systs[specific_syst]["value"]))
    print ("added " + name_syst + " with value " + str(specific_ln_systs[specific_syst]["value"]) + " to processes: ",  specific_ln_systs[specific_syst]["proc"] )

########################################
finalFile = inputShapes
if list_channel_opt[channel]["isSMCSplit"] :
    print ("Construct templates for fake/gentau systematics:")
    specific_ln_shape_systs    = specific_syst_list["specific_ln_to_shape_systs"]
    specific_shape_shape_systs = specific_syst_list["specific_shape_to_shape_systs"]
    finalFile = construct_templates(cb, ch, specific_ln_shape_systs, specific_shape_shape_systs, inputShapes , MC_proc, shape, noX_prefix )

########################################
# bin by bin stat syst
cb.cp().SetAutoMCStats(cb, 10)

if noX_prefix :
    cb.cp().backgrounds().ExtractShapes(
        finalFile,
        "$PROCESS",
        "$PROCESS_$SYSTEMATIC")
    cb.cp().signals().ExtractShapes(
        finalFile,
        "$PROCESS",
        "$PROCESS_$SYSTEMATIC")
else :
    cb.cp().backgrounds().ExtractShapes(
        finalFile,
        "x_$PROCESS",
        "x_$PROCESS_$SYSTEMATIC")
    cb.cp().signals().ExtractShapes(
        finalFile,
        "x_$PROCESS",
        "x_$PROCESS_$SYSTEMATIC")
########################################
# rename some shape systematics according to era to keep them uncorrelated
if shape :
    ########################################
    if list_channel_opt[channel]["isSMCSplit"] :
        MC_proc_less = list(set(list(MC_proc)) - set(["Convs"]))
        for shape_syst in specific_syst_list["created_shape_to_shape_syst"] :
            MC_shape_syst = shape_syst.replace("CMS_constructed_", "CMS_")
            cb.cp().process(MC_proc_less).RenameSystematic(cb, shape_syst, MC_shape_syst)
            print ("renamed " + shape_syst + " to " +  MC_shape_syst + " to the MC processes ")
            if "tauES" in shape_syst :
                MC_shape_syst_era_3 = "CMS_scale_t_Era".replace("Era", str(era))
                cb.cp().process(MC_proc_less).RenameSystematic(cb, MC_shape_syst, MC_shape_syst_era_3)
                print ("renamed " + MC_shape_syst + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era_3)
            elif "tauID" in shape_syst :
                MC_shape_syst_era_3 = "CMS_eff_t_Era".replace("Era", str(era))
                cb.cp().process(MC_proc_less).RenameSystematic(cb, MC_shape_syst, MC_shape_syst_era_3)
                print ("renamed " + MC_shape_syst + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era_3)
            else :
                MC_shape_syst_era_2 = MC_shape_syst.replace("CMS_ttHl", "CMS_ttHl%s" % str(era).replace("20","")).replace("Era", str(era))
                cb.cp().process(MC_proc_less).RenameSystematic(cb, MC_shape_syst, MC_shape_syst_era_2)
                print ("renamed " + MC_shape_syst + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era_2)
    ##################################
    for specific_syst in specific_shape_systs :
        if channel not in specific_shape_systs[specific_syst]["channels"] :
            continue
        if era == 2018 and specific_syst == "CMS_ttHl_l1PreFire" :
            continue
        #if "SS" in output_file and ("JER" in specific_syst or "JES" in specific_syst ) :
        #    continue
        if ( "HEM" in specific_syst ) and era != 2018 :
            print ("skkiping ", specific_syst, "as it is not era 2018")
        if "HEM" in specific_syst and stxs :
            continue
        if specific_shape_systs[specific_syst]["correlated"] and specific_shape_systs[specific_syst]["renameTo"] == None :
            continue
        #################
        procs = list_proc(specific_shape_systs[specific_syst], MC_proc, bkg_proc_from_data + bkg_procs_from_MC, specific_syst)
        # that above take the overlap of the lists
        if len(procs) == 0 :
            continue
        #################
        if not specific_shape_systs[specific_syst]["renameTo"] == None :
            MC_shape_syst_era = specific_shape_systs[specific_syst]["renameTo"]
            cb.cp().process(procs).RenameSystematic(cb, specific_syst, MC_shape_syst_era)
            print ("renamed " + specific_syst + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era)
        else :
            MC_shape_syst_era = specific_syst
        if not specific_shape_systs[specific_syst]["correlated"] :
            MC_shape_syst_era_2 = MC_shape_syst_era.replace("CMS_ttHl", "CMS_ttHl%s" % str(era).replace("20","")).replace("Era", str(era))
            cb.cp().process(procs).RenameSystematic(cb, MC_shape_syst_era, MC_shape_syst_era_2)
            print ("renamed " + MC_shape_syst_era + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era_2)
        else :
            MC_shape_syst_era_2 = MC_shape_syst_era
        ###################
        if specific_syst == "CMS_ttHl_trigger" :
            if channel in ["1l_2tau", "1l_1tau"] :
                MC_shape_syst_era_3 = MC_shape_syst_era_2 + "_leptau"
            elif channel in ["0l_2tau"] :
                MC_shape_syst_era_3 = MC_shape_syst_era_2 + "_tau"
            else :
                MC_shape_syst_era_3 = MC_shape_syst_era_2 + "_" + channel
            cb.cp().process(procs).RenameSystematic(cb, MC_shape_syst_era_2, MC_shape_syst_era_3)
            print ("renamed " + MC_shape_syst_era_2 + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era_3)
        if  "Clos_t_norm" in specific_syst or  "Clos_t_shape" in specific_syst:
            MC_shape_syst_era_3 = MC_shape_syst_era_2 + "_" + channel
            cb.cp().process(procs).RenameSystematic(cb, MC_shape_syst_era_2, MC_shape_syst_era_3)
            print ("renamed " + MC_shape_syst_era_2 + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era_3)

########################################

bins = cb.bin_set()
for b in bins :
    print ("\n Output file: " + output_file + ".txt", b )
    cb.cp().bin([b]).mass(["*"]).WriteDatacard(output_file + ".txt" , output_file + ".root")

if no_data :
    print("Making data_obs as the asimov in SM if asked to do so")
    manipulate_cards(output_file, "none", bins, no_data, bkg_procs_from_MC+higgs_procs_plain+bkg_proc_from_data, inputShapes)

if not (coupling == "none" or coupling == "kt_1_kv_1") :
    print("Renaming tH processes (remove the coupling mention to combime)")
    manipulate_cards(output_file, coupling, bins, no_data, bkg_procs_from_MC+higgs_procs_plain+bkg_proc_from_data, inputShapes)

sys.stdout.flush()
