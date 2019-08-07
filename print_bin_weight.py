#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math

ROOT.gROOT.SetBatch(True)

#pileup2016file = TFile('pileUPinfo2016.root')
#pileup2016file = TFile('PU_Reweight_2016.root')
#pileup2016histo=pileup2016file.Get('hpileUPhist')
#pileup2016histo=pileup2016file.Get('pileup')

#Electron Trigger reweights
eleTrigReweightFile = TFile('scalefactors/electron_Trigger_eleTrig.root')
eleTrig_hEffEtaPt = eleTrigReweightFile.Get('hEffEtaPt')
eleTrig_hEffEtaPtUp = eleTrigReweightFile.Get('hErrhEtaPt')
eleTrig_hEffEtaPtDown = eleTrigReweightFile.Get('hErrlEtaPt')

#Electron Reconstruction efficiency. Scale factors for 80X
eleRecoSFsFile_ptgt_20 = TFile('scalefactors/electron_Reco_SFs_egammaEffi_txt_EGM2D.root')
eleRecoSF_EGamma_SF2D_ptgt_20 = eleRecoSFsFile_ptgt_20.Get('EGamma_SF2D')

eleRecoSFsFile_ptlt_20 = TFile('scalefactors/electron_Reco_SFs_egammaEffi_txt_EGM2D_ptlt_20.root')
eleRecoSF_EGamma_SF2D_ptlt_20 = eleRecoSFsFile_ptlt_20.Get('EGamma_SF2D')

#Loose electron ID SFs
eleLooseIDSFsFile = TFile('scalefactors/electron_Loose_ID_SFs_egammaEffi_txt_EGM2D.root')
eleLooseIDSF_EGamma_SF2D = eleLooseIDSFsFile.Get('EGamma_SF2D')

#Tight electron ID SFs
phoTightIDSFsFile = TFile('scalefactors/photon_Tight_ID_SFs_egammaEffi_txt_EGM2D.root')
phoTightIDSF_EGamma_SF2D = phoTightIDSFsFile.Get('EGamma_SF2D')

#Loose photon ID SFs
phoLooseIDSFsFile = TFile('scalefactors/photon_Loose_ID_SFs_egammaEffi_txt_EGM2D.root')
phoLooseIDSF_EGamma_SF2D = phoLooseIDSFsFile.Get('EGamma_SF2D')

#Tight photon ID SFs
eleTightIDSFsFile = TFile('scalefactors/electron_Tight_ID_SFs_egammaEffi_txt_EGM2D.root')
eleTightIDSF_EGamma_SF2D = eleTightIDSFsFile.Get('EGamma_SF2D')

# Veto cut-based electron ID SFs
eleVetoCutBasedIDSFsFile = TFile('scalefactors/electron_Veto_cut-based_ID_SFs_egammaEffi_txt_EGM2D.root')
eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D = eleVetoCutBasedIDSFsFile.Get('EGamma_SF2D')

#Muon Trigger SFs
#BCDEF
muonTrigSFsRunBCDEFFile = TFile('scalefactors/muon_single_lepton_trigger_EfficienciesAndSF_RunBtoF.root')
muonTrigSFs_EfficienciesAndSF_RunBtoF = muonTrigSFsRunBCDEFFile.Get('IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio')
#GH
muonTrigSFsRunGHFile = TFile('scalefactors/muon_single_lepton_trigger_EfficienciesAndSF_Period4.root')
muonTrigSFs_EfficienciesAndSF_Period4 = muonTrigSFsRunBCDEFFile.Get('IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio')

#Muon ID SFs
#BCDEF
muonIDSFsBCDEFFile = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_BCDEF.root')
muonLooseIDSFs_EfficienciesAndSF_BCDEF = muonIDSFsBCDEFFile.Get('NUM_LooseID_DEN_genTracks_eta_pt')
muonTightIDSFs_EfficienciesAndSF_BCDEF = muonIDSFsBCDEFFile.Get('NUM_TightID_DEN_genTracks_eta_pt')
#GH
muonIDSFsGHFile = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_GH.root')
muonLooseIDSFs_EfficienciesAndSF_GH = muonIDSFsGHFile.Get('NUM_LooseID_DEN_genTracks_eta_pt')
muonTightIDSFs_EfficienciesAndSF_GH = muonIDSFsGHFile.Get('NUM_TightID_DEN_genTracks_eta_pt')

#for low pt muons
#BCDEF
muonIDSFsBCDEFFile_lowpt = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_BCDEF_lowpt.root')
muonLooseIDSFs_EfficienciesAndSF_lowpt_BCDEF = muonIDSFsBCDEFFile_lowpt.Get('NUM_LooseID_DEN_genTracks_pt_abseta')
#GH
muonIDSFsGHFile_lowpt = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_GH_lowpt.root')
muonLooseIDSFs_EfficienciesAndSF_lowpt_GH = muonIDSFsGHFile_lowpt.Get('NUM_LooseID_DEN_genTracks_pt_abseta')

