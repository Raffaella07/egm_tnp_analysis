
### python specific import
import argparse
import os
import sys
import pickle
import shutil
from multiprocessing import Pool
import numpy as np

# Handle numpy compatibility for older versions
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    if not hasattr(np, "bool"):
        np.bool = bool


parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--sample'     , default='all'        , help = 'create histograms (per sample, expert only)')
parser.add_argument('--altSig'     , action='store_true'  , help = 'alternate signal model fit')
parser.add_argument('--addGaus'    , action='store_true'  , help = 'add gaussian to alternate signal model failing probe')
parser.add_argument('--altBkg'     , action='store_true'  , help = 'alternate background model fit')
parser.add_argument('--doPol'     , action='store_true'  , help = 'alternate background model fit- polynomial')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--mcSig'      , action='store_true'  , help = 'fit MC nom [to init fit parama]')
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('--flag'       , default = None       , help ='WP to test')
parser.add_argument('--flag2'       , default = None       , help ='WP2 to test')
parser.add_argument('--parquet'    , action='store_true'  , help = 'use Parquet input files (faster I/O, outputs ROOT histograms for compatibility)')
parser.add_argument('settings'     , default = None       , help = 'setting file [mandatory]')


args = parser.parse_args()

print((args.flag))
print((args.flag2))


print(('===> settings %s <===' % args.settings))
import importlib
import importlib.util
import os

# Handle both relative and absolute paths for config file import
settings_path = args.settings
if not os.path.isabs(settings_path):
    # If relative path, assume it's relative to current directory
    settings_path = os.path.abspath(settings_path)

print('Loading settings from: %s' % settings_path)

# Use spec_from_file_location to import from absolute path
spec = importlib.util.spec_from_file_location("tnpConf", settings_path)
tnpConf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tnpConf)

### tnp library
import libPython.binUtils  as tnpBiner
import libPython.rootUtils as tnpRoot

# Additional ROOT configuration for FFTW plugins
try:
    import ROOT as rt
    rt.gErrorIgnoreLevel = rt.kError  # Suppress FFT plugin warnings
    print("ROOT FFT configuration completed")
except Exception as e:
    print(f"Warning: Could not configure ROOT FFT: {e}")


if args.flag is None and args.flag2 is None:
    print('[tnpEGM_fitter] flag is MANDATORY, this is the working point as defined in the settings.py')
    sys.exit(0)
    
if not args.flag in list(tnpConf.flags.keys()) and not args.flag2 in list(tnpConf.flags.keys()) :
    print(('[tnpEGM_fitter] flag %s not found in flags definitions' % args.flag))
    print('  --> define in settings first')
    print('  In settings I found flags: ')
    print((list(tnpConf.flags.keys())))
    sys.exit(1)

outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)

print('===>  Output directory: ')
print(outputDirectory)


####################################################################
##### Create (check) Bins
####################################################################
if args.checkBins:
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    for ib in range(len(tnpBins['bins'])):
        print((tnpBins['bins'][ib]['name']))
        print(('  - cut: ',tnpBins['bins'][ib]['cut']))
    sys.exit(0)
    
if args.createBins:
    if os.path.exists( outputDirectory ):
            shutil.rmtree( outputDirectory )
    os.makedirs( outputDirectory )
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    pickle.dump( tnpBins, open( '%s/bining.pkl'%(outputDirectory),'wb') )
    print(('created dir: %s ' % outputDirectory))
    print('bining created successfully... ')
    print(('Note than any additional call to createBins will overwrite directory %s' % outputDirectory))
    sys.exit(0)

tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )


####################################################################
##### Create Histograms
####################################################################
for s in list(tnpConf.samplesDef.keys()):
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'tree'     ,'%s/fitter_tree' % tnpConf.tnpTreeDir )
    setattr( sample, 'histFile' , '%s/%s_%s.root' % ( outputDirectory , sample.name, args.flag ) )

if args.createHists:

	def parallel_hists(sampleType):
		sample = tnpConf.samplesDef[sampleType]
		if sample is None:
			return
		if not (sampleType == args.sample or args.sample == 'all'):
			return

		print('creating histogram for sample ')
		sample.dump()

		var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
		if sample.mcTruth:
			var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }

		# Choose histogram backend based on --parquet flag and format detection
		if args.parquet:
			try:
				import libPython.histUtils_hybrid as tnpHist
				print("Using hybrid histogram utilities (Parquet input to  ROOT histograms)")
			except ImportError:
				print("Warning: hybrid histogram utilities not available, falling back to original")
				import libPython.histUtils as tnpHist
		else:
			import libPython.histUtils as tnpHist
		
		# Use unified interface - hybrid backend handles format detection
		tnpHist.makePassFailHistograms(
			sample,
			tnpConf.flags[args.flag],
			tnpConf.flags[args.flag2],
			tnpBins,
			var
		)

	pool = Pool()
	pool.map(parallel_hists, list(tnpConf.samplesDef.keys()))
	pool.close()
	pool.join()
	sys.exit(0)


