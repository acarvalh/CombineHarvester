#!/bin/bash
python rebin_quantiles.py --inputPath=rawRootFiles_v0/4l/2016/
python rebin_quantiles.py --inputPath=rawRootFiles_v0/4l/2017/
python rebin_quantiles.py --inputPath=rawRootFiles_v0/4l/2018/
python rename_procs.py --inputPath=rawRootFiles_v0/4l/2016/rebinned_quantile/
python rename_procs.py --inputPath=rawRootFiles_v0/4l/2017/rebinned_quantile/
python rename_procs.py --inputPath=rawRootFiles_v0/4l/2018/rebinned_quantile/
python writeResCards.py --channel=4l --era=2016 --spinCase=spin0 --inputPath=rawRootFiles_v0/4l/2016/rebinned_quantile/newProcName/ --outPath=dataCards_spin0_v0/4l/2016
python writeResCards.py --channel=4l --era=2017 --spinCase=spin0 --inputPath=rawRootFiles_v0/4l/2017/rebinned_quantile/newProcName/ --outPath=dataCards_spin0_v0/4l/2017
python writeResCards.py --channel=4l --era=2018 --spinCase=spin0 --inputPath=rawRootFiles_v0/4l/2018/rebinned_quantile/newProcName/ --outPath=dataCards_spin0_v0/4l/2018
python writeResCards.py --channel=4l --era=2016 --spinCase=spin2 --inputPath=rawRootFiles_v0/4l/2016/rebinned_quantile/newProcName/ --outPath=dataCards_spin2_v0/4l/2016
python writeResCards.py --channel=4l --era=2017 --spinCase=spin2 --inputPath=rawRootFiles_v0/4l/2017/rebinned_quantile/newProcName/ --outPath=dataCards_spin2_v0/4l/2017
python writeResCards.py --channel=4l --era=2018 --spinCase=spin2 --inputPath=rawRootFiles_v0/4l/2018/rebinned_quantile/newProcName/ --outPath=dataCards_spin2_v0/4l/2018
python writenonresCards.py --sigtype nonresLO --era 2016 --channel 4l --outPath dataCards_nonRes_LO_v0/4l/2016 --inputPath rawRootFiles_v0/4l/2016/rebinned_quantile/newProcName/
python writenonresCards.py --sigtype nonresLO --era 2017 --channel 4l --outPath dataCards_nonRes_LO_v0/4l/2017 --inputPath rawRootFiles_v0/4l/2017/rebinned_quantile/newProcName/
python writenonresCards.py --sigtype nonresLO --era 2018 --channel 4l --outPath dataCards_nonRes_LO_v0/4l/2018 --inputPath rawRootFiles_v0/4l/2018/rebinned_quantile/newProcName/
python writenonresCards.py --sigtype nonresNLO --era 2016 --channel 4l --outPath dataCards_nonRes_NLO_v0/4l/2016 --inputPath rawRootFiles_v0/4l/2016/rebinned_quantile/newProcName/
python writenonresCards.py --sigtype nonresNLO --era 2017 --channel 4l --outPath dataCards_nonRes_NLO_v0/4l/2017 --inputPath rawRootFiles_v0/4l/2017/rebinned_quantile/newProcName/
python writenonresCards.py --sigtype nonresNLO --era 2018 --channel 4l --outPath dataCards_nonRes_NLO_v0/4l/2018 --inputPath rawRootFiles_v0/4l/2018/rebinned_quantile/newProcName/
python combineYear.py --inputPath dataCards_spin0_v0/4l/ --channel 4l
python combineYear.py --inputPath dataCards_spin2_v0/4l/ --channel 4l
python combineYear.py --inputPath dataCards_nonRes_LO_v0/4l/ --channel 4l
python calcResLimits.py --inputPath=dataCards_spin0_v0/4l/2016 --outPath combineResults_spin0_v0/4l/2016 --era 2016 --spinCase spin0 --channel 4l
python calcResLimits.py --inputPath=dataCards_spin0_v0/4l/2017 --outPath combineResults_spin0_v0/4l/2017 --era 2017 --spinCase spin0 --channel 4l
python calcResLimits.py --inputPath=dataCards_spin0_v0/4l/2018 --outPath combineResults_spin0_v0/4l/2018 --era 2018 --spinCase spin0 --channel 4l
python calcResLimits.py --inputPath=dataCards_spin0_v0/4l/RUN2 --outPath combineResults_spin0_v0/4l/RUN2 --era RUN2 --spinCase spin0 --channel 4l
python calcResLimits.py --inputPath=dataCards_spin2_v0/4l/2016 --outPath combineResults_spin2_v0/4l/2016 --era 2016 --spinCase spin2 --channel 4l
python calcResLimits.py --inputPath=dataCards_spin2_v0/4l/2017 --outPath combineResults_spin2_v0/4l/2017 --era 2017 --spinCase spin2 --channel 4l
python calcResLimits.py --inputPath=dataCards_spin2_v0/4l/2018 --outPath combineResults_spin2_v0/4l/2018 --era 2018 --spinCase spin2 --channel 4l
python calcResLimits.py --inputPath=dataCards_spin2_v0/4l/RUN2 --outPath combineResults_spin2_v0/4l/RUN2 --era RUN2 --spinCase spin2 --channel 4l
python calcnoResLimits.py --inputPath dataCards_nonRes_LO_v0/4l/2016/ --channel 4l --era 2016 --outPath combineResults_nonRes_LO_v0/4l/2016
python calcnoResLimits.py --inputPath dataCards_nonRes_LO_v0/4l/2017/ --channel 4l --era 2017 --outPath combineResults_nonRes_LO_v0/4l/2017
python calcnoResLimits.py --inputPath dataCards_nonRes_LO_v0/4l/2018/ --channel 4l --era 2018 --outPath combineResults_nonRes_LO_v0/4l/2018
python calcnoResLimits.py --inputPath dataCards_nonRes_LO_v0/4l/RUN2/ --channel 4l --era RUN2 --outPath combineResults_nonRes_LO_v0/4l/RUN2
python plotResLimit.py --inputPath combineResults_spin0_v0/4l/2016/ --outPath plots_spin0_v0/4l/2016/massScan_spin0_4l_2016.pdf --spinCase spin0 --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @13 TeV" --log --min 0.1
python plotResLimit.py --inputPath combineResults_spin0_v0/4l/2017/ --outPath plots_spin0_v0/4l/2017/massScan_spin0_4l_2017.pdf --spinCase spin0 --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @13 TeV" --log --min 0.1
python plotResLimit.py --inputPath combineResults_spin0_v0/4l/2018/ --outPath plots_spin0_v0/4l/2018/massScan_spin0_4l_2018.pdf --spinCase spin0 --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @13 TeV" --log --min 0.1
python plotResLimit.py --inputPath combineResults_spin0_v0/4l/RUN2/ --outPath plots_spin0_v0/4l/RUN2/massScan_spin0_4l_RUN2.pdf --spinCase spin0 --ylabel "hh-multilepton 4l (137.2 fb^{-1}) @13 TeV" --log --min 0.01
python plotResLimit.py --inputPath combineResults_spin2_v0/4l/2016/ --outPath plots_spin2_v0/4l/2016/massScan_spin2_4l_2016.pdf --spinCase spin2 --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @13 TeV" --log --min 0.1
python plotResLimit.py --inputPath combineResults_spin2_v0/4l/2017/ --outPath plots_spin2_v0/4l/2017/massScan_spin2_4l_2017.pdf --spinCase spin2 --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @13 TeV" --log --min 0.1
python plotResLimit.py --inputPath combineResults_spin2_v0/4l/2018/ --outPath plots_spin2_v0/4l/2018/massScan_spin2_4l_2018.pdf --spinCase spin2 --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @13 TeV" --log --min 0.1
python plotResLimit.py --inputPath combineResults_spin2_v0/4l/RUN2/ --outPath plots_spin2_v0/4l/RUN2/massScan_spin2_4l_RUN2.pdf --spinCase spin2 --ylabel "hh-multilepton 4l (137.2 fb^{-1}) @13 TeV" --log --min 0.01
python plotnonResLimit.py --inputPath combineResults_nonRes_LO_v0/4l/2016/ --outPath plots_nonRes_LO_v0/4l/2016/bmScan_4l_2016.pdf --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @13 TeV" --log --min 0.1
python plotnonResLimit.py --inputPath combineResults_nonRes_LO_v0/4l/2017/ --outPath plots_nonRes_LO_v0/4l/2017/bmScan_4l_2017.pdf --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @13 TeV" --log --min 0.1
python plotnonResLimit.py --inputPath combineResults_nonRes_LO_v0/4l/2018/ --outPath plots_nonRes_LO_v0/4l/2018/bmScan_4l_2018.pdf --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @13 TeV" --log --min 0.1
python plotnonResLimit.py --inputPath combineResults_nonRes_LO_v0/4l/RUN2/ --outPath plots_nonRes_LO_v0/4l/RUN2/bmScan_4l_RUN2.pdf --ylabel "hh-multilepton 4l (137.2 fb^{-1}) @13 TeV" --log --min 0.01
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2016/datacard_4l_2016_spin0_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin0_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_400" --log
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2016/datacard_4l_2016_spin0_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin0_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_400" --skipCombine
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2017/datacard_4l_2017_spin0_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin0_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_400" --log
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2017/datacard_4l_2017_spin0_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin0_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_400" --skipCombine
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2018/datacard_4l_2018_spin0_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin0_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_400" --log
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2018/datacard_4l_2018_spin0_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin0_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_400" --skipCombine
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2016/datacard_4l_2016_spin0_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin0_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_700" --log
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2016/datacard_4l_2016_spin0_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin0_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_700" --skipCombine
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2017/datacard_4l_2017_spin0_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin0_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_700" --log
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2017/datacard_4l_2017_spin0_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin0_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_700" --skipCombine
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2018/datacard_4l_2018_spin0_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin0_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_700" --log
python prefitplot.py --inputCard dataCards_spin0_v0/4l/2018/datacard_4l_2018_spin0_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin0_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin0_700" --skipCombine
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2016/datacard_4l_2016_spin2_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin2_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_400" --log
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2016/datacard_4l_2016_spin2_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin2_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_400" --skipCombine
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2017/datacard_4l_2017_spin2_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin2_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_400" --log
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2017/datacard_4l_2017_spin2_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin2_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_400" --skipCombine
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2018/datacard_4l_2018_spin2_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin2_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_400" --log
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2018/datacard_4l_2018_spin2_400.txt --Bin HH_4l --sigDesc "m#Chi 400 GeV(1 pb)" --outPath plots_spin2_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_400" --skipCombine
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2016/datacard_4l_2016_spin2_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin2_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_700" --log
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2016/datacard_4l_2016_spin2_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin2_v0/4l/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_700" --skipCombine
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2017/datacard_4l_2017_spin2_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin2_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_700" --log
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2017/datacard_4l_2017_spin2_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin2_v0/4l/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_700" --skipCombine
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2018/datacard_4l_2018_spin2_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin2_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_700" --log
python prefitplot.py --inputCard dataCards_spin2_v0/4l/2018/datacard_4l_2018_spin2_700.txt --Bin HH_4l --sigDesc "m#Chi 700 GeV(1 pb)" --outPath plots_spin2_v0/4l/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2016_spin2_700" --skipCombine
python prefitplot.py --inputCard dataCards_nonRes_LO_v0/4l/2016/datacard_4l_2016_SM.txt --Bin HH_4l --sigDesc "SM ggHH LO (1 pb)" --outPath plots_nonRes_LO_v0/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_nonResLO_SM" --log
python prefitplot.py --inputCard dataCards_nonRes_LO_v0/4l/2016/datacard_4l_2016_SM.txt --Bin HH_4l --sigDesc "SM ggHH LO (1 pb)" --outPath plots_nonRes_LO_v0/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_nonResLO_SM" --skipCombine
python prefitplot.py --inputCard dataCards_nonRes_LO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH LO (1 pb)" --outPath plots_nonRes_LO_v0/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResLO_SM" --log
python prefitplot.py --inputCard dataCards_nonRes_LO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH LO (1 pb)" --outPath plots_nonRes_LO_v0/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResLO_SM" --skipCombine
python prefitplot.py --inputCard dataCards_nonRes_LO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH LO (1 pb)" --outPath plots_nonRes_LO_v0/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResLO_SM" --log
python prefitplot.py --inputCard dataCards_nonRes_LO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH LO (1 pb)" --outPath plots_nonRes_LO_v0/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResLO_SM" --skipCombine
python prefitplot.py --inputCard dataCards_nonRes_NLO_v0/4l/2016/datacard_4l_2016_SM.txt --Bin HH_4l --sigDesc "SM ggHH + qqHH" --outPath plots_nonRes_NLO_v0/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_nonResNLO_SM" --log
python prefitplot.py --inputCard dataCards_nonRes_NLO_v0/4l/2016/datacard_4l_2016_SM.txt --Bin HH_4l --sigDesc "SM ggHH + qqHH" --outPath plots_nonRes_NLO_v0/2016/ --ylabel "hh-multilepton 4l (35.9 fb^{-1}) @ 13 TeV" --Info "4l_2016_nonResNLO_SM" --skipCombine
python prefitplot.py --inputCard dataCards_nonRes_NLO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH + qqHH" --outPath plots_nonRes_NLO_v0/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResNLO_SM" --log
python prefitplot.py --inputCard dataCards_nonRes_NLO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH + qqHH" --outPath plots_nonRes_NLO_v0/2017/ --ylabel "hh-multilepton 4l (41.5 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResNLO_SM" --skipCombine
python prefitplot.py --inputCard dataCards_nonRes_NLO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH + qqHH" --outPath plots_nonRes_NLO_v0/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResNLO_SM" --log
python prefitplot.py --inputCard dataCards_nonRes_NLO_v0/4l/2017/datacard_4l_2017_SM.txt --Bin HH_4l --sigDesc "SM ggHH + qqHH" --outPath plots_nonRes_NLO_v0/2018/ --ylabel "hh-multilepton 4l (59.7 fb^{-1}) @ 13 TeV" --Info "4l_2017_nonResNLO_SM" --skipCombine
python goodnessOfFitPlots.py --inputPath dataCards_nonRes_LO_v0/4l/RUN2/datacard_4l_Run2_SM.txt --era RUN2 --channel 4l --analysis nonRes_LO_SM --ntoys 500 --outPath plots_nonRes_LO_v0/4l/RUN2/ --minx 0 --maxx 75 
