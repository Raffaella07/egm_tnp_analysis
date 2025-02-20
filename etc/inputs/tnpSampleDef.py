from libPython.tnpClassUtils import tnpSample

#github branches
#LegacyReReco2016: https://github.com/swagata87/egm_tnp_analysis/tree/Legacy2016_94XIDv2 
#ReReco2017: https://github.com/swagata87/egm_tnp_analysis/tree/tnp_2017datamc_IDV2_10_2_0
#PromptReco2018: https://github.com/swagata87/egm_tnp_analysis/tree/egm_tnp_Prompt2018_102X_10222018_MC102XECALnoiseFix200kRelVal
#UL2017: https://github.com/swagata87/egm_tnp_analysis/blob/UL2017Final/etc/inputs/tnpSampleDef.py

### eos repositories
eosLegacyReReco2016 = '/eos/cms/store/group/phys_egamma/swmukher/egmNtuple_V2ID_2016/'
eosReReco2017 = '/eos/cms/store/group/phys_egamma/swmukher/ntuple_2017_v2/'
eosReReco2018 = '/eos/cms/store/group/phys_egamma/swmukher/rereco2018/ECAL_NOISE/'
# UL Summer19
eosUL2016preVFP  = '/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016preVFP/merged/'
eosUL2016postVFP = '/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016postVFP/merged/'
eosUL2017 = '/eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20/UL2017/merged/'
eosUL2018 = '/eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20/UL2018/merged/'
#Run3
eosRun3 = '/eos/cms/store/group/phys_egamma/ec/nkasarag/EGM_comm/'
eos2023 = '/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023/'

ReReco2017 = {

    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosReReco2017 + 'DYJetsToLL.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_1j_madgraph'              : tnpSample('DY_1j_madgraph',
                                       eosReReco2017 + 'DY1JetsToLLM50madgraphMLM.root',
                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
#                                       eosMoriond18 + 'DYJetsToLLM50amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'                 : tnpSample('DY_amcatnloext',
                                       eosReReco2017 + 'DYJetsToLLM50amcatnloFXFXext.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2017B' : tnpSample('data_Run2017B' , eosReReco2017 + 'RunB.root' , lumi = 4.793 ),
    'data_Run2017C' : tnpSample('data_Run2017C' , eosReReco2017 + 'RunC.root' , lumi = 9.753),
    'data_Run2017D' : tnpSample('data_Run2017D' , eosReReco2017 + 'RunD.root' , lumi = 4.320 ),
    'data_Run2017E' : tnpSample('data_Run2017E' , eosReReco2017 + 'RunE.root' , lumi = 8.802),
    'data_Run2017F' : tnpSample('data_Run2017F' , eosReReco2017 + 'RunF.root' , lumi = 13.567),

    }

LegacyReReco2016 = {

    'DY_madgraph' : tnpSample('DY_madgraph', 
                                        eosLegacyReReco2016 + 'TnPTree_DY_M50_madgraphMLM.root',
                                        isMC = True, nEvts =  -1 ),
    'DY_amcatnlo' : tnpSample('DY_amcatnlo', 
                                        eosLegacyReReco2016 + 'TnPTree_DY_M50_amcatnloFXFX.root',
                                        isMC = True, nEvts =  -1 ),

    'data_Run2016Bv2' : tnpSample('data_Run2017Bv2' , eosLegacyReReco2016 + 'TnPTree_2016B_2.root' , lumi = 5.785 ),
    'data_Run2016C' : tnpSample('data_Run2017C' , eosLegacyReReco2016 + 'TnPTree_2016C.root' , lumi = 2.573 ),
    'data_Run2016D' : tnpSample('data_Run2017D' , eosLegacyReReco2016 + 'TnPTree_2016D.root' , lumi = 4.248 ),
    'data_Run2016E' : tnpSample('data_Run2017E' , eosLegacyReReco2016 + 'TnPTree_2016E.root' , lumi = 3.947 ),
    'data_Run2016F' : tnpSample('data_Run2017F' , eosLegacyReReco2016 + 'TnPTree_2016F.root' , lumi = 3.102 ),
    'data_Run2016G' : tnpSample('data_Run2017G' , eosLegacyReReco2016 + 'TnPTree_2016G.root' , lumi = 7.540 ),
    'data_Run2016H' : tnpSample('data_Run2017H' , eosLegacyReReco2016 + 'TnPTree_2016H.root' , lumi = 7.813 ),



}


ReReco2018 = {
    ### MiniAOD TnP for IDs scale 

    'DY_madgraph'              : tnpSample('DY_madgraph',
                                            eosReReco2018 + 'DYJetsToLLmadgraphMLM.root',
                                            isMC = True, nEvts =  -1 ),

    'DY_powheg'              : tnpSample('DY_powheg',
                                            eosReReco2018 + 'DYToEEpowheg.root',
                                            isMC = True, nEvts =  -1 ),
    

    'data_Run2018A' : tnpSample('data_Run2018A' , eosReReco2018 + 'RunA.root' , lumi = 10.723),  
    'data_Run2018B' : tnpSample('data_Run2018B' , eosReReco2018 + 'RunB.root' , lumi = 5.964),
    'data_Run2018C' : tnpSample('data_Run2018C' , eosReReco2018 + 'RunC.root' , lumi = 6.382),
    'data_Run2018D' : tnpSample('data_Run2018D' , eosReReco2018 + 'RunD.root' , lumi = 29.181), 
}

UL2016_preVFP = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2016preVFP + 'DY_LO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2016preVFP + 'DY_NLO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2016B' : tnpSample('data_Run2016B' , eosUL2016preVFP + 'Run2016B_L1matched.root' , lumi = 5.9098246),
    'data_Run2016C' : tnpSample('data_Run2016C' , eosUL2016preVFP + 'Run2016C_L1matched.root' , lumi = 2.64992914),
    'data_Run2016D' : tnpSample('data_Run2016D' , eosUL2016preVFP + 'Run2016D_L1matched.root' , lumi = 4.292865604),
    'data_Run2016E' : tnpSample('data_Run2016E' , eosUL2016preVFP + 'Run2016E_L1matched.root' , lumi = 4.185165152),
    'data_Run2016F' : tnpSample('data_Run2016F' , eosUL2016preVFP + 'Run2016F_L1matched.root' , lumi = 2.725508364)
}

