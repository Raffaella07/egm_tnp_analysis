#!/usr/bin/env python
import os
import sys

# Add the parent directory to Python path for imports
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

#############################################################
########## General flags for running fitter
#############################################################
#flags = {
#    'doFit' : True,        # Essential: we want to fit
#    'doPlot': True,        # Essential: we want plots 
#    'doSyst': False,       # No systematics (data-only workflow)
#    'doMomCorr': False,    # No momentum corrections (data-only)
#    'doNomVsAlt': False,   # No nominal vs alternative (no MC)
#    'doFillTemplates': False, # No template filling needed
#}

#############################################################
########## Flags for specific ID working points 
#############################################################
# Define flags based on actual Parquet data columns
# Our Parquet files have columns: medium, tight, loose, etc.
flags = {
    # Actual working points available in Parquet data
    'passingCutBasedMedium122XV1'   : '(medium == 1)',
    'passingCutBasedTight122XV1'    : '(tight == 1)',
    'passingCutBasedLoose122XV1'    : '(loose == 1)',  # if available
    'passingCutBasedVeto122XV1'     : '(veto == 1)',   # if available
}

#############################################################
########## samples definition  - preparing the samples
#############################################################
### For Parquet workflow, we use pre-computed histograms
try:
    import etc.inputs.tnpSampleDef as tnpSamples
except ImportError:
    # If running as standalone script, try without the etc prefix
    try:
        sys.path.append('../../')
        import inputs.tnpSampleDef as tnpSamples
    except ImportError:
        print("Warning: Could not import tnpSampleDef. Continuing with minimal sample definitions.")
        tnpSamples = None

baseOutDir = 'results/Run3_2025_C/tnpEleID/'

# Since we're using pre-computed histograms from Parquet files,
# we define minimal sample structure for compatibility with --parquet mode
samplesDef = {
    'data'    : None,  # Will use pre-computed histograms from data Parquet
    'mcNom'   : None,  # Will use pre-computed histograms from MC Parquet
    'mcAlt'   : None,  # No alternative MC for now
    'tagSel'  : None,  # No tag selection MC for now
}

## tree on which to run (for compatibility)
tnpTreeDir = 'tnpEleIDs'

#############################################################
########## bining definition  [can be nD bining]  
#############################################################
# Use binning compatible with created histograms
biningDef = [
   { 'var' : 'el_eta' , 'type': 'float', 'bins': [-2.5, -2.0, -1.566, -1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 20, 35, 50, 100, 500] },
]

# Alternative: explicit bin ranges that match histogram creation
# This gives 11 pt bins  10 eta bins = 110 total bins (bin00 to bin109)

#############################################################
########## Cuts definition for all samples
#############################################################
### base cut - adapted for Parquet column names
cutBase = 'tag_Ele_pt > 35 && abs(tag_Ele_eta) < 2.17'

# Additional cuts per bin (can be used for systematic studies)
additionalCuts = { 
    0 : 'tag_Ele_pt > 35',  # Can add more specific cuts if needed
    1 : 'tag_Ele_pt > 35',
    2 : 'tag_Ele_pt > 35',
    3 : 'tag_Ele_pt > 35',
    4 : 'tag_Ele_pt > 35',
    5 : 'tag_Ele_pt > 35',
    6 : 'tag_Ele_pt > 35',
    7 : 'tag_Ele_pt > 35',
    8 : 'tag_Ele_pt > 35',
    9 : 'tag_Ele_pt > 35'
}

#### For now, no additional cuts 
additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.05,5.0]",
    "meanF[-0.1,-5.0,5.0]","sigmaF[0.9,0.05,5.0]",
    "acmsP[60.,30.,100.]","betaP[0.05,0.001,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,30.,80.]","betaF[0.05,0.001,0.12]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
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
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]

#############################################################
########## Systematic settings
#############################################################
# For now, no systematic variations
systematicsDef = None

#############################################################
########## Parquet-specific configuration
#############################################################
# Configuration for the histogram creation phase from Parquet files
# Parquet file pattern for standalone histogram creator
parquet_pattern = '/eos/cms/store/group/phys_egamma/Run3_commissioning/config2_EGamma_Run3_2025_C_EGamma0_synchronous/*.parquet'

parquet_config = {
    'data_input_files': '/eos/cms/store/group/phys_egamma/Run3_commissioning/config2_EGamma_Run3_2025_C_EGamma0_synchronous/',
    'mc_input_files': '/eos/cms/store/group/phys_egamma/Run3_commissioning/config2_EGamma_Run3_2018_simulation_Summer20UL18NanoAODv15_synchronous/',
    'output_dir': 'results/Run3_2025_C/tnpEleID/',
    'mass_range': [60, 120],       # Invariant mass range for TnP fits
    'n_mass_bins': 60,             # Number of mass bins in histograms
    # Note: flag_column will be determined dynamically based on working point
}

print("Configuration loaded for Run3 2025 C Parquet TnP analysis (Data + MC workflow)")
print("Base output directory:", baseOutDir)
print("Data Parquet files:", parquet_config['data_input_files'])
print("MC Parquet files:", parquet_config['mc_input_files'])
print("Available flags:", list(flags.keys()))
eta_bins = len(biningDef[0]['bins'])-1
pt_bins = len(biningDef[1]['bins'])-1
total_bins = eta_bins * pt_bins
print("Binning:", eta_bins, "eta bins x", pt_bins, "pt bins =", total_bins, "total bins")
print("Note: Using pre-computed histograms from Parquet files (no ROOT trees)")
