def sigmatHq(KT, KV) :
    return (2.63*KT**2 + 3.588*KV**2 - 5.21*KT*KV)
def sigmatHW(KT, KV):
    return (2.91*KT**2 + 2.31*KV**2 - 4.22*KT*KV)


def options_plot (analysis, channel, all_procs, leading_minor_H_local, leading_minor_tH_local, tH_separated) :
    dprocs = OrderedDict()
    Hdecays_long = [ "hww", "hzz", "htt",] #  "hzg", "hmm"
    Hdecays      = ["hww", "htt" , "hzz"]
    hproc_louvain = [
    "ggH_hbb", "ggH_hgg", "ggH_hmm", "ggH_htt", "ggH_hww", "ggH_hzz",
    "qqH_hbb", "qqH_hgg", "qqH_hmm", "qqH_htt", "qqH_hww", "qqH_hzz",
    "ttH_hbb", "ttH_hgg", "ttH_hmm", "ttH_htt", "ttH_hww", "ttH_hzz",
    "WH_hbb",  "WH_hgg",   "WH_hmm", "WH_htt",  "WH_hww",  "WH_hzz",
    "ZH_hbb",   "ZH_hgg", "ZH_hmm", "ZH_htt", "ZH_hww", "ZH_hzz",
    "tHq_hbb", "tHq_hgg", "tHq_hmm", "tHq_htt", "tHq_hww", "tHq_hzz",
    "tHW_hbb", "tHW_hgg", "tHW_hmm", "tHW_htt", "tHW_hww", "tHW_hzz",
    "VH_hbb", "VH_hgg", "VH_hmm", "VH_htt", "VH_hww", "VH_hzz",
    "ttVH"
     ] # "ttH_hww"
    other_H_proc = 0
    ## the order of the entries will be the order of the drawing, that is why this is almost manual
    # TODO: write it on a smarther way
    if 1 > 0 :
        #conversions = "conversions"
        #fakes       = "fakes_data"
        #flips       = "flips_data"
        # if label == "none" it means that this process is to be merged with the anterior key
        if "data_fakes" in all_procs       : dprocs["data_fakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "fakes_mc" in all_procs       : dprocs["fakes_mc"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "flips_mc" in all_procs       : dprocs["flips_mc"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if "data_flips" in all_procs       : dprocs["data_flips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if conversions in all_procs : dprocs[conversions] = {"color" :   5, "fillStype" : 1001, "label" : "Conversions"       , "make border" :  True}
        #if "Fakes" in all_procs       : dprocs["Fakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "Flips" in all_procs       : dprocs["Flips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if "Conv" in all_procs : dprocs["Conv"] = {"color" :   5, "fillStype" : 1001, "label" : "Conversions"       , "make border" :  True}
        if "mcFakes" in all_procs       : dprocs["mcFakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "mcFlips" in all_procs       : dprocs["mcFlips"]       = {"color" :   1, "fillStype" : 3006, "label" : "Flips", "make border" : True}
        if "Convs" in all_procs : dprocs["Convs"] = {"color" :   5, "fillStype" : 1001, "label" : "Conversions"       , "make border" :  True}
        if "SM" in all_procs         : dprocs["SM"]         = {"color" : 226, "fillStype" : 1001, "label" : 'SM'          , "make border" : True}
        if "Rares" in all_procs     : dprocs["Rares"]     = {"color" : 851, "fillStype" : 1001, "label" : "Rares"       , "make border" : True}
        if "Others" in all_procs     : dprocs["Rares"]     = {"color" : 851, "fillStype" : 1001, "label" : "Rares"       , "make border" : True}
        if "EWK" in all_procs       : dprocs["EWK"]       = {"color" : 610, "fillStype" : 1001, "label" : "EWK"         , "make border" : True}
        if "W" in all_procs       : dprocs["W"]       = {"color" : 610, "fillStype" : 1001, "label" : "W"         , "make border" : True}
        if "Wjets" in all_procs       : dprocs["Wjets"]       = {"color" : 5, "fillStype" : 1001, "label" : "W"         , "make border" : True}
        if "ZZ" in all_procs        : dprocs["ZZ"]        = {"color" : 52,  "fillStype" : 1001, "label" : "ZZ"          , "make border" : True}
        if "WZ" in all_procs        : dprocs["WZ"]        = {"color" : 6, "fillStype" : 1001, "label" : "WZ"          , "make border" : True}
        if "TTWW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["TTWW"]                                = {"color" : 823, "fillStype" : 1001, "label" : "t#bar{t}(W)"  , "make border" : True}
        elif "TTW" in all_procs :
            dprocs["TTW"]                                 = {"color" : 823, "fillStype" : 1001, "label" : "t#bar{t}W(W)"        , "make border" : True}
        if "TTZ" in all_procs       : dprocs["TTZ"]       = {"color" : 822, "fillStype" : 1001, "label" : "t#bar{t}Z"         , "make border" : True}
        ### signals
        ### "TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"
        if "HH" in all_procs         : dprocs["HH"]         = {"color" : 4, "fillStype" : 1001, "label" : "none"           , "make border" : False}
        if "VH" in all_procs         : dprocs["VH"]         = {"color" : 4, "fillStype" : 1001, "label" : "VH + TH"           , "make border" : True}
        if "TH" in all_procs         : dprocs["TH"]         = {"color" : 4, "fillStype" : 1001, "label" : 'none'          , "make border" : False}
        for pp in hproc_louvain :
            if pp in all_procs         : dprocs[pp]         = {"color" : 226, "fillStype" : 1001, "label" : "none"           , "make border" : False}
        if "ttH_hww" in all_procs : dprocs["ttH_hww"]         = {"color" : 226, "fillStype" : 1001, "label" : "single H"           , "make border" : True}
        if "WJets" in all_procs     : dprocs["WJets"]           = {"color" : 822, "fillStype" : 1001, "label" :  "Wjets"    , "make border" : True}
        if "Other_bbWW" in all_procs     : dprocs["Other_bbWW"]           = {"color" : 205, "fillStype" : 1001, "label" :  "other"    , "make border" : True}

        if "VV" in all_procs     : dprocs["VV"]           = {"color" : 208, "fillStype" : 1001, "label" :  "none"    , "make border" : False}
        if "VVV" in all_procs : dprocs["VVV"]                                 = {"color" : 208, "fillStype" : 1001, "label" : "VVV + VV"        , "make border" : True}

        if "VV" in all_procs     : dprocs["VV"]           = {"color" : 208, "fillStype" : 1001, "label" :  "none"    , "make border" : False}
        if "vvv" in all_procs : dprocs["vvv"]                                 = {"color" : 208, "fillStype" : 1001, "label" : "VVV+VV"        , "make border" : True}

        if "ttZ" in all_procs : dprocs["ttZ"]                                 = {"color" : 9, "fillStype" : 1001, "label" : "none"        , "make border" : False}
        if "ttW" in all_procs : dprocs["ttW"]                                 = {"color" : 9, "fillStype" : 1001, "label" : "none"        , "make border" : False}
        if "ttVV" in all_procs : dprocs["ttVV"]                                 = {"color" : 9, "fillStype" : 1001, "label" : "ttW + ttZ + ttVV"        , "make border" : True}

        #"vvv", "ttZ", "ttW", "ttVV",
        if "Fakes" in all_procs       : dprocs["Fakes"]       = {"color" :  12, "fillStype" : 3345, "label" : "Fakes"  , "make border" : True}
        if "ST" in all_procs     : dprocs["ST"]           = {"color" : 610, "fillStype" : 1001, "label" :  "ST"    , "make border" : True}
        if "DY" in all_procs     : dprocs["DY"]                                  = {"color" : 221, "fillStype" : 1001, "label" : "DY"         , "make border" : True}
        if "TT" in all_procs     : dprocs["TT"]           = {"color" : 11, "fillStype" : 1001, "label" : 't#bar{t} + jets'   , "make border" : True}


        for hig_proc in ["TTWH", "TTZH", "qqH", "VH", "WH", "ZH", "ggH"] :
            if hig_proc in all_procs   and not leading_minor_H_local == "HH"    :
                for decay in Hdecays :
                    if "%s_%s" % (hig_proc, decay) == leading_minor_H_local : #
                        dprocs[leading_minor_H_local]       = {"color" : 208, "fillStype" : 1001, "label" : "VH + ggH + q#bar{q}H"      , "make border" : False} # "Other H processes" "tHW + VH + ggH + qqH + HH + ttVH"
                    else :
                        dprocs["%s_%s" % (hig_proc, decay)]       = {"color" : 208, "fillStype" : 1001, "label" : "none"         , "make border" : False}
        if not tH_separated :
            if "tHW" in all_procs :
                for decay in list(Hdecays) :
                    if "tHW_%s" % decay == leading_minor_tH_local :
                        dprocs["tHW_%s" % decay ]                             = {"color" : 4, "fillStype" : 1001, "label" : "tH"           , "make border" : True}
                    else :
                        dprocs["tHW_%s" % decay]                     = {"color" : 4, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            if "tHq" in all_procs :
                for decay in list(Hdecays) :
                    if "tHq_%s" % decay == leading_minor_tH_local :
                        dprocs["tHq_%s" % decay]                     = {"color" : 4, "fillStype" : 1001, "label" : "tH"           , "make border" : True}
                    else :
                        dprocs["tHq_%s" % decay]                     = {"color" : 4, "fillStype" : 1001, "label" : "none"        , "make border" : False}
        # change the order of the stack if channel is dominated by fakes
        if "ttH" in all_procs :
            for decay in list(set(list(Hdecays_long)) - set(["htt"])) :
                dprocs["ttH_%s" % decay]                 = {"color" :   2, "fillStype" : 1001, "label" : "none"        , "make border" : False}
            dprocs["ttH_htt"]                                 = {"color" :   2, "fillStype" : 1001, "label" : "t#bar{t}H"         , "make border" : True}
            #dprocs["ttH"]                                 = {"color" :   2, "fillStype" : 1001, "label" : "ttH"         , "make border" : True}
        if "TTH" in all_procs     : dprocs["TTH"]           = {"color" : 2, "fillStype" : 1001, "label" :  "t#bar{t}H"    , "make border" : True}
        ### changing processes orders
        if channel in ["2l_0tau"] and not leading_minor_H_local =="HH" :
            del dprocs[fakes]
            dprocs[fakes]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Fakes"        , "make border" : True}
            #del dprocs["DY"]
            dprocs["DY"]                                  = {"color" : 221, "fillStype" : 1001, "label" : "DY"         , "make border" : True}
            del dprocs["TT"]
            dprocs["TT"]                                  = {"color" : 17, "fillStype" : 1001, "label" : 't#bar{t} + jets'   , "make border" : True}
        if channel in ["1l_0tau"] and not leading_minor_H_local =="HH" :
            del dprocs[conversions]
            dprocs[conversions]                           = {"color" :   5, "fillStype" : 1001, "label" : "Conv."        , "make border" : True}
            del dprocs[fakes]
            dprocs[fakes]                                 = {"color" :   1, "fillStype" : 3005, "label" : "Fakes"        , "make border" : True}
            #del dprocs["DY"]
            dprocs["DY"]                                  = {"color" : 221, "fillStype" : 1001, "label" : "DY"         , "make border" : True}
            del dprocs["W"]
            dprocs["W"]                                   = {"color" : 610, "fillStype" : 1001, "label" : 'W + jets'   , "make border" : True}
            del dprocs["TT"]
            dprocs["TT"]                                  = {"color" : 17, "fillStype" : 1001, "label" : 't#bar{t} + jets'   , "make border" : True}
    return dprocs

def Higgs_proc_decay (proc) :
    Hdecays_long = [  "htt",  "hww", "hzz",  "hzg", "hmm"] #
    Hdecays      = ["hww", "hzz", "htt" ]
    #sum(higgs_procs,[])
    return sum([ [y + "_" + x  for x in decays if not (x in ["hzz", "htt", "hzg", "hmm"] and y != "ttH")] for y in sigs], [])

def options_plot_ranges (analysis) :
    if 1 > 0 :
        ### it will have the subcategories for the DNNs
        info_channel = {
            "2l_0tau" : {
                "minY" : 0.1,    "maxY" :  220000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l ', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300. ,
                "list_cats" : [],
                "list_cats_original" : [],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "1l_0tau" : {
                "minY" : 0.01,    "maxY" :  10000000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 1l ',
                "labelX" : "BDT bin#",
                "position_cats": 300. ,
                "list_cats" : [],
                "list_cats_original" : [],
                "cats" : [""],
                "catsX" :  [0.0]
                },
            "bbWW_DL" : {
                "minY" : 0.001,    "maxY" :  220000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l ', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300. ,
                "list_cats" : [],
                "list_cats_original" : [],
                "cats" : [""],
                "catsX" :  [0.0]
            },
            "bbWW_SL" : {
                "minY" : 0.01,    "maxY" :  2200000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 1l ', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300. ,
                "list_cats" : [],
                "list_cats_original" : [],
                "cats" : [""],
                "catsX" :  [0.0]
            },
            "bbWW_SL_aa" : {
                "minY" : 0.01,    "maxY" :  2200000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 1l ', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300. ,
                "list_cats" : [],
                "list_cats_original" : [],
                "cats" : [""],
                "catsX" :  [0.0]
            },
            "bbWW_DL_aa" : {
                "minY" : 0.01,    "maxY" :  2200000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 1l ', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300. ,
                "list_cats" : [],
                "list_cats_original" : [],
                "cats" : [""],
                "catsX" :  [0.0]
            },
            "bbWW_DL_BKG" : {
                "minY" : 0.001,    "maxY" :  2200000000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l - BKG nodes', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300000. ,
                "list_cats" : ["DY_VVVnode", "TT_ST_TTVX_Rarenode"],
                "list_cats_original" : [],
                "cats" : ["DY VVV", "TT rest"],
                "catsX" :  [2.0, 10.]
            },
            "bbWW_DL_DY_hbb" : {
                "minY" : 0.001,    "maxY" :  2200000000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l - DY + VVV nodes', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300000. ,
                "list_cats" : ["boosted1b_DY_VVVnode", "resolved1b_DY_VVVnode", "resolved2b_DY_VVVnode"],
                "list_cats_original" : [],
                "cats" : ["boosted", "res 1b", "res 2b"],
                "catsX" :  [2.0, 10., 30]
            },
            "bbWW_DL_TT_hbb" : {
                "minY" : 0.001,    "maxY" :  2200000000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l - DY + VVV nodes', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300000. ,
                "list_cats" : ["boosted1b_TT_ST_TTVX_Rarenode", "resolved1b_TT_ST_TTVX_Rarenode", "resolved2b_TT_ST_TTVX_Rarenode"],
                "list_cats_original" : [],
                "cats" : ["boosted", "res 1b", "res 2b"],
                "catsX" :  [2.0, 10., 30]
            },
            "bbWW_DL_Hnode" : {
                "minY" : 0.001,    "maxY" :  2200000000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l - single H node', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300000. ,
                "list_cats" : ["boosted1b_Hnode", "resolved2b_Hnode", "resolved1b_Hnode"],
                "list_cats_original" : [],
                "cats" : ["boosted1b", "resolved2b", "resolved1b"],
                "catsX" :  [2.0, 40., 60 ]
            },
            "bbWW_DL_GGFnode" : {
                "minY" : 0.001,    "maxY" :  2200000000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l - GGF HH node', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300000. ,
                "list_cats" : ["boosted1b_GGFnode", "resolved2b_GGFnode", "resolved1b_GGFnode"],
                "list_cats_original" : [],
                "cats" : ["boosted1b", "resolved2b", "resolved1b"],
                "catsX" :  [2.0, 40., 60 ]
            },
            "bbWW_DL_VBFnode" : {
                "minY" : 0.001,    "maxY" :  2200000000000.,
                "minYerr": -1.02, "maxYerr" : 1.02,
                "useLogPlot" : True,
                "label" : 'HH bbWW 2l - VBF HH node', # (HH SM normalized to 1pb)
                "labelX" : "BDT bin#",
                "position_cats": 300000. ,
                "list_cats" : ["boosted1b_VBFnode", "resolved2b_VBFnode", "resolved1b_VBFnode"],
                "list_cats_original" : [],
                "cats" : ["boosted1b", "resolved2b", "resolved1b"],
                "catsX" :  [2.0, 40., 60 ]
            },
        }
        """
        "boosted1b_GGFnode", "resolved1b_GGFnode", "resolved2b_GGFnode"
        "boosted1b_Hnode", "resolved1b_Hnode", "resolved2b_Hnode"
        "boosted1b_VBFnode", "resolved1b_VBFnode", "resolved2b_VBFnode"

        "boosted1b_DY_VVVnode", "resolved1b_DY_VVVnode", "resolved2b_DY_VVVnode"
        "boosted1b_TT_ST_TTVX_Rarenode", "resolved1b_TT_ST_TTVX_Rarenode", "resolved2b_TT_ST_TTVX_Rarenode"

        """
    return info_channel

def list_channels_draw(analysis) :
    hproc_louvain = ["ggH_hbb", "ggH_hgg", "ggH_hmm", "ggH_htt", "ggH_hww", "ggH_hzz", "qqH_hbb", "qqH_hgg", "qqH_hmm", "qqH_htt", "qqH_hww", "qqH_hzz", "ttH_hbb", "WH_hbb", "ZH_hbb", "ZH_htt", "ZH_hww", "tHq_hww", "tHW_hww", "VH_hww", "ttH_hww"] #

    info_channel = {
    "2l_0tau"   : {
        "bkg_proc_from_data" : [fakes       ],
        "bkg_procs_from_MC"  : [ "TT", "Convs", "TTH", "TH", "TTZ", "TTW", "TTWW", "TT", "Other", "VH", "DY", "W", "WW", "WZ", "ZZ"], #
        "signal" : [], # "signal_ggf_nonresonant_hh_bbttSM", "signal_ggf_nonresonant_hh_bbvv_slSM", "signal_ggf_nonresonant_hh_bbvvSM"
        "signal_HH" : ["signal_ggf_nonresonant_hh_bbttSM", "signal_ggf_nonresonant_hh_bbvv_slSM", "signal_ggf_nonresonant_hh_bbvvSM"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "1l_0tau"   : {
        "bkg_proc_from_data" : [fakes       ],
        "bkg_procs_from_MC"  : [ "TT", "Convs", "TTH", "TH", "TTZ", "TTW", "TTWW", "TT", "Other", "VH", "DY", "W", "WW", "WZ", "ZZ"],
        "signal_HH" : ["signal_ggf_nonresonant_hh_bbttkl_1p00", "signal_ggf_nonresonant_hh_bbvv_slkl_1p00", "signal_ggf_nonresonant_hh_bbvvkl_1p00"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL"   : {
        "bkg_proc_from_data" : ["Fakes"       ],
        "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_0_kt_1_2B2VTo2L2Nu"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_SL"   : {
        "bkg_proc_from_data" : ["Fakes"       ],
        "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_1_kt_1_hbbhww1l"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_SL_aa"   : {
        "bkg_proc_from_data" : ["Fakes"       ],
        "bkg_procs_from_MC"  : ["WJets", "DY", "ST", "TT", "VV", "vvv", "ttZ", "ttW", "ttVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_1_kt_1_hbbhwwsl"], #
        "leading_minor_H" : "ttH_hbb", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL_aa"   : {
        "bkg_proc_from_data" : ["Fakes"       ],
        "bkg_procs_from_MC"  : ["WJets", "DY", "ST", "TT", "VV", "vvv", "ttZ", "ttW", "ttVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_1_kt_1_hbbhwwsl"], #
        "leading_minor_H" : "ttH_hbb", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL_BKG"   : {
        "bkg_proc_from_data" : ["Fake"       ],
        "bkg_procs_from_MC"  : ["DY", "Rares", "SM", "ST", "VVV", "Wjets", "TTVX", "TT"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_0_kt_1_2B2VTo2L2Nu"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL_Hnode"   : {
        "bkg_proc_from_data" : ["Fake"       ],
        "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_0_kt_1_2B2VTo2L2Nu"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL_GGFnode"   : {
        "bkg_proc_from_data" : ["Fake"       ],
        "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_0_kt_1_2B2VTo2L2Nu"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL_VBFnode"   : {
        "bkg_proc_from_data" : ["Fake"       ],
        "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_0_kt_1_2B2VTo2L2Nu"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL_TT_hbb"   : {
        "bkg_proc_from_data" : ["Fake"       ],
        "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_0_kt_1_2B2VTo2L2Nu"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },
    "bbWW_DL_DY_hbb"   : {
        "bkg_proc_from_data" : ["Fake"       ],
        "bkg_procs_from_MC"  : ["TT", "ST", "DY", "WJets", "VV", "VVV", "Other_bbWW"] + hproc_louvain,
        "signal_HH" : ["ggHH_kl_0_kt_1_2B2VTo2L2Nu"], #
        "leading_minor_H" : "TH", ## The legend for the mino H proc will only appear if this process is in the card
        "leading_minor_tH" : "tHq_htt" ## The legend for the mino H proc will only appear if this process is in the card
        },



    }
    return info_channel
