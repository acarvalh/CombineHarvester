def list_channels( fake_mc, signal_type="none", mass="none", HHtype="none", renamedHHInput=False ) :
    #####################
    # signal_type = "noresLO" | "nonresNLO" | "res"
    # mass nonres = "cHHH1" | cHHH... || "SM", "BM12", "kl_1p00"... || "spin0_900",....
    # HHtype = "bbWW" | "multilep"
    #####################
    #sigs = ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH" ]
    #decays = ["_hww", "_hzz", "_htt", "_hzg", "_hmm" ]
    sigs = []
    hproc_louvain = [
        "ggH_hbb", "ggH_hgg", "ggH_hmm", "ggH_htt", "ggH_hww", "ggH_hzz",
        "qqH_hbb", "qqH_hgg", "qqH_hmm", "qqH_htt", "qqH_hww", "qqH_hzz",
        "ttH_hbb", "ttH_hgg", "ttH_hmm", "ttH_htt", "ttH_hww", "ttH_hzz",
        "WH_hbb",  "WH_hgg",   "WH_hmm", "WH_htt",  "WH_hww",  "WH_hzz",
        "ZH_hbb",   "ZH_hgg", "ZH_hmm", "ZH_htt", "ZH_hww", "ZH_hzz",
        "tHq_hbb", "tHq_hgg", "tHq_hmm", "tHq_htt", "tHq_hww", "tHq_hzz",
        "tHW_hbb", "tHW_hgg", "tHW_hmm", "tHW_htt", "tHW_hww", "tHW_hzz",
        "VH_hbb", "VH_hgg", "VH_hmm", "VH_htt", "VH_hww", "VH_hzz",
        ]
    # FIXME ---> to be used when the cards are done with Higs processes in Physics model
    # naming convention and separating by branching ratio
    # by now it will look for them (eg ttH_hww) in the prepareDatacards and not find
    decays_hh = []
    if HHtype == "bbWW" :
        decays_hh = ["bbvv_sl", "bbtt", "bbvv"]
    else :
        print("HHtype (%s) not implemented" % ( HHtype))
        sys.exit()

    #---> by now not used, we may use to implement systematics/BR -- see how decays_hh is used in WriteDatacards
    #higgs_procs = [ [y + x  for x in decays if not (x in ["hzg", "hmm"] and y != "ttH")] for y in sigs]
    #higgs_procs = [hproc_louvain]
    higgs_procs = [[]]

    prefix_VBF = "signal_ggf_nonresonant"
    SM_VBF     = "1_1_1"
    prefix_GF  = "signal_ggf_nonresonant"
    couplings_GF_NLO = [ "cHHH0", "cHHH1", "cHHH5" ]
    # --> using "cHHH2p45" as control -- check closure to see if this is the best case
    couplings_VBF    = [ "1_1_1", "1_1_2", "1_2_1", "1_1_0", "1p5_1_1", "0p5_1_1" ]
    if renamedHHInput :
        prefix_VBF = "qqHH"
        SM_VBF     = "CV_1_C2V_1_kl_1"
        prefix_GF  = "ggHH"
        couplings_GF_NLO = [ "kl_0_kt_1", "kl_1_kt_1", "kl_5_kt_1" ]
        # --> using "cHHH2p45" as control -- check closure to see if this is the best case
        couplings_VBF    = [ "CV_1_C2V_1_kl_1", "CV_1_C2V_1_kl_2", "CV_1_C2V_2_kl_1",  "CV_1_C2V_1_kl_0", "CV_1p5_C2V_1_kl_1", "CV_0p5_C2V_1_kl_1" ]

    if signal_type == "nonresLO" :
        listSig = []
        for decay_hh in decays_hh :
            listSig = listSig + [
            "%s_hh_%s%s"  % (prefix_GF, decay_hh, mass),
            "%s_%s_hh_%s" % (prefix_VBF, SM_VBF, decay_hh)
            ]
        sigs = [ listSig ]
    elif signal_type == "nonresNLO" :
        listSig = []
        listSig = listSig + ["qqHH_CV_0p5_C2V_1_kl_1_hbbhtt", "qqHH_CV_1p5_C2V_1_kl_1_hbbhtt", "qqHH_CV_1_C2V_1_kl_0_hbbhtt", "qqHH_CV_1_C2V_1_kl_1_hbbhtt", "qqHH_CV_1_C2V_1_kl_2_hbbhtt", "qqHH_CV_1_C2V_2_kl_1_hbbhtt", "qqHH_CV_1_C2V_0_kl_1_hbbhtt",]
        listSig = listSig + ["qqHH_CV_0p5_C2V_1_kl_1_hbbhww2l", "qqHH_CV_1p5_C2V_1_kl_1_hbbhww2l", "qqHH_CV_1_C2V_1_kl_0_hbbhww2l", "qqHH_CV_1_C2V_1_kl_1_hbbhww2l", "qqHH_CV_1_C2V_1_kl_2_hbbhww2l", "qqHH_CV_1_C2V_2_kl_1_hbbhww2l", "qqHH_CV_1_C2V_0_kl_1_hbbhww2l",]
        listSig = listSig + ["qqHH_CV_0p5_C2V_1_kl_1_hbbhww1l", "qqHH_CV_1p5_C2V_1_kl_1_hbbhww1l", "qqHH_CV_1_C2V_1_kl_0_hbbhww1l", "qqHH_CV_1_C2V_1_kl_1_hbbhww1l", "qqHH_CV_1_C2V_1_kl_2_hbbhww1l", "qqHH_CV_1_C2V_2_kl_1_hbbhww1l", "qqHH_CV_1_C2V_0_kl_1_hbbhww1l" ]
        listSig = listSig + ["ggHH_kl_2p45_kt_1_hbbhtt",  "ggHH_kl_1_kt_1_hbbhtt", "ggHH_kl_5_kt_1_hbbhtt", "ggHH_kl_0_kt_1_hbbhtt",]
        listSig = listSig + ["ggHH_kl_2p45_kt_1_hbbhww2l", "ggHH_kl_1_kt_1_hbbhww2l", "ggHH_kl_5_kt_1_hbbhww2l", "ggHH_kl_0_kt_1_hbbhww2l",]
        listSig = listSig + ["ggHH_kl_2p45_kt_1_hbbhww1l", "ggHH_kl_1_kt_1_hbbhww1l", "ggHH_kl_5_kt_1_hbbhww1l", ]
        # "ggHH_kl_0_kt_1_hbbhww2l",
        #listSig = listSig + [ "ggHH_kl_1_kt_1_hbbhtt", "ggHH_kl_1_kt_1_hbbhww1l" ]


        sigs = [ listSig ]
    elif signal_type == "res" :
        listSig = []
        for decay_hh in decays_hh :
            listSig = listSig + [ "signal_ggf_%s_hh_%s" % (mass, decay_hh) ]
        sigs = [ listSig ]
    else :
        print("signal_type %s not implemented" % (signal_type))
        sys.exit()
    # FIXME ---> add VBF to nonres case (SM by default)
    # FIXME ---> add multilep options
    ######################
    #sigs = [["signal_ggf_nonresonant_cHHH1_hh_bbtt", "signal_ggf_nonresonant_cHHH1_hh_bbvv_sl", "signal_ggf_nonresonant_cHHH1_hh_bbvv"]]
    #sigs = [["signal_ggf_nonresonant_hh_bbttSM", "signal_ggf_nonresonant_hh_bbvv_slSM", "signal_ggf_nonresonant_hh_bbvvSM" ]]
    #sigs = [["signal_ggf_nonresonant_hh_bbttBM12", "signal_ggf_nonresonant_hh_bbvv_slBM12", "signal_ggf_nonresonant_hh_bbvvBM12" ]]
    #sigs = [["signal_ggf_spin0_900_hh_bbtt", "signal_ggf_spin0_900_hh_bbvv", "signal_ggf_spin0_900_hh_bbvv_sl"]]
    #sigs = [["signal_ggf_spin0_400_hh_bbtt", "signal_ggf_spin0_400_hh_bbvv", "signal_ggf_spin0_400_hh_bbvv_sl"]]
    #sigs = [["signal_ggf_nonresonant_hh_bbttkl_1p00", "signal_ggf_nonresonant_hh_bbvv_slkl_1p00", "signal_ggf_nonresonant_hh_bbvvkl_1p00"]]

    higgs_procs = higgs_procs + [listSig]

    #higgs_procs = [hproc_louvain]
    conversions = "Convs"
    if fake_mc :
        fakes       = "fakes_mc"
        flips       = "flips_mc"
    else :
        fakes       = "data_fakes"
        flips       = "data_flips"

    info_channel = {
        "2l_0tau" : {
            "bkg_proc_from_data" : [ fakes    ],
            "bkg_procs_from_MC"  : ["Convs", "TTH", "TH", "TTZ", "TTW", "TTWW", "TT", "Other", "VH", "DY", "W", "WW", "WZ", "ZZ"],
            "isSMCSplit" : False,
            "proc_to_remove" : {}
        },
        "1l_0tau" : {
            "bkg_proc_from_data" : [ fakes    ],
            "bkg_procs_from_MC"  : ["Convs", "TTH", "TH", "TTZ", "TTW", "TTWW", "TT", "Other", "VH", "DY", "W", "WW", "WZ", "ZZ"],
            "isSMCSplit" : False,
            "proc_to_remove" : {}
        },
        "bbWW_DL" : {
            "bkg_proc_from_data" : [ "Fakes"  ],
            "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain, #
            "isSMCSplit" : False,
            "proc_to_remove" : {}
        },
        "bbWW_SL" : {
            "bkg_proc_from_data" : [ "Fakes"  ],
            "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain , #
            "isSMCSplit" : False,
            "proc_to_remove" : {}
        },
    }
    #---> by now "TTH", "TH" and "VH" are automatically marked as BKG

    return {
        "higgs_procs"      : higgs_procs,
        "decays"           : [],
        "decays_hh"        : decays_hh,
        "info_bkg_channel" : info_channel,
        #"higgs_procs_to_draw"      : sigs[0],
        "higgs_procs_to_draw"      : ["ggHH_kl_1_kt_1_hbbhww1l", "qqHH_CV_1_C2V_1_kl_1_hbbhww1l", "ggHH_kl_1_kt_1_hbbhww2l", "qqHH_CV_1_C2V_1_kl_1_hbbhww2l", "ggHH_kl_1_kt_1_hbbhtt", "qqHH_CV_1_C2V_1_kl_1_hbbhtt" ],
        #"higgs_procs_to_draw"      : [ "qqHH_CV_1_C2V_1_kl_1_hbbhww2l", "qqHH_CV_1_C2V_1_kl_1_hbbhtt", "qqHH_CV_1_C2V_2_kl_1_hbbhww2l", "qqHH_CV_1_C2V_2_kl_1_hbbhtt" ],
    }