UL2016_postVFP = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2016postVFP + 'DY_LO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2016postVFP + 'DY_NLO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2016F' : tnpSample('data_Run2016F' , eosUL2016postVFP + 'Run2016F_L1merged.root' , lumi = 0.414987426),
    'data_Run2016G' : tnpSample('data_Run2016G' , eosUL2016postVFP + 'Run2016G_L1matched.root' , lumi = 7.634508755),
    'data_Run2016H' : tnpSample('data_Run2016H' , eosUL2016postVFP + 'Run2016H_L1matched.root' , lumi = 8.802242522)
    }

UL2017 = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2017 + 'DY_LO.root ',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2017 + 'DY_NLO.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2017B' : tnpSample('data_Run2017B' , eosUL2017 + 'Run2017B.root' , lumi = 4.793961427),
    'data_Run2017C' : tnpSample('data_Run2017C' , eosUL2017 + 'Run2017C.root' , lumi = 9.631214821),
    'data_Run2017D' : tnpSample('data_Run2017D' , eosUL2017 + 'Run2017D.root' , lumi = 4.247682053),
    'data_Run2017E' : tnpSample('data_Run2017E' , eosUL2017 + 'Run2017E.root' , lumi = 9.313642402),
    'data_Run2017F' : tnpSample('data_Run2017F' , eosUL2017 + 'Run2017F.root' , lumi = 13.510934811),
}

UL2018 = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2018 + 'DY_LO.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2018 + 'DY_NLO.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2018A' : tnpSample('data_Run2018A' , eosUL2018 + 'Run2018A.root' , lumi = 14.02672485),
    'data_Run2018B' : tnpSample('data_Run2018B' , eosUL2018 + 'Run2018B.root' , lumi = 7.060617355),
    'data_Run2018C' : tnpSample('data_Run2018C' , eosUL2018 + 'Run2018C.root' , lumi = 6.894770971),
    'data_Run2018D' : tnpSample('data_Run2018D' , eosUL2018 + 'Run2018D.root' , lumi = 31.74220577),
}

Run3 = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosRun3 + 'DYToEE_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8_EleID_PhoID/DYToEE_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8/DYToEE_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8_EleID_PhoID/221018_080249/0000/merged.root',
                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
