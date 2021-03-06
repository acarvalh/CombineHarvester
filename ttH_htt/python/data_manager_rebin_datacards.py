import ROOT
from ROOT import *
import array as arr
import math
from math import sqrt, sin, cos, tan, exp
import sys, os, re, shlex
from subprocess import Popen, PIPE
import glob

global testPrint
def testPrint() :
    print ("loaded data_manager_rebin_datacards")

global runCmd
def runCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        proc=subprocess.Popen(["cd %s ; %s" % (outfolder, combinecmd)],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
    except OSError:
        print ("command not known\n", combinecmd)

global runCombineCmd
def runCombineCmd(combinecmd, outfolder='.', saveout=None):
    print ("Command: ", combinecmd)
    try:
        p = Popen(shlex.split(combinecmd) , stdout=PIPE, stderr=PIPE, cwd=outfolder)
        comboutput = p.communicate()[0]
    except OSError:
        print ("command not known\n", combinecmd)
        comboutput = None
    if not saveout == None :
        if saveout.startswith("/") : saveTo = saveout
        else : saveTo = outfolder + "/" + saveout
        with open(saveTo, "w") as text_file:
            text_file.write(unicode(comboutput))
        print ("Saved result to: " + saveTo)
    print ("\n")
    return comboutput

global finMaxMin
def finMaxMin(histSource) :
    file = TFile(histSource+".root","READ")
    file.cd()
    hSum = TH1F()
    for keyO in file.GetListOfKeys() :
       obj =  keyO.ReadObj()
       if type(obj) is not TH1F : continue
       hSumDumb = obj.Clone()
       if not hSum.Integral()>0 : hSum=hSumDumb
       else : hSum.Add(hSumDumb)
    return [
    [hSum.GetBinLowEdge(1),  hSum.GetBinCenter(hSum.GetNbinsX())+hSum.GetBinWidth(hSum.GetNbinsX())/2.],
    [hSum.GetBinLowEdge(hSum.FindFirstBinAbove(0.0)),  hSum.GetBinCenter(hSum.FindLastBinAbove (0.0))+hSum.GetBinWidth(hSum.FindLastBinAbove (0.0))/2.]]
    return 0

global getQuantiles
def getQuantiles(histoP, ntarget, xmax) :
    histoP.Scale(1./histoP.Integral())
    histoP.GetCumulative()
    histoP.GetXaxis().SetRangeUser(0.,1.)
    histoP.GetYaxis().SetRangeUser(0.,1.)
    histoP.SetMinimum(0.0)
    xq    = arr.array('d', [0.] * (ntarget+1))
    yq    = arr.array('d', [0.] * (ntarget+1))
    yqbin = arr.array('d', [0.] * (ntarget+1)) # +2 if firsrt is not zero
    for  ii in range(0,ntarget) :
        xq[ii] = (float(ii)/(ntarget))
    xq[ntarget] = 0.999999999
    histoP.GetQuantiles(ntarget, yq, xq)
    line = [None for point in range(ntarget)]
    line2 = [None for point in range(ntarget)]
    for  ii in range(1,ntarget+1) : yqbin[ii]=yq[ii]
    yqbin[ntarget] = xmax
    return yqbin
global rebinHistogram_binindex
def rebinHistogram_binindex(histogram) :
  numBins = histogram.GetNbinsX()
  histogram_rebinned = TH1F()
  histogram_rebinned = TH1F(histogram.GetName(), histogram.GetName(),  numBins, 0.5, numBins + 0.5)
  if not histogram_rebinned.GetSumw2N() : histogram_rebinned.Sumw2()
  histogram_rebinned.Reset()
  for idxBin in range(0, numBins+1) : # CV: include underflow and overflow bins
    binContent = histogram.GetBinContent(idxBin)
    print 'bincont=========== ', binContent, '\t', idxBin
    binError = histogram.GetBinError(idxBin)
    histogram_rebinned.SetBinContent(idxBin, binContent)
    histogram_rebinned.SetBinError(idxBin, binError)
  return histogram_rebinned


global rebinRegular
def rebinRegular(
    histSource,
    nbin,
    BINtype,
    doFlat,
    targetBinning,
    doplots,
    bdtType,
    outdir,
    nameOutFileAddL,
    withFolder=False,
    partialCopy=False
    ) :
    print ("rebinRegular")
    nQuantMax = 36
    minmax = finMaxMin(histSource) # [[0], [1]], [0]=first, last bin above 0; [1]= their corresponding x-value
    errOcontTTLast=[]
    errOcontTTPLast=[]
    errOcontSUMLast=[]
    errOcontSUMPLast=[]
    #
    errTTLast=[]
    contTTLast=[]
    errSUMLast=[]
    contSUMLast=[]
    #
    realbins=[]
    xminbin=[]
    xmaxbin=[]
    xmaxLbin=[]
    #
    lastQuant=[]
    xmaxQuant=[]
    xminQuant=[]
    #
    if BINtype=="ranged" :
        xmin=minmax[1][0]
        xmax=minmax[1][1]
        xmindef=minmax[1][0]
        xmaxdef=minmax[1][1]
    else :
        if minmax[1][0] < 0 and not withFolder: xmin=-1.0
        else : xmin=0.0
        xmax=1.0
        xmaxdef=minmax[1][1]
        xmindef=minmax[1][0]
    #print ("enumerate(nbin): ",enumerate(nbin), ", nbin: ",nbin)
    isMoreThan02 = 0
    bin_isMoreThan02 = 0
    for nn,nbins in enumerate(nbin) :
        print ("nbins: %s" % nbins)
        print ("targetBinning", targetBinning)
        file = TFile("%s.root" % histSource ,"READ");
        print ("Opened %s.root" % histSource)
        file.cd()
        histograms=[]
        histograms2=[]
        h2 = TH1F()
        hSum = TH1F()
        hFakes = TH1F()
        hSumAll = TH1F()
        ratiohSum=1.
        ratiohSumP=1.
        name = histSource.split("/")[len(histSource.split("/"))-1] + "_" + str(nbins) + nameOutFileAddL + ".root"
        nameOutFile = "%s/%s" % (outdir, name)
        fileOut  = TFile(nameOutFile, "recreate")
        print ("created %s" % nameOutFile)
        if withFolder :
            folders_Loop = file.GetListOfKeys()
        else :
            folders_Loop = ["none"]
        for nkey, keyF in enumerate(folders_Loop) :
            print ("nkey: ",nkey,", keyF: ",keyF)
            if withFolder :
                if partialCopy :
                    if str(source) not in str(keyF.GetName()) : continue
                obj =  keyF.ReadObj()
                loop_on = obj.GetListOfKeys()
                histograms=[]
                histograms2=[]
                h2 = TH1F()
                hSum = TH1F()
                hFakes = TH1F()
                hSumAll = TH1F()
                ratiohSum=1.
                ratiohSumP=1.
            else :
                loop_on = file.GetListOfKeys()
            print ("withFolder", withFolder)
            for keyO in loop_on :

               if not withFolder :
                   obj = keyO.ReadObj()
                   if not (type(obj) is TH1F or type(obj) is TH1D ) :
                       continue
                   h2  = obj.Clone()
               else :
                   print ("keys ", keyF.GetName(), keyO.GetName() )
                   obj = keyO.ReadObj()
                   if not (type(obj) is TH1F  or type(obj) is TH1D ):
                       continue
                   h2  = obj.Clone()
                   print (h2.GetName(), h2.Integral())
               factor=1.
               if  not h2.GetSumw2N() :
                   h2.Sumw2()
               if  not hSum.GetSumw2N() :
                   hSum.Sumw2()
               if withFolder :
                   h2.SetName(str(h2.GetName()))
               histograms.append(h2.Clone())
               if "fakes_data" in h2.GetName() : hFakes=h2.Clone()
               ####
               print ("keys 2", h2.GetName())
               if doFlat == "VBFnode" :
                   condition = h2.GetName().find("qqHH_CV_1_C2V_2_kl_1_") == 0
               elif doFlat == "GGFnode" :
                   condition = h2.GetName().find("ggHH_kl_1_kt_1_") == 0
               elif  doFlat == "Hnode" :
                   condition = h2.GetName().find("WH_") == 0 or h2.GetName().find("ZH_") == 0 or h2.GetName().find("VH_") == 0 or h2.GetName().find("qqH_") == 0 or h2.GetName().find("ggH_") == 0 or h2.GetName().find("ttH_") == 0 or h2.GetName().find("tHq_") == 0 or h2.GetName().find("tHW_") == 0
               else :
                   condition = h2.GetName().find("HH") ==-1 or h2.GetName().find("hh") ==-1
               #####
               if (condition) and h2.GetName().find("data_obs") ==-1 and h2.GetName().find("CMS") ==-1 and h2.GetName().find("Up") ==-1 and h2.GetName().find("Down") ==-1:
                   #hSumDumb2 = obj # h2_rebin #
                   if BINtype=="quantiles" :
                       print ("sum to quantiles in BKG:", h2.GetName(), h2.Integral())
                   if not hSumAll.Integral()>0 :
                       hSumAll=h2.Clone()
                       hSumAll.Sumw2()
                       hSumAll.SetName("hSumAllBk1")
                   else :
                       hSumAll.Add(h2)
            #################################################
            print ("Sum of BKG: ", hSumAll.Integral(), ", hFakes.Integral: ",hFakes.Integral())
            if BINtype=="quantiles" :
                if len(targetBinning) > 0 :
                    nbinsQuant = targetBinning
                else :
                    nbinsQuant =  getQuantiles(hSumAll, nbins, xmax)
            print ("Bins by quantiles ",nbins,nbinsQuant)
            if withFolder :
                fileOut.mkdir(keyF.GetName()+"/")
            histo = TH1F()
            for nn1, histogram in enumerate(histograms) :
                #print ("nn1: ",nn1,", histogram: ",histogram,", histo:",histo.GetName())
                #if BINtype=="quantiles" : ### fix that -- I do not want these written to the file
                histogramCopy=histogram.Clone()
                nameHisto=histogramCopy.GetName()
                histogram.SetName(histogramCopy.GetName())
                histogramCopy.SetName(histogramCopy.GetName())
                if BINtype=="none" :
                    histo=histogramCopy.Clone()
                    histo.SetName(nameHisto)
                elif BINtype=="ranged" or BINtype=="regular" :
                    histo= TH1F( nameHisto, nameHisto , nbins , xmin , xmax)
                elif BINtype=="quantiles" :
                    xmaxLbin=xmaxLbin+[nbinsQuant[nbins-2]]
                    histo=TH1F( nameHisto, nameHisto , nbins , nbinsQuant) # nbins+1 if first is zero
                elif BINtype=="mTauTauVis" :
                    histo= TH1F( nameHisto, nameHisto , nbins , 0. , 200.)
                histo.Sumw2()
                #if BINtype=="quantiles" : ### fix that -- I do not want these written to the file
                for place in range(0,histogramCopy.GetNbinsX() + 1) :
                    content =      histogramCopy.GetBinContent(place)
                    #if content < 0 : continue # print (content,place)
                    binErrorCopy = histogramCopy.GetBinError(place);
                    newbin =       histo.GetXaxis().FindBin(histogramCopy.GetXaxis().GetBinCenter(place))
                    binError =     histo.GetBinError(newbin);
                    contentNew =   histo.GetBinContent(newbin)
                    histo.SetBinContent(newbin, content+contentNew)
                    histo.SetBinError(newbin, sqrt(binError*binError+binErrorCopy*binErrorCopy))
                if withFolder :
                    #print (histo.GetName(),histo.Integral(), BINtype)
                    fileOut.cd("/"+keyF.GetName()+"/")
                    histo.Write("",TObject.kOverwrite)
                    fileOut.cd()
                    print ("histo.Write("",TObject.kOverwrite) withFolder :: histoName: ",histo.GetName())
                else :
                    histogram.Write("",TObject.kOverwrite)
                    histo.Write("",TObject.kOverwrite)
                    print ("histo.Write("",TObject.kOverwrite) :: histoName: ",histo.GetName())
                    if "fakes_data" in histo.GetName():
                        histoClone1 = histo.Clone(histo.GetName()+"_Norm")
                        histoClone1.Scale(1./histoClone1.Integral())
                        histoCumulative = histoClone1.GetCumulative()
                        histoCumulative.Write("",TObject.kOverwrite)
                print("targetBinning", targetBinning, nbinsQuant)
                continue
            print (nameOutFile+" created")
            print ("nkey ", nkey )
            if nkey == 0 :
                hSumCopy=hSumAll.Clone()
                print ("hSumCopy for rebinning:: hSumCopy.Name: ",hSumCopy.GetName())
                hSumi = TH1F()
                if BINtype=="ranged" or BINtype=="regular" : hSumi = TH1F( "hSumRebinned", "hSum" , nbins , xmin , xmax)
                elif BINtype=="quantiles" : hSumi = TH1F( "hSumRebinned", "hSum" , nbins , nbinsQuant)
                elif BINtype=="mTauTauVis" : hSumi = TH1F( "hSumRebinned", "hSum" , nbins , 0. , 200.)
                if not hSumi.GetSumw2N() : hSumi.Sumw2()
                for place in range(1,hSumCopy.GetNbinsX() + 2) :
                    content=hSumCopy.GetBinContent(place)
                    newbin=hSumi.FindBin(hSumCopy.GetBinCenter(place))
                    binErrorCopy = hSumCopy.GetBinError(place);
                    binError = hSumi.GetBinError(newbin);
                    hSumi.SetBinContent(newbin, hSumi.GetBinContent(newbin)+content)
                    hSumi.SetBinError(newbin,sqrt(binError*binError+ binErrorCopy*binErrorCopy))
                hSumi.SetBinErrorOption(1)
                if hSumi.GetBinContent(hSumi.GetNbinsX()) >0 :
                    ratiohSum=hSumi.GetBinError(hSumi.GetNbinsX())/hSumi.GetBinContent(hSumi.GetNbinsX())
                if hSumi.GetBinContent(hSumi.GetNbinsX()-1) >0 : ratiohSumP=hSumi.GetBinError(hSumi.GetNbinsX()-1)/hSumi.GetBinContent(hSumi.GetNbinsX()-1)
                errOcontSUMLast  = errOcontSUMLast+[ratiohSum] if ratiohSum<1.001 else errOcontSUMLast+[1.0]
                errOcontSUMPLast = errOcontSUMPLast+[ratiohSumP] if ratiohSumP<1.001 else errOcontSUMPLast+[1.0]
                errSUMLast       = errSUMLast+[hSumi.GetBinError(hSumi.GetNbinsX())]
                contSUMLast      = contSUMLast+[hSumi.GetBinContent(hSumi.GetNbinsX())]
                if ratiohSum > 0.199 or nbins > nQuantMax :
                    isMoreThan02 = isMoreThan02 + 1
                    if isMoreThan02 == 1 :
                        bin_isMoreThan02 = nbins
                fileOut.cd()
                if BINtype=="quantiles" and not len(targetBinning) > 0 :
                    print ("nbins: ",nbins)
                    print ("nbinsQuant: ",nbinsQuant)
                    lastQuant = lastQuant+[nbinsQuant[nbins]]   # original
                    xmaxQuant = xmaxQuant+[xmaxdef]
                    xminQuant = xminQuant+[xmindef]
                print ("it should be only one ",  nkey, errOcontTTLast)
    print ("min",xmindef,xmin)
    print ("max",xmaxdef,xmax)
    print ("isMoreThan02", isMoreThan02, bin_isMoreThan02)
    return [errOcontTTLast,errOcontTTPLast,errOcontSUMLast,errOcontSUMPLast,lastQuant,xmaxQuant,xminQuant, bin_isMoreThan02]

global ReadLimits
def ReadLimits(bdtType, nbin, BINtype,channel,local,nstart,ntarget, sendToCondor, toAdd):
    print ("ReadLimits:: bdtType: ",bdtType,", nbin:",nbin,", BINtype: ",BINtype,", channel: ",channel,", local: ",local,", ",nstart,", ntarget: ",ntarget)
    central=[]
    do1=[]
    do2=[]
    up1=[]
    up2=[]
    for nn,nbins in enumerate(nbin) :
        shapeVariable = "%s_%s%s" % (bdtType, str(nbins), nameOutFileAdd)
        #rint ("looking for ", os.path.join(local, "*%s*.log" % (shapeVariable)))
        if channel in [ "0l_2tau"] and sendToCondor :
            datacardFile_output = glob.glob(os.path.join(local, "%s*.out" % (shapeVariable)))[0]
        else :
            datacardFile_output = glob.glob(os.path.join(local, "*%s*.log" % (shapeVariable)))[0]
        if channel == "hh_3l":
            datacardFile_output = os.path.join(local, "hh_3l_%s.log" % shapeVariable)
        if nn==0 : print ("reading ", datacardFile_output)
        f = open(datacardFile_output, 'r+')
        lines = f.readlines() # get all lines as a list (array)
        for line in  lines:
          l = []
          tokens = line.split()
          if "Expected  2.5%"  in line : do2=do2+[float(tokens[4])]
          if "Expected 16.0%:" in line : do1=do1+[float(tokens[4])]
          if "Expected 50.0%:" in line : central=central+[float(tokens[4])]
          if "Expected 84.0%:" in line : up1=up1+[float(tokens[4])]
          if "Expected 97.5%:" in line : up2=up2+[float(tokens[4])]
    return [central,do1,do2,up1,up2]
