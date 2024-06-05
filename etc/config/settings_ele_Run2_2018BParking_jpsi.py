#############################################################
# General settings

# flag to be Tested
idbdtlppass = '(probeIsPF==1) && (probePfmvaId > %f )' % -3.0
idbdtlppassEB = '(probeIsPF==1) && probeAbsEta<1.5 && (probePfmvaId > %f )' % -3.0
#idbdtlppassEE = '(probeIsPF==1) && probeAbsEta>1.5 && (probePfmvaId > %f )' % -3.0

# flag to be Tested
flags = {
    'passingIdPF_LxySBins'  : idbdtlppass,
    'passingIdPFEB'  : idbdtlppassEB,
   # 'passingIdPFEE'  : idbdtlppassEE,
    }
baseOutDir = 'results/test/'

#############################################################
# Samples definition  - preparing the samples

### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpAna'

samplesDef = {
    'data'   : tnpSamples.Parking_Jan16['data_Run2018ALL'].clone(),
    'mcNom'  : tnpSamples.Parking_Jan16['BuToKJpsi'].clone(),
    'mcAlt'  : tnpSamples.Parking_Jan16['BuToKJpsi'].clone(),
    'tagSel' : tnpSamples.Parking_Jan16['BuToKJpsi'].clone(),
}

## if you need to use 2 times the same sample, then rename the second one
if not samplesDef['mcAlt'] is None:
    samplesDef['mcAlt'].rename('BuToKJpsi_mcAlt')
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('BuToKJpsi_tagSel')

## set MC weight
weightName = 'weight'    # 1 for data; pu_weight for MC   
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

#############################################################
# Bining definition  [can be nD bining]
biningDef = [
    # EB
    { 'var' : 'probePt' , 'type': 'float', 'bins': [2.0, 5.0,100.0] },
    { 'var' : 'B_xysig' , 'type': 'float', 'bins': [0.0,50.0,150.0,10000.0] },
    # EE
#    { 'var' : 'probeAbsEta' , 'type': 'float', 'bins': [1.5,3.0] },
    #{ 'var' : 'probePt' , 'type': 'float', 'bins': [0.5,2.0,5.0,100.0] },
]

#############################################################
# Cuts definition for all samples
# EB
cutBase = 'probePt>0.5 && probePt<100 && probeIsPF==1 && hlt_9ip6 && ((tagMvaId>5 && tagMvaId!=20) ||( tagPfmvaId!=20 )) && B_mass<6 && B_mass>5  && probeAbsEta<1.5'
# EE
#cutBase = 'probePt>0.5 && probePt<100 && probeIsPF==1 && probeAbsEta>1.5 && (tagMvaId>4 && tagMvaId!=20) && B_pt>15 && B_svprob>0.1 && B_cos2d>0.99'
#cutBase = 'probePt>0.5 && probePt<30 && probeIsPF==1 && hlt_9ip6 && probeAbsEta>1.5'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = {
0: 'tagPt>7',
3: 'tagPt>7'
}

# or remove any additional cut (default)
#additionalCuts = None

#############################################################
# Fitting params to tune fit by hand if necessary
tnpParAltSigFitJPsi = [
    "meanP[3.1,2.8,3.4]","sigmaP[0.1,0.01,3.0]",      
    "meanF[3.1,2.8,3.4]","sigmaF[0.1,0.01,1.0]",
    "alphaP[0.5, 0.2, 0.8]",
    "alphaF[0.5, 0.2, 0.8]",    
    ]

