import subprocess
import shutil

def plotvalues(dictVal, masterfile, compilefile):
    with open(masterfile, 'r') as inputlines:
        replaced_content = ""
        
        chunksize_not_changed = True

        for line in inputlines:
            replaced = False
            for key, value in dictVal.items():
                if key in line:
                    if key.find('thread_limit') != -1: # thread_limit
                        threadlimit = line.split('num_teams')[0].split()[-1]
                        new_line = line.replace(threadlimit + ' ', str(value))
                        replaced_content += new_line
                        replaced = True
                    if key.find('chunksize') != -1 and chunksize_not_changed: # ChunksizePerTeam
                        new_list = line.split()
                        new_list[-1] = str(value)
                        new_line = ' '.join(new_list)
                        replaced_content += new_line + '\n'
                        chunksize_not_changed = False
                        replaced = True

            if not replaced:
                replaced_content += line
                replaced = False

    with open(compilefile, 'w') as f1:
        f1.write(replaced_content)

def createDict(x, params):
    dictVal = {}
    for p, v in zip(params, x):
        dictVal[p] = v
    return(dictVal)
   

    # Function to find the performance of the interim file, and return the rate cost to the search module
def findPerformance(x, params):    
        # Generate intermediate file
    dictVal = createDict(x, params)

        # Write for Sourcefile
    plotvalues(dictVal, masterfile_cpp, compilefile_cpp)
        # Write for headerfile1
    plotvalues(dictVal, masterfile_hAA, compilefile_hAA)
        # Write for headerfile2
    plotvalues(dictVal, masterfile_hAB, compilefile_hAB)

        #compile and find the performance  
        
    
    run_cmd = ["sh", "test_script.sh", str(dictVal['P0'])]

    try:
        execution_status = subprocess.run(run_cmd, capture_output=True, text=True)
    except ValueError:
        print("There is a Value error")

        # print('execution_status: ', execution_status.stderr)
    qmc_exetime = execution_status.stdout.split("\n")[-2]
    print('execution time: ', qmc_exetime)
    performance = float(50)/float(qmc_exetime)
    print('performance: ', performance)
    return float(performance) #return performance 
 
#if __name__=="main":
#dictVal = {'P0':1000, 'P1':20, 'thread_limit':'', 'chunksize':700}
masterfile_cpp = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/QMCWaveFunctions/BsplineFactory/SplineC2ROMPTarget_master.cpp'
compilefile_cpp = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/QMCWaveFunctions/BsplineFactory/SplineC2ROMPTarget.cpp'
masterfile_hAA = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableAAOMPTarget_master.h'
compilefile_hAA = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableAAOMPTarget.h'
masterfile_hAB = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableABOMPTarget_master.h'
compilefile_hAB = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableABOMPTarget.h'

ans = findPerformance(['8', '', '', '', '512', '512', '512'], ['P0', 'thread_limit_cpp', 'thread_limit_hAA', 'thread_limit_hAB', 'chunksize_cpp', 'chunksize_hAA', 'chunksize_hAB'])
print(ans)
