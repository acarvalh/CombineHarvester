def list_channels(analysis) :
    if analysis == "ttH" :
        sigs = ["ttH", "tHq", "tHW", "WH", "ZH"]
        decays = ["_hww", "_hzz", "_htt", "_hzg", "_hmm" ]
        higgs_procs = [ [y + x  for x in decays if not (x in ["hzg", "hmm"] and y != "ttH")] for y in sigs]
        conversions = "Convs"
        fakes       = "fakes_mc"
        flips       = "flips_mc"
        #higgs_procs += [["TTWH", "TTZH", "HH"]]
        #higgs_procs = [ [y + "_" + x  for x in decays if not (x in ["hzz", "htt", "hzg", "hmm"] and y != "ttH")] for y in sigs]
        ## add the H processes (that shall be marked as signal on the datacards)

        info_channel = {
        "2lss_0tau" : {
            "bkg_proc_from_data" : [ fakes  , flips  ],
            "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "Rares", conversions, "WZ", "ZZ", "TT", "ggH", "qqH", "TTWH", "TTZH",  "HH",], # "TTWH", "TTZH",
            "isSMCSplit" : False
        },
        "ttWctrl"   : { "bkg_proc_from_data" : [             ], "bkg_procs_from_MC"  : ["TTWH", "TTZH", "HH"], "isSMCSplit" : False},
        "2lss_1tau" : {
            "bkg_proc_from_data" : [ fakes , flips ], #
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "Rares", "WZ", "ZZ", conversions, "TT", "TTWH", "TTZH", "HH",], # "TTWH", "TTZH", "HH",
            "isSMCSplit" : False
            },
        "3l_0tau"   : {
            "bkg_proc_from_data" : [ fakes  ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "Rares", "WZ", "ZZ", "EWK", conversions, "TT", "TTWH", "TTZH", "HH",], # "TTWH", "TTZH", "HH",
            "isSMCSplit" : False
        },
        "1l_2tau"   : {
            "bkg_proc_from_data" : [ "fakes_mc"       ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "EWK", "Rares", "WZ", "ZZ", "TT", "TTWH", "TTZH", "HH",], #
            "isSMCSplit" : False
            },
        "ttZctrl"   : { "bkg_proc_from_data" : [             ], "bkg_procs_from_MC"  : ["TTWH", "TTZH", "HH"], "isSMCSplit" : False},
        "2l_2tau"   : {
            "bkg_proc_from_data" : [ fakes       ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "EWK", "Rares", "WZ", "ZZ", "TT", "TTWH", "TTZH", "HH",], #
            "isSMCSplit" : False
            },
        "3l_1tau"   : {
            "bkg_proc_from_data" : [ fakes, flips   ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "Rares", "WZ", "ZZ", conversions, "TT", "HH",], # "TTWH", "TTZH", "HH",
            "isSMCSplit" : False
            },
        "2los_1tau" : {
            "bkg_proc_from_data" : [ fakes, flips   ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "Rares", "WZ", "ZZ", conversions, "TT"], # "TTWH", "TTZH", "HH",
            "isSMCSplit" : False
        },
        "0l_2tau"   : {
            "bkg_proc_from_data" : [ fakes      ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "EWK", "Rares", "WZ", "ZZ", "DY", "TT", "HH",], #  "TTWH", "TTZH",
            "isSMCSplit" : False
            },
        "1l_1tau"   : {
            "bkg_proc_from_data" : [ fakes      ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "EWK", "Rares", "WZ", "ZZ", "DY", "TT", "HH",], # "TTWH", "TTZH", "HH",
            "isSMCSplit" : False
            },
        "WZctrl"    : { "bkg_proc_from_data" : [             ], "bkg_procs_from_MC"  : ["TTWH", "TTZH", "HH"],                "isSMCSplit" : False},
        "4l_0tau"   : {
            "bkg_proc_from_data" : [ fakes, flips   ],
            "bkg_procs_from_MC"  : [ "TTW", "TTWW", "TTZ", "Rares", "WZ", "ZZ", conversions, "TT"], # "TTWH", "TTZH", "HH",
            "isSMCSplit" : False
        },
        "ZZctrl"    : { "bkg_proc_from_data" : [             ], "bkg_procs_from_MC"  : ["TTWH", "TTZH", "HH"],                               "isSMCSplit" : False},
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return {
        "higgs_procs"      : higgs_procs,
        "decays"           : decays,
        "info_bkg_channel" : info_channel
    }