tnpParNomFitJPsi = [

    # EB with pT 0.5-1.5 
    # with fix sigmaF, meanF, alphaLF, alphaRF, nLF, nRF to those for passing
    # 26 bin, 2.3-3.6
    #"meanP[3.0969, 3.095, 3.098]","sigmaP[0.05, 0.03, 0.1]","alphaLP[0.6, 0.2, 0.7]","alphaRP[1.2, 1.0, 1.5]","nLP[3.6, 3.56, 3.64]","nRP[1.85, 1.80, 1.95]",
    #"meanF[3.0969, 3.09, 3.10]","sigmaF[0.05, 0.03, 0.1]","alphaLF[0.6, 0.2, 0.7]","alphaRF[1.2, 0.8, 1.5]","nLF[3.6, 3.56, 3.64]","nRF[1.85, 1.80, 1.95]",
    #"expalphaP[0.5, 0.2, 0.8]",
    #"expalphaF[0.5, 0.2, 0.8]",   

    # EB with pT 1.5-2  - old
    # with fix sigmaF=sigmaP  
    # 26 bin, 2.3-3.6  
    #"meanP[3.0969, 3.08, 3.10]","sigmaP[0.05, 0.03, 0.1]","alphaLP[0.6, 0.2, 0.7]","alphaRP[1.2, 1.0, 1.5]","nLP[3.6, 3.56, 3.64]","nRP[1.85, 1.80, 1.95]",
    #"meanF[3.0969, 3.09, 3.10]","sigmaF[0.05, 0.03, 0.1]","alphaLF[0.6, 0.2, 0.7]","alphaRF[1.2, 1.0, 1.5]","nLF[3.6, 3.56, 3.64]","nRF[1.85, 1.80, 1.95]",
    #"expalphaP[0.5, -0.2, 0.8]",
    #"expalphaF[0.5, 0.2, 0.8]",   

    # EB with pT 1.5-2  - new
    # with fix sigmaF=sigmaP  
    # 26 bin, 2.3-3.6  
   # "meanP[3.0969, 3.09, 3.10]","sigmaP[0.05, 0.04, 0.1]","alphaLP[0.4, 0.2, 0.7]","alphaRP[1.2, 1.0, 1.3]","nLP[3.5, 3.4, 3.64]","nRP[1.85, 1.80, 1.95]",
   # "meanF[3.0969, 3.09, 3.10]","sigmaF[0.05, 0.03, 0.1]","alphaLF[0.6, 0.2, 0.7]","alphaRF[1.2, 1.0, 1.5]","nLF[3.6, 3.56, 3.64]","nRF[1.85, 1.80, 1.95]",
    "meanP[3.09, 3.07, 3.095]","sigmaP[0.04, 0.03, 0.06]","alphaLP[2.0, 0.2, 6.0]","alphaRP[4.0, 0.3, 6.0]","nLP[4.5, 3.0, 10.0]","nRP[3.0, 1.80, 15.0]",
    "meanF[3.09, 3.07, 3.095]","sigmaF[0.03, 0.02, 0.04]","alphaLF[0.5, 0.1, 0.8]","alphaRF[0.9, 0.6, 2.0]","nLF[3.5, 3.3, 4.0]","nRF[1.85, 1.80, 2]",
    "expalphaP[0., -1.5, 0.5]",
    "expalphaF[0.5, -1, 1]",   

   #   EB with pT 2-5 and pT>5
    #  with fix sigmaF, alphaLF, alphaRF, nLF, nRF to those for passing. NB: meanF free
    #  18 bin, 2.6-3.5   
    # "meanP[3.09, 3.085, 3.095]","sigmaP[0.05, 0.03, 0.1]",  "alphaLP[0.6, 0.2, 0.7]","alphaRP[1.2, 1.0, 1.5]","nLP[3.6, 3.56, 3.64]","nRP[1.80, 1.70, 1.95]",
    # "meanF[3.082, 3.070, 3.085]","sigmaF[0.01, 0.001, 0.03]","alphaLF[0.6, 0.2, 0.7]","alphaRF[1.2, 1.0, 1.5]","nLF[3.6, 3.56, 3.64]","nRF[1.85, 1.80, 1.95]",
    #"expalphaP[-0.75, -1., -0.5]",
    #"expalphaF[0., -0.5, 0.2]",       

    # EE with pT<5
    # with fix sigmaF, meanF, alphaLF, alphaRF, nLF, nRF to those for passing
    # 26 bin, 2.3-3.6
    #"meanP[3.0969, 3.095, 3.1]","sigmaP[0.05, 0.03, 0.12]","alphaLP[0.6, 0.2, 0.7]","alphaRP[0.75, 0.4, 1.]","nLP[3.5, 3.4, 3.60]","nRP[1.85, 1.80, 1.95]",
    #"meanF[3.0969, 3.095, 3.098]","sigmaF[0.05, 0.03, 0.1]","alphaLF[0.6, 0.2, 0.7]","alphaRF[1.2, 1.0, 1.5]","nLF[3.6, 3.56, 3.64]","nRF[1.85, 1.80, 1.95]",
    #"expalphaP[0.6, -0.5, 1.]",
    #"expalphaF[0., -0.2, 0.8]",   
    
    # EE with pT>5 
    # with fix sigmaF, meanF, alphaLF, alphaRF, nLF, nRF to those for passing
    # 26 bin, 2.3-3.6
    #"meanP[3.0969, 3.09, 3.11]","sigmaP[0.05, 0.03, 0.2]",  "alphaLP[0.6, 0.2, 1.0]","alphaRP[1.0, 0.5, 1.2]","nLP[3.6, 3.56, 3.8]","nRP[1.85, 1.80, 1.95]",
    #"meanF[3.0969, 3.09, 3.11]","sigmaF[0.02, 0.01, 0.03]","alphaLF[0.6, 0.2, 0.7]","alphaRF[1.2, 1.0, 1.5]","nLF[3.6, 3.56, 3.64]","nRF[1.85, 1.80, 1.95]",
    #"expalphaP[0., -0.1, 0.8]",
    #"expalphaF[0., -0.2, 0.8]",   
    ]
     
tnpParAltBkgFitJPsi = [
    #"meanP[3.0969, 3.09, 3.10]","sigmaP[0.05, 0.03, 0.1]","alphaLP[0.3, 0.2, 0.7]","alphaRP[1.2, 1.0, 1.5]","nLP[3.5, 3.4, 3.64]","nRP[1.85, 1.80, 2.05]",
    #"meanF[3.0969, 3.09, 3.10]","sigmaF[0.05, 0.03, 0.1]","alphaLF[0.4, 0.2, 0.7]","alphaRF[1.2, 1.0, 1.3]","nLF[3.6, 3.56, 3.64]","nRF[1.85, 1.80, 1.95]",
   # "meanP[3.09, 3.07, 3.095]","sigmaP[0.04, 0.02, 0.06]","alphaLP[0.6, 0.2, 1.2]","alphaRP[1.0, 0.3, 1]","nLP[3.4, 3.0, 3.64]","nRP[1.85, 1.80, 3.5]",
   # "meanF[3.09, 3.07, 3.095]","sigmaF[0.03, 0.02, 0.06]","alphaLF[0.5, 0.1, 0.8]","alphaRF[0.9, 0.6, 1]","nLF[3.5, 3.3, 3.64]","nRF[1.85, 1.80, 2]",
    "cP[-0.1,-0.5,0.5]",
    "cF[0.5,-0.5,0.8]",
    ]

