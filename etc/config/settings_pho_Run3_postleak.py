#############################################################
########## General settings
#############################################################
# flag to be Tested
flags = {
    'passingCutBasedVeto94XV2'    : '(passingCutBasedVeto94XV2   == 1)',
    'passingCutBasedLoose94XV2'   : '(passingCutBasedLoose94XV2  == 1)',
    'passingCutBasedMedium94XV2'  : '(passingCutBasedMedium94XV2 == 1)',
    'passingCutBasedTight94XV2'   : '(passingCutBasedTight94XV2  == 1)',
    'passingMVA94Xwp80isoV2' : '(passingMVA94Xwp80isoV2 == 1)',
    'passingMVA94Xwp90isoV2' : '(passingMVA94Xwp90isoV2 == 1)',
    'passingMVA94Xwp80noisoV2' : '(passingMVA94Xwp80noisoV2 == 1)',
    'passingMVA94Xwp90noisoV2' : '(passingMVA94Xwp90noisoV2 == 1)',
    'passingCutBasedVeto122XV1'    : '(passingCutBasedVeto122XV1 == 1)',
    'passingCutBasedLoose122XV1'    : '(passingCutBasedLoose122XV1 == 1)',
    'passingCutBasedMedium122XV1'    : '(passingCutBasedMedium122XV1 == 1)',
    'passingCutBasedTight122XV1'    : '(passingCutBasedTight122XV1 == 1)',
    'passingMVA122Xwp80V1'    : '(passingMVA122Xwp80V1 == 1)',
    'passingMVA122Xwp90V1'    : '(passingMVA122Xwp90V1 == 1)',
    'passingCutBasedVetoRun3V1'    : '(passingCutBasedVetoRun3V1 == 1)',
    'passingCutBasedLooseRun3V1'    : '(passingCutBasedLooseRun3V1 == 1)',
    'passingCutBasedMediumRun3V1'    : '(passingCutBasedMediumRun3V1 == 1)',
    'passingCutBasedTightRun3V1'    : '(passingCutBasedTightRun3V1 == 1)',
    'passingMVARun3Xwp80isoV1'    : '(passingMVARun3Xwp80isoV1 == 1)',
    'passingMVARun3Xwp90isoV1'    : '(passingMVARun3Xwp90isoV1 == 1)',
    'passingMVA122XV1wp80'        : '(passingMVA122XV1wp80 == 1)',
    'passingMVA122XV1wp90'        : '(passingMVA122XV1wp90 == 1)',
    }

baseOutDir = 'results/Run3_postleak_dev/tnpPhoID/'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpPhoIDs'

samplesDef = {
    'data'   : tnpSamples.Run3_postleak['data_Run3EFG'].clone(),
    'mcNom'  : tnpSamples.Run3_postleak['DY_madgraph'].clone(),
    #'mcAlt'  : tnpSamples.Run3['DY_amcatnloext'].clone(),
    'tagSel' : tnpSamples.Run3_postleak['DY_madgraph'].clone(),
}
## can add data sample easily
#samplesDef['data'].add_sample( tnpSamples.Run3['data_Run3G'] )
#samplesDef['data'].add_sample( tnpSamples.Run3['data_Run3G'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 37')

## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

## set MC weight, can use several pileup rw for different data taking 
weightName = 'weights_data_Run2022EFG.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/eos/cms/store/group/phys_egamma/ec/nkasarag/EGM_comm/PU/EFG_2022/mcRun3_130X_2022_realistic_postEE_pho_80mb.pu.puTree.root')
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/eos/cms/store/group/phys_egamma/ec/nkasarag/EGM_comm/PU/PU_Run2_EFG_updated/mcRun3_130X_2022_realistic_postEE_pho.pu.puTree.root')
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('/eos/cms/store/group/phys_egamma/swmukher/UL2017/PU_miniAOD/DY_amcatnloext_ele.pu.puTree.root')
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('/eos/cms/store/group/phys_egamma/ec/nkasarag/EGM_comm/PU/PU_Run2_EFG_updated/mcRun3_130X_2022_realistic_postEE_pho.pu.puTree.root')

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'ph_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442,-0.8,0.0,0.8,1.4442,1.566,2.0,2.5] },
   { 'var' : 'ph_et' , 'type': 'float', 'bins': [10,20,35,50,100,500] },
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#LS: we removed the met cuts cause JEC not ready for UL2017        
additionalCuts = { 
   0 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   1 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   2 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   3 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   4 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   5 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   6 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   7 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   8 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
   9 : 'tag_Ele_pt > 60 && tag_Ele_Iso122X> 0.99',
}

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-7,-5.0,5.0]","sigmaP[1.0,0.5,3.0]",
    "meanF[-1,-5.0,5.0]","sigmaF[1.0,0.5,3.0]",
    "acmsP[50.,40.,70.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,40.,70.]","betaF[0.08,0.01,0.1]","gammaF[0.3, -1, 1]","peakF[90.0]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-10.0,10.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.5,0.5,6.0]","sosF[2,1.0,10.0]",
    "acmsP[60.,50.,75.]","betaP[0.05,0.01,0.08]","gammaP[0.2, 0.005, 1]","peakP[90.0]",
    "acmsF[50.,40.,75.]","betaF[0.05,0.01,0.08]","gammaF[0.2, 0.001, 1]","peakF[90.0]",
    ]
    
tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "meanGF[80.0,70.0,100.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,85.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]

tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[0.5,-5.0,5.0]","sigmaF[1.9,0.5,6.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
        
tnpParAltBkgFit_pol = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[0.5,-5.0,5.0]","sigmaF[1.9,0.5,6.0]",
    "meanGF[80.0,70.0,100.0]","sigmaGF[10,1.0,30.0]",
    "a1_P[0.,-5.,5.]","a2_P[0.,-5.,5.]","a3_P[0.,-5.,5.]","a4_P[0.,-5.,5.]",
    "a1_F[-0.1.,-1.,0.]","a2_F[-0.2.,-1.,0]","a3_F[0.,-5.,5.]","a4_F[0.,-5.,5.]",
    ]
        