#                                       eosUL2017 + 'DYJetsToLLM50amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnloext'                 : tnpSample('DY_amcatnloext',
#                                       eosUL2017 + 'DYJetsToLL_amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),


    'data_Run3B' : tnpSample('data_Run3B' , eosRun3 + 'ntuple_Run3_data_2022B_EleID_PhoID/data/EGamma/crab_Egamma2022B_EleID_PhoID/221012_155735/0000/merged.root' , lumi = 0.086),
    'data_Run3C' : tnpSample('data_Run3C' , eosRun3 + 'ntuple_Run3_data_2022C_EleID_PhoID/data/EGamma/crab_Egamma2022C_EleID_PhoID/221014_145533/0000/merged.root' , lumi = 4.45),
    'data_Run3D' : tnpSample('data_Run3D' , eosRun3 + 'ntuple_Run3_data_2022D_EleID_PhoID/data/EGamma/crab_Egamma2022D_EleID_PhoID/221014_145636/0000/merged.root' , lumi = 0.912),
    'data_Run3E' : tnpSample('data_Run3E' , eosRun3 + 'ntuple_Run3_data_2022E_EleID_PhoID/data/EGamma/crab_Egamma2022E_EleID_PhoID/221018_073725/0000/merged.root' , lumi = 2.08),
    'data_Run3F' : tnpSample('data_Run3F' , eosRun3 + 'ntuple_Run3_data_2022F_EleID_PhoID/data/EGamma/crab_Egamma2022F_EleID_PhoID/221114_171125/0000/merged.root' , lumi = 4.99),
    'data_Run3G' : tnpSample('data_Run3G' , eosRun3 + 'ntuple_Run3_data_2022G_EleID_PhoID/data/EGamma/crab_Egamma2022G_EleID_PhoID/221211_201213/0000/merged.root' , lumi = 2.43),
}

Run3_preleak = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosRun3 + 'Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/DYto2E_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8/crab_Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/231027_151954/0000/merged_Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2.root',
                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
#                                       eosUL2017 + 'DYJetsToLLM50amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnloext'                 : tnpSample('DY_amcatnloext',
#                                       eosUL2017 + 'DYJetsToLL_amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),


    'data_Run3B' : tnpSample('data_Run3B' , eosRun3 + 'ntuple_Run3_data_2022B_EleID_PhoID/data/EGamma/crab_Egamma2022B_EleID_PhoID/221012_155735/0000/merged.root' , lumi = 0.086),
    'data_Run3C' : tnpSample('data_Run3C' , eosRun3 + 'ntuple_Run3_data_2022C_EleID_PhoID/data/EGamma/crab_Egamma2022C_EleID_PhoID/221014_145533/0000/merged.root' , lumi = 4.45),
    'data_Run3D' : tnpSample('data_Run3D' , eosRun3 + 'ntuple_Run3_data_2022D_EleID_PhoID/data/EGamma/crab_Egamma2022D_EleID_PhoID/221014_145636/0000/merged.root' , lumi = 0.912),
    'data_Run3BCD' : tnpSample('data_Run3BCD' , eosRun3 + 'Run2022_BCD_ReReco/merged_Run2022_BCD_ReReco_up.root' , lumi = 5.45),
}

Run3_postleak = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosRun3 + 'Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2/DYto2E_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8/crab_Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2/231027_152558/0000/merged_Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2.root',
                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
#                                       eosUL2017 + 'DYJetsToLLM50amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnloext'                 : tnpSample('DY_amcatnloext',
#                                       eosUL2017 + 'DYJetsToLL_amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),


    'data_Run3E' : tnpSample('data_Run3E' , eosRun3 + 'Run2022E-22Sep2023-v1/EGamma/crab_Run2022E-22Sep2023-v1/231027_143318/0000/merged_Run2022E-22Sep2023-v1_up.root' , lumi = 5.62),
    'data_Run3F' : tnpSample('data_Run3F' , '/eos/cms/store/group/phys_egamma/ec/tnpTuples/rsalvatico/ntuples_Run3/PromptData2022/Run2022F.root' , lumi = 10),
    'data_Run3G' : tnpSample('data_Run3G' , '/eos/cms/store/group/phys_egamma/ec/tnpTuples/rsalvatico/ntuples_Run3/PromptData2022/Run2022G.root' , lumi = 11.1),
    'data_Run3EFG' : tnpSample('data_Run3EFG' , '/eos/cms/store/group/phys_egamma/ec/nkasarag/EGM_comm/Run2022_EReReco_FG_PromptReco/merged_Run2022_EReReco_FG_PromptReco_updated.root' , lumi = 26.72),
}


Run3_2023_preBPIX = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eos2023 + 'DY_LO_2023preBPIX.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
                                       eos2023 + 'DY_NLO_2023preBPIX.root',
                                       isMC = True, nEvts =  -1 ),


    'data_2023' : tnpSample('data_2023' , eos2023 + 'data_2023C.root' , lumi = 18.0),
}

Run3_2023_postBPIX = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eos2023 + 'photonIDpostBPIXntuples/DY_LO_2023postBPIX.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
                                       eos2023 + 'photonIDpostBPIXntuples/DY_NLO_2023postBPIX.root',
                                       isMC = True, nEvts =  -1 ),


    'data_2023' : tnpSample('data_2023' , eos2023 + 'photonIDpostBPIXntuples/data_2023D.root' , lumi = 9.52),
}

