import os
import sys

config = sys.argv[1]
pwd = "/afs/cern.ch/work/r/ratramon/EGamma/CMSSW_11_2_0/src/egm_tnp_analysis"
tag = config.split("/")[-1].strip(".py")
print tag

flags_Run3 = ["passingCutBasedLoose122XV1","passingCutBasedMedium122XV1","passingCutBasedTight122XV1","passingMVA122XV1wp80","passingMVA122XV1wp90"]

command = "python tnpEGM_fitter.py" 

options = [ " --flag pippo --flag2 pluto --checkBins",
            " --flag pippo --flag2 pluto --createBins",
            " --flag pippo --flag2 pluto --createHists",
            " --flag pippo --doFit",
            " --flag pippo --doFit --altBkg",
            " --flag pippo --doFit --altSig --mcSig",
            " --flag pippo --doFit --altSig",
            " --flag pippo --sumUp" 
            ]



for flag in flags_Run3:

    script_name =pwd+"/launchers/"+tag+"_"+flag+".sh" 

    with open(script_name, 'w') as file:
        script_content = "eval `scram runtime -sh` \n"
        for option in options:
            if "pippo" in option:
                option = option.replace("pippo",flag)
            if "pluto" in option:
                option = option.replace("pluto",flag)
            if "altBkg" not in option:
                script_content = script_content + command + " " + config + option + "\n"
            else:
                for i in range(0,50):
                    if i in range(10,20):

                        script_content = script_content + command + " " + config + option + " --iBin " +str(i) + " --doPol \n"
                    else: 
                        script_content = script_content +command + " " + config + option + " --iBin " +str(i) + " \n" 

        file.write(script_content)
        # Make the script executable
        os.chmod(script_name, 0o755)