#Muon Iso SFs
#BCDEF
muonIsoSFsBCDEFFile = TFile('scalefactors/muon_Iso_SFs_EfficienciesAndSF_BCDEF.root')
muonLooseIsoSFs_EfficienciesAndSF_BCDEF = muonIsoSFsBCDEFFile.Get('NUM_LooseRelIso_DEN_LooseID_eta_pt')
muonTightIsoSFs_EfficienciesAndSF_BCDEF = muonIsoSFsBCDEFFile.Get('NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt')
#GH
muonIsoSFsGHFile = TFile('scalefactors/muon_Iso_SFs_EfficienciesAndSF_GH.root')
muonLooseIsoSFs_EfficienciesAndSF_GH = muonIsoSFsGHFile.Get('NUM_LooseRelIso_DEN_LooseID_eta_pt')
muonTightIsoSFs_EfficienciesAndSF_GH = muonIsoSFsGHFile.Get('NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt')

#Muon Tracking SFs
muonTrackingSFsFile = TFile('scalefactors/muon_Tracking_SFs_Tracking_EfficienciesAndSF_BCDEFGH.root')
muonTrackingSFs_EfficienciesAndSF_BCDEFGH = muonTrackingSFsFile.Get('ratio_eff_aeta_dr030e030_corr')


#MET Trigger reweights
metTrigEff_zmmfile = TFile('scalefactors/metTriggerEfficiency_zmm_recoil_monojet_TH1F.root')
metTrig_firstmethod = metTrigEff_zmmfile.Get('hden_monojet_recoil_clone_passed')

metTrigEff_secondfile = TFile('scalefactors/metTriggerEfficiency_recoil_monojet_TH1F.root')
metTrig_secondmethod = metTrigEff_secondfile.Get('hden_monojet_recoil_clone_passed')


# In[2]:


sf_list = [eleTrig_hEffEtaPt,eleRecoSF_EGamma_SF2D_ptgt_20,eleRecoSF_EGamma_SF2D_ptlt_20,eleLooseIDSF_EGamma_SF2D,eleTightIDSF_EGamma_SF2D,muonTrigSFs_EfficienciesAndSF_RunBtoF,muonTrigSFs_EfficienciesAndSF_Period4,muonLooseIDSFs_EfficienciesAndSF_BCDEF,muonLooseIDSFs_EfficienciesAndSF_GH,muonTightIDSFs_EfficienciesAndSF_BCDEF,muonTightIDSFs_EfficienciesAndSF_GH,muonLooseIsoSFs_EfficienciesAndSF_BCDEF,muonLooseIsoSFs_EfficienciesAndSF_GH,muonTightIsoSFs_EfficienciesAndSF_BCDEF,muonTightIsoSFs_EfficienciesAndSF_GH,muonTrackingSFs_EfficienciesAndSF_BCDEFGH]

sf_list_dict = {eleTrig_hEffEtaPt:'eleTrig_hEffEtaPt',eleRecoSF_EGamma_SF2D_ptgt_20:'eleRecoSF_EGamma_SF2D_ptgt_20',eleRecoSF_EGamma_SF2D_ptlt_20:'eleRecoSF_EGamma_SF2D_ptlt_20',eleLooseIDSF_EGamma_SF2D:'eleLooseIDSF_EGamma_SF2D',eleTightIDSF_EGamma_SF2D:'eleTightIDSF_EGamma_SF2D',muonTrigSFs_EfficienciesAndSF_RunBtoF:'muonTrigSFs_EfficienciesAndSF_RunBtoF',muonTrigSFs_EfficienciesAndSF_Period4:'muonTrigSFs_EfficienciesAndSF_Period4',muonLooseIDSFs_EfficienciesAndSF_BCDEF:'muonLooseIDSFs_EfficienciesAndSF_BCDEF',muonLooseIDSFs_EfficienciesAndSF_GH:'muonLooseIDSFs_EfficienciesAndSF_GH',muonTightIDSFs_EfficienciesAndSF_BCDEF:'muonTightIDSFs_EfficienciesAndSF_BCDEF',muonTightIDSFs_EfficienciesAndSF_GH:'muonTightIDSFs_EfficienciesAndSF_GH',muonLooseIsoSFs_EfficienciesAndSF_BCDEF:'muonLooseIsoSFs_EfficienciesAndSF_BCDEF',muonLooseIsoSFs_EfficienciesAndSF_GH:'muonLooseIsoSFs_EfficienciesAndSF_GH',muonTightIsoSFs_EfficienciesAndSF_BCDEF:'muonTightIsoSFs_EfficienciesAndSF_BCDEF',muonTightIsoSFs_EfficienciesAndSF_GH:'muonTightIsoSFs_EfficienciesAndSF_GH',muonTrackingSFs_EfficienciesAndSF_BCDEFGH:'muonTrackingSFs_EfficienciesAndSF_BCDEFGH'}