####################################################################
##### Actual Fitter
####################################################################

# In parquet mode, we skip sample checks since histograms are pre-computed
# but we verify that the histogram files exist
if not args.parquet:
    sampleToFit = tnpConf.samplesDef['data']
    if sampleToFit is None:
        print('[tnpEGM_fitter, prelim checks]: sample (data or MC) not available... check your settings')
        sys.exit(1)

    sampleMC = tnpConf.samplesDef['mcNom']

    if sampleMC is None:
        print('[tnpEGM_fitter, prelim checks]: MC sample not available... check your settings')
        sys.exit(1)
        
    for s in list(tnpConf.samplesDef.keys()):
        sample =  tnpConf.samplesDef[s]
        if sample is None: continue
        setattr( sample, 'mcRef'     , sampleMC )
        setattr( sample, 'nominalFit', '%s/%s_%s.nominalFit.root' % ( outputDirectory , sample.name, args.flag ) )
        setattr( sample, 'altSigFit' , '%s/%s_%s.altSigFit.root'  % ( outputDirectory , sample.name, args.flag ) )
else:
    # Parquet mode: Check that pre-computed histogram files exist
    print('[tnpEGM_fitter]: Running in Parquet mode - checking for pre-computed histograms...')
    
    # Check data histogram file
    data_hist_file = '%s/data_Run3_2025_C_%s.root' % (outputDirectory, args.flag)
    if not os.path.exists(data_hist_file):
        print('[tnpEGM_fitter, prelim checks]: Data histogram file not found: %s' % data_hist_file)
        print('  --> Run histogram creation phase first')
        sys.exit(1)
    else:
        print('  ✓ Data histograms found: %s' % data_hist_file)
    
    # Check MC histogram file  
    mc_hist_file = '%s/mc_Run3_2025_C_%s.root' % (outputDirectory, args.flag)
    if not os.path.exists(mc_hist_file):
        print('[tnpEGM_fitter, prelim checks]: MC histogram file not found: %s' % mc_hist_file)
        print('  --> Run histogram creation phase first')
        sys.exit(1)
    else:
        print('  ✓ MC histograms found: %s' % mc_hist_file)
    
    print('[tnpEGM_fitter]: All histogram files ready for fitting!')

# For parquet mode, create minimal sample objects pointing to histogram files
if args.parquet:
    from libPython.tnpClassUtils import tnpSample
    
    # Create data sample pointing to existing histogram file
    # Use dummy paths since histograms are pre-computed
    sampleToFit = tnpSample('data', 'dummy_data_path.root', lumi=1.0)
    sampleToFit.histFile = '%s/data_Run3_2025_C_%s.root' % (outputDirectory, args.flag)
    sampleToFit.nominalFit = '%s/data_%s.nominalFit.root' % (outputDirectory, args.flag)
    sampleToFit.altSigFit = '%s/data_%s.altSigFit.root' % (outputDirectory, args.flag)
    sampleToFit.altBkgFit = '%s/data_%s.altBkgFit.root' % (outputDirectory, args.flag)
    
    # Create MC sample
    sampleMC = tnpSample('mcNom', 'dummy_mc_path.root', lumi=1.0, isMC=True)
    sampleMC.histFile = '%s/mc_Run3_2025_C_%s.root' % (outputDirectory, args.flag)
    sampleMC.nominalFit = '%s/mc_%s.nominalFit.root' % (outputDirectory, args.flag)
    sampleMC.altSigFit = '%s/mc_%s.altSigFit.root' % (outputDirectory, args.flag)
    sampleMC.altBkgFit = '%s/mc_%s.altBkgFit.root' % (outputDirectory, args.flag)
    
    # Set references
    sampleToFit.mcRef = sampleMC



### change the sample to fit is mc fit
if args.mcSig :
    sampleToFit = sampleMC#tnpConf.samplesDef['mcNom']
    sampleToFit.mcRef = sampleMC#tnpConf.samplesDef['mcNom']

if  args.doFit:
#    sampleToFit.dump()
    def parallel_fit(ib):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            if args.altSig and not args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
            elif args.altSig and args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit_addGaus, 1)
            elif args.altBkg:
                # Use standard alternative background fit (no polynomial distinction for now)
                tnpRoot.histFitterAltBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
            else:
                tnpRoot.histFitterNominal( sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParNomFit )
    pool = Pool()
    pool.map(parallel_fit, list(range(len(tnpBins['bins']))))
    #parallel_fit(range(len(tnpBins['bins']))[0])
    args.doPlot = True
     
