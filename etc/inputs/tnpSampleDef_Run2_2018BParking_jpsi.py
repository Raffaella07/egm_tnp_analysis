from libPython.tnpClassUtils import tnpSample
import os

### samples
eosTnp = '/eos/cms/store/user/crovelli/LowPtEle/TnpData/March21noRegression/'

Parking_Jan16 = {
    'BuToKJpsi'          : tnpSample('BuToKJpsi',
                                    # eosTnp + 'Formatted_TnP_March21_BuToKJpsiToeeV2_PUweightsRunAll__probeLowPt.root',
                                     eosTnp + 'Formatted_March21_NoRegr_BuToKJpsi_Toee_v2_probePF__withPuWeights.root',
                                     isMC = True, nEvts =  -1 ),

    'data_Run2018ALL' : tnpSample('data_Run2018ALL' , os.getcwd() + '/etc/inputs/Formatted_March21_NoRegr_Parking2018ALL_probePF.root' , lumi = 41.6), 
    }