# In[3]:


f= open("weights.txt","w+")
for sf in sf_list:
    #ele_trig=[][]
    eta_bins=[]
    pt_bins=[]
    for bin in range(sf.GetXaxis().GetNbins()):
        if bin == 0:
            eta_bins.append(sf.GetXaxis().GetBinLowEdge( bin+1))
            eta_bins.append(sf.GetXaxis().GetBinUpEdge( bin+1))
        else:
            eta_bins.append(sf.GetXaxis().GetBinUpEdge( bin+1))

    for bin in range(sf.GetYaxis().GetNbins()):
        if bin==0:
            pt_bins.append(sf.GetYaxis().GetBinLowEdge( bin+1))
            pt_bins.append(sf.GetYaxis().GetBinUpEdge( bin+1))
        else:
            pt_bins.append(sf.GetYaxis().GetBinUpEdge( bin+1))
    print ('For ',sf_list_dict[sf],':\n')
    f.write('For '+sf_list_dict[sf]+':\n')
    print ('#Eta bin: '+ str(sf.GetXaxis().GetNbins()),' #pT bin: '+str(sf.GetYaxis().GetNbins()))
    f.write('#Eta bin: '+str(sf.GetXaxis().GetNbins()))
    f.write('  #pT bin: '+str(sf.GetYaxis().GetNbins())+'\n')
    print ('eta_bins ',eta_bins)
    f.write ('eta_bins '+str(eta_bins)+'\n')
    print ('pt_bins',pt_bins)
    f.write ('pt_bins '+str(pt_bins)+'\n')
    ptlist=[];ptlistUp=[];ptlistDown=[]
    if 'muonTrackingSFs_EfficienciesAndSF_BCDEFGH' in sf_list_dict[sf]:
        for j in eta_bins:
            ptlist.append(sf.Eval(j))
            ptlistUp.append(sf.Eval(j) + sf.GetErrorYhigh(sf.GetYaxis().FindBin(j)))
            ptlistDown.append(sf.Eval(j) - sf.GetErrorYlow(sf.GetYaxis().FindBin(j)))
    else:     
        for i in range(sf.GetYaxis().GetNbins()):
            etalist=[]; etalistUp=[]; etalistDown=[]
            for j in range(sf.GetXaxis().GetNbins()):
                if 'eleRecoSF' in sf_list_dict[sf]:
                    etalist.append(sf.GetBinContent(j,1))
                elif 'muonLooseIDSFs_EfficienciesAndSF_lowpt_GH' in sf_list_dict[sf]:
                    etalist.append(sf.GetBinContent(i,j))
                else:
                    etalist.append(sf.GetBinContent(j,i) )
                if 'eleTrig' in sf_list_dict[sf]:
                    etalistUp.append(eleTrig_hEffEtaPt.GetBinContent(i,j) + eleTrig_hEffEtaPtUp.GetBinContent(i,j))
                    etalistDown.append(eleTrig_hEffEtaPt.GetBinContent(i,j) - eleTrig_hEffEtaPtDown.GetBinContent(i,j))
                elif 'eleRecoSF' in sf_list_dict[sf]:
                    etalistUp.append(sf.GetBinContent(j,1) + sf.GetBinErrorUp(j,1))
                    etalistDown.append(sf.GetBinContent(j,1) - sf.GetBinErrorLow(j,1))
                elif 'muonLooseIDSFs_EfficienciesAndSF_lowpt_GH' in sf_list_dict[sf]:
                    etalistUp.append(sf.GetBinContent(i,j) + sf.GetBinErrorUp(i,j))
                    etalistDown.append(sf.GetBinContent(i,j) - sf.GetBinErrorLow(i,j))
                else:
                    etalistUp.append(sf.GetBinContent(j,i) + sf.GetBinErrorUp(j,i))
                    etalistDown.append(sf.GetBinContent(j,i) - sf.GetBinErrorLow(j,i))
                #print(sf.GetBinContent(i,j))
            ptlist.append(etalist)
            ptlistUp.append(etalistUp)
            ptlistDown.append(etalistDown)
    f.write('weight Central: '+ str(ptlist))
    f.write ('\n')
    f.write ('weight Up: '+ str(ptlistUp))
    f.write ('\n')
    f.write ('weight Down: '+str(ptlistDown))
    f.write ('\n\n')
    print ('weight Central: ', ptlist)
    print ('\n')
    print ('weight Up: ', ptlistUp)
    print ('\n')
    print ('weight Down: ', ptlistDown)
    print ('\n\n')
    
f.close()
    


# In[ ]:




