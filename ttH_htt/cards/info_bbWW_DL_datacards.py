def read_from():
    withFolder = True
    mom = "/afs/cern.ch/work/a/acarvalh/HH_inference/bbWW_binninng/dataset_fit_TTHIDLoose_DNN10_2018/all_hbb_flavour_merged_type4/"

    bdtTypes = [
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

    #"HH_cat_ee_DNN10_Hnode_2018", # 5
    #"HH_cat_em_DNN10_Hnode_2018", # 5
    #"HH_cat_mm_DNN10_Hnode_2018", # 5
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
    "HH_cat_DNN10_TT_ST_TTVX_Rarenode_2018", # 10

    #"HH_cat_boosted1b_DNN10_Hnode_2018", # 5
    #"HH_cat_resolved1b_DNN10_Hnode_2018", # 5
    #"HH_cat_resolved2b_DNN10_Hnode_2018", # 5

    #"HH_cat_boosted1b_DNN10_GGFnode_2018", # 2
    #"HH_cat_resolved1b_DNN10_GGFnode_2018", # 20
    #"HH_cat_resolved2b_DNN10_GGFnode_2018", # 10

    #"HH_cat_boosted1b_DNN10_VBFnode_2018", # 2
    #"HH_cat_resolved1b_DNN10_VBFnode_2018", # 7
    #"HH_cat_resolved2b_DNN10_VBFnode_2018", # 4
    ###
    #"HH_cat_boosted1b_DNN10_DY_VVVnode_2018", # 10
    #"HH_cat_resolved1b_DNN10_DY_VVVnode_2018", # 10
    #"HH_cat_resolved2b_DNN10_DY_VVVnode_2018", # 10

    #"HH_cat_boosted1b_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    #"HH_cat_resolved1b_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    #"HH_cat_resolved2b_DNN10_TT_ST_TTVX_Rarenode_2018", # 10
    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    ## prepareDatacards_2lss_1tau_sumOS_output_NN_2lss_1tau_ttH_tH_3cat_v5_ttH_1tau",

    channelsTypes = [ "0l_2tau" ]
    ch_nickname = "hh_bb2l_hh_bb2l_OS"
    label = "bbWW_DL"

    targetBinning=[]
    nbinRegular = np.arange(20, 61)
    nbinQuant = np.arange(10, 11)

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
    "makePlotsBin"    : [10]
    }

    return output
