def read_from():
    withFolder = True
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/datacards_2016_DY_datadriven/all_hbb_flavour_merged/"
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/datacards_2016_DY_MC/all_hbb_flavour_merged/"
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/datacards_2016_DY_datadriven_syst/all_hbb_flavour_merged/"
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/datacards_2016_DY_MC_syst/all_hbb_flavour_merged/"
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/step1_noHbb_noflavour_18Jan/HHDatacards/datacard_2018/all_hbb_flavour_merged/"
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/step1_noHbb_noflavour_18Jan/HHDatacards/datacard_2018/"
    # /afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/step1_noHbb_noflavour_18Jan/HHDatacards/datacard_2018/all_hbb_flavour_merged/cards/datacards_rebined/
    ####
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/dataset_fit_TTHIDLoose_DNN09_DYEstimation_2018/all_hbb_flavour_merged/"
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/dataset_fit_TTHIDLoose_DNN09_2018/all_hbb_flavour_merged/"
    ###
    #mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/dataset_fit_TTHIDLoose_DNN10_2018/all_hbb_flavour_merged_type2/"
    mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/dataset_fit_TTHIDLoose_DNN10_2018/all_hbb_flavour_merged_type4/"

    bdtTypes = [
    #"HH_cat_DNN08_DYnode_2018",
    #"HH_cat_DNN08_STnode_2018",
    #"HH_cat_DNN08_TTVXnode_2018",
    #"HH_cat_DNN08_VVVnode_2018",
    #"HH_cat_DNN08_Rarenode_2018",
    #"HH_cat_DNN08_TTnode_2018",
    #"HH_cat_DNN08_Hnode_2018",
    #"HH_cat_DNN08_VBFnode_2018",
    #"HH_cat_DNN08_GGFnode_2018",
    #"HH_cat_DNN08_TT_STnode_2018",
    #"HH_cat_DNN08_TTVX_Rarenode_2018",
    #"HH_cat_DNN08_DY_VVVnode_2018",
    #"HH_cat_DNN08_TT_ST_TTVX_Rarenode_2018",
    #"HH_cat_DNN08_TT_ST_TTVX_Rarenode_resolved1b_2018",
    #"HH_cat_DNN08_TT_ST_TTVX_Rarenode_resolved2b_2018",
    #"HH_cat_DNN08_TT_ST_TTVX_Rarenode_boosted1b_2018",
    #"HH_cat_DNN08_DY_VVVnode_resolved1b_2018",
    #"HH_cat_DNN08_DY_VVVnode_resolved2b_2018",
    #"HH_cat_DNN08_DY_VVVnode_boosted1b_2018",
    #
    #"HH_cat_boosted1b_DNN08_Hnode_2018",
    #"HH_cat_resolved1b_DNN08_Hnode_2018",
    #"HH_cat_resolved2b_DNN08_Hnode_2018",
    #"HH_cat_boosted1b_DNN08_GGFnode_2018",
    #"HH_cat_resolved1b_DNN08_GGFnode_2018",
    #"HH_cat_resolved2b_DNN08_GGFnode_2018",
    #"HH_cat_boosted1b_DNN08_VBFnode_2018",
    #"HH_cat_resolved1b_DNN08_VBFnode_2018",
    #"HH_cat_resolved2b_DNN08_VBFnode_2018",
    ########
    ##"HH_cat_ee_boosted1b_DNN08_GGFnode_2018",
    #"HH_cat_ee_resolved1b_DNN08_GGFnode_2018", # 8
    #"HH_cat_ee_resolved2b_DNN08_GGFnode_2018", # 6
    ##"HH_cat_em_boosted1b_DNN08_GGFnode_2018",
    #"HH_cat_em_resolved1b_DNN08_GGFnode_2018", # 5
    #"HH_cat_em_resolved2b_DNN08_GGFnode_2018", # 5
    ##"HH_cat_mm_boosted1b_DNN08_GGFnode_2018",
    #"HH_cat_mm_resolved1b_DNN08_GGFnode_2018", # 5
    #"HH_cat_mm_resolved2b_DNN08_GGFnode_2018", # 10
    #######
    #"HH_cat_ee_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    #"HH_cat_em_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    #"HH_cat_mm_DNN10_TT_ST_TTVX_Rarenode_2018", # 10

    #"HH_cat_ee_DNN10_DY_VVVnode_2018", # 10
    #"HH_cat_em_DNN10_DY_VVVnode_2018", # 10
    #"HH_cat_mm_DNN10_DY_VVVnode_2018", # 10

    #"HH_cat_ee_DNN10_VBFnode_2018", # 3
    #"HH_cat_em_DNN10_VBFnode_2018", # 3
    #"HH_cat_mm_DNN10_VBFnode_2018", # 3

    #"HH_cat_ee_DNN10_GGFnode_2018", # 10
    #"HH_cat_em_DNN10_GGFnode_2018", # 10
    #"HH_cat_mm_DNN10_GGFnode_2018", # 10

    "HH_cat_ee_DNN10_Hnode_2018", # 5
    "HH_cat_em_DNN10_Hnode_2018", # 5
    "HH_cat_mm_DNN10_Hnode_2018", # 5
    ########
    #"HH_cat_ee_resolved_DNN10_GGFnode_2018",
    #"HH_cat_em_resolved_DNN10_GGFnode_2018",
    #"HH_cat_mm_resolved_DNN10_GGFnode_2018",
    #"HH_cat_ee_resolved_DNN10_VBFnode_2018",
    #"HH_cat_em_resolved_DNN10_VBFnode_2018",
    #"HH_cat_mm_resolved_DNN10_VBFnode_2018",
    #"HH_cat_ee_resolved_DNN10_Hnode_2018",
    #"HH_cat_em_resolved_DNN10_Hnode_2018",
    #"HH_cat_mm_resolved_DNN10_Hnode_2018",
    ########
    #"HH_cat_DNN10_DY_VVVnode_2018", # 10
    #"HH_cat_DNN10_TT_ST_TTVX_Rarenode_2018", # 10

    #"HH_cat_boosted1b_DNN10_Hnode_2018", # 5
    #"HH_cat_resolved1b_DNN10_Hnode_2018", # 5
    #"HH_cat_resolved2b_DNN10_Hnode_2018", # 5

    #"HH_cat_boosted1b_DNN10_GGFnode_2018", # 2
    #"HH_cat_resolved1b_DNN10_GGFnode_2018", # 20
    #"HH_cat_resolved2b_DNN10_GGFnode_2018", # 10

    #"HH_cat_boosted1b_DNN10_VBFnode_2018", # 2 - customized
    #"HH_cat_resolved1b_DNN10_VBFnode_2018", # 7
    #"HH_cat_resolved2b_DNN10_VBFnode_2018", # 4
    ###
    #"HH_cat_boosted1b_DNN10_DY_VVVnode_2018", # 10
    #"HH_cat_resolved1b_DNN10_DY_VVVnode_2018", # 10
    #"HH_cat_resolved2b_DNN10_DY_VVVnode_2018", # 10

    #"HH_cat_boosted1b_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    #"HH_cat_resolved1b_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    #"HH_cat_resolved2b_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    #####
    #"HH_cat_DNN09_GGFnode_2016", # 45
    #"HH_cat_DNN09_VBFnode_2016", # 15
    #"HH_cat_DNN09_Hnode_2016", # 15
    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    ## prepareDatacards_2lss_1tau_sumOS_output_NN_2lss_1tau_ttH_tH_3cat_v5_ttH_1tau",

    channelsTypes = [ "0l_2tau" ]
    ch_nickname = "hh_bb2l_hh_bb2l_OS"
    label = "bbWW_DL"

    targetBinning=[]
    nbinRegular = np.arange(20, 61)
    nbinQuant = np.arange(5, 6) #5

    maxlim = 2.0

    output = {
    "withFolder"      : withFolder,
    "label"           : label,
    "local"           : mom + "/cards",
    "mom"             : mom,
    "bdtTypes"        : bdtTypes,
    "channelsTypes"   : channelsTypes,
    "targetBinning"   : targetBinning,
    "nbinRegular"     : nbinRegular,
    "nbinQuant"       : nbinQuant,
    "maxlim"          : maxlim,
    "ch_nickname"     : ch_nickname,
    "maxlim"          : 26.5,
    "minlim"          : 0.0,
    "makePlotsBin"    : []
    }

    return output