####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    fileName = sampleToFit.nominalFit
    fitType  = 'nominalFit'
    if args.altSig : 
        fileName = sampleToFit.altSigFit
        fitType  = 'altSigFit'
    if args.altBkg : 
        fileName = sampleToFit.altBkgFit
        fitType  = 'altBkgFit'
        
    os.system('hadd -f %s %s' % (fileName, fileName.replace('.root', '-*.root')))

    plottingDir = '%s/plots/%s/%s' % (outputDirectory,sampleToFit.name,fitType)
    if not os.path.exists( plottingDir ):
        os.makedirs( plottingDir )
    shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)

    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            tnpRoot.histPlotter( fileName, tnpBins['bins'][ib], plottingDir )

    print(' ===> Plots saved in <=======')
#    print 'localhost/%s/' % plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:
    if args.parquet:
        # Parquet mode: construct info dict for pre-computed histograms
        from libPython.tnpClassUtils import tnpSample
        
        # Create minimal sampleToFit object for parquet mode
        sampleToFit = tnpSample('data', 'dummy_data_path.root', lumi=1.0)
        sampleToFit.histFile = '%s/data_Run3_2025_C_%s.root' % (outputDirectory, args.flag)
        
        # Check if alternative fit files exist before adding to info dict
        altSigFile = '%s/data_%s.altSigFit.root' % (outputDirectory, args.flag)
        altBkgFile = '%s/data_%s.altBkgFit.root' % (outputDirectory, args.flag)
        
        # For parquet mode, use fit files if they exist, otherwise fallback to histograms
        info = {
            'data'           : '%s/data_Run3_2025_C_%s.root' % (outputDirectory, args.flag),
            'dataNominal'    : '%s/data_%s.nominalFit.root' % (outputDirectory, args.flag),
            'dataAltSig'     : altSigFile if os.path.exists(altSigFile) else None,
            'dataAltBkg'     : altBkgFile if os.path.exists(altBkgFile) else None,
            'dataAltSigBkg'  : None,  # Not implemented for parquet mode yet
            'mcNominal'      : '%s/mc_Run3_2025_C_%s.root' % (outputDirectory, args.flag),
            'mcAlt'          : None,
            'tagSel'         : None
        }
    else:
        # Standard mode: use sample objects
        sampleToFit.dump()
        info = {
            'data'        : sampleToFit.histFile,
            'dataNominal' : sampleToFit.nominalFit,
            'dataAltSig'  : sampleToFit.altSigFit ,
            'dataAltBkg'  : sampleToFit.altBkgFit ,
            'dataAltSigBkg': None,  # Add missing key
            'mcNominal'   : sampleToFit.mcRef.histFile,
            'mcAlt'       : None,
            'tagSel'      : None
            }

    #if not tnpConf.samplesDef['mcAlt' ] is None:
    #    info['mcAlt'    ] = tnpConf.samplesDef['mcAlt' ].histFile
    #if not tnpConf.samplesDef['tagSel'] is None:
     #   info['tagSel'   ] = tnpConf.samplesDef['tagSel'].histFile

    effis = None
    effFileName ='%s/egammaEffi.txt' % outputDirectory 
    fOut = open( effFileName,'w')
    
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )

        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            print(astr)
            fOut.write( astr + '\n' )
            astr = '### var2 : %s' % v2Range[1]
            print(astr)
            fOut.write( astr + '\n' )
            
        astr =  '%+8.5f\t%+8.5f\t%+8.5f\t%+8.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            effis['dataNominal'][0],effis['dataNominal'][1],
            effis['mcNominal'  ][0],effis['mcNominal'  ][1],
            effis['dataAltBkg' ][0],
            effis['dataAltSig' ][0],
            effis['mcAlt' ][0],
            effis['tagSel'][0],
            )
        print(astr)
        fOut.write( astr + '\n' )
    fOut.close()

    print(('Effis saved in file : ',  effFileName))
    import libPython.EGammaID_scaleFactors as egm_sf
    egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi)

# Print status summary
print("\n=== TnP Analysis Complete ===")
if args.parquet:
    print("Used Parquet mode: fast input reading with ROOT histogram output")
    print("Histogram creation: Parquet to ROOT (hybrid)")
    print("Fitting/plotting: Standard ROOT workflow")
else:
    print("Used standard ROOT mode: traditional workflow")
    print("All operations used ROOT files")
print(" Results ready for downstream analysis")
