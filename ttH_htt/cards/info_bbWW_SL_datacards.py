def read_from():
    withFolder = True
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_SL_2018/plainbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_SL_2018/JPAbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/DNN_SL_v1/dataset_fit_TTHIDLoose_SL_BSM_2018/plainbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/DNN_SL_v1/dataset_fit_TTHIDLoose_SL_BSM_2018/JPAbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/DNN_SL_v1/dataset_fit_TTHIDLoose_SL_SM_2018/plainbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/DNN_SL_v1/dataset_fit_TTHIDLoose_SL_SM_2018/JPAbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_SL_BSM_cutBased_2018/plainbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_SL_BSM_cutBased_2018/JPAbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_SL_BSM_DNNBased_2018/plainbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/dataset_fit_TTHIDLoose_SL_BSM_DNNBased_2018/JPAbtag_merge/"

    mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/SL_DNNv2/dataset_fit_TTHIDLoose_SL_BSM_resolved_2018/JPAbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/SL_DNNv2/dataset_fit_TTHIDLoose_SL_SM_resolved_2018/JPAbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/SL_DNNv2/dataset_fit_TTHIDLoose_SL_BSM_resolved_2018/plainbtag_merge/"
    #mom = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/SL_DNNv2/dataset_fit_TTHIDLoose_SL_SM_resolved_2018/plainbtag_merge/"

    #"/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/datacards_louvain_Jan2020/SL_DNNv2/dataset_fit_TTHIDLoose_SL_BSM_resolved_2018/"



    bdtTypes = [
    #"HH_cat_Ewknode_2018",
    #"HH_cat_Topnode_2018",
    #"HH_cat_WJetsnode_2018",
    #"HH_cat_boostedHbb_GGFnode_2018",
    #"HH_cat_boostedHbb_Hnode_2018",
    #"HH_cat_boostedHbb_VBFnode_2018",
    ####
    #"HH_cat_resolved_1b_GGFnode_2018",
    #"HH_cat_resolved_1b_Hnode_2018",
    #"HH_cat_resolved_1b_VBFnode_2018",
    #"HH_cat_resolved_2b_GGFnode_2018",
    #"HH_cat_resolved_2b_Hnode_2018",
    #"HH_cat_resolved_2b_VBFnode_2018",
    ############
    "HH_cat_resolved_JPA1b_GGFnode_2018",
    "HH_cat_resolved_JPA1b_Hnode_2018",
    "HH_cat_resolved_JPA1b_VBFnode_2018",
    "HH_cat_resolved_JPA2b_GGFnode_2018",
    "HH_cat_resolved_JPA2b_Hnode_2018",
    "HH_cat_resolved_JPA2b_VBFnode_2018",
    ############
    #"HH_cat_boostedHbb_WJetsnode_2018",
    #"HH_cat_boostedHbb_Ewknode_2018",
    #"HH_cat_boostedHbb_Topnode_2018",
    #"HH_cat_resolvedHbb_WJetsnode_2018",
    #"HH_cat_resolvedHbb_Ewknode_2018",
    #"HH_cat_resolvedHbb_Topnode_2018",

    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    ## prepareDatacards_2lss_1tau_sumOS_output_NN_2lss_1tau_ttH_tH_3cat_v5_ttH_1tau",

    channelsTypes = [ "0l_1tau" ]
    ch_nickname = "hh_bb1l_hh_bb2l_OS"
    label = "bbWW_SL"

    targetBinning=[] # if you want to put the numbers of bin boundaries by hand put them here
    nbinRegular = np.arange(20, 61)
    nbinQuant = np.arange(10, 11) #5, 20

    maxlim = 2.0

    output = {
    "withFolder"      : withFolder,
    "label"           : label,
    "local"           : mom + "/cards",
    "mom"             : mom,
    "bdtTypes"        : bdtTypes,
    "channelsTypes"   : channelsTypes,
    "targetBinning" : targetBinning,
    "nbinRegular"     : nbinRegular,
    "nbinQuant"       : nbinQuant,
    "maxlim"          : maxlim,
    "ch_nickname"     : ch_nickname,
    "maxlim"          : 380.5,
    "minlim"          : 50.0,
    "makePlotsBin"    : [1]
    }

    return output
