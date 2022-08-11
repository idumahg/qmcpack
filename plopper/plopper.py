import os, sys, subprocess, random, uuid

class Plopper:
    def __init__(self, num_walkers, masterfile_cpp, compilefile_cpp, masterfile_hAA, compilefile_hAA, masterfile_hAB, compilefile_hAB):

        # Initilizing global variables
        self.masterfile_cpp = masterfile_cpp
        self.compilefile_cpp = compilefile_cpp
        self.masterfile_hAA = masterfile_hAA
        self.compilefile_hAA = compilefile_hAA
        self.masterfile_hAB = masterfile_hAB
        self.compilefile_hAB = compilefile_hAB
        self.num_walkers = num_walkers

    # Creating a dictionary using parameter label and value
    def plotvalues(self, dictVal, masterfile, compilefile):
        with open(masterfile, 'r') as inputlines:
            replaced_content = ""
        
            chunksize_not_changed = True

            for line in inputlines:
                replaced = False
                for key, value in dictVal.items():
                    if key in line:
                        if key.find('thread_limit') != -1: # thread_limit
                            threadlimit = line.split('num_teams')[0].split()[-1]
                            if str(value) == '0':
                                new_line = line.replace(threadlimit + ' ', "")
                            else:
                                new_line = line.replace(threadlimit + ' ', "thread_limit" + "(" + str(value) + ") ")
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

        print("Running plotvalues")
        with open(compilefile, 'w') as f1:
            f1.write(replaced_content)

    def createDict(self, x, params):
        print("Running createDict")
        dictVal = {}
        for p, v in zip(params, x):
            dictVal[p] = v
        return(dictVal)
   
 
    def findPerformance(self, x, params):
        print("running findPerformance")    
            # Generate intermediate file
        dictVal = self.createDict(x, params)

            # Write for Sourcefile
        self.plotvalues(dictVal, self.masterfile_cpp, self.compilefile_cpp)
            # Write for headerfile1
        self.plotvalues(dictVal, self.masterfile_hAA, self.compilefile_hAA)
            # Write for headerfile2
        self.plotvalues(dictVal, self.masterfile_hAB, self.compilefile_hAB)

        #compile and find the performance  
        
    
        run_cmd = ["sh", "test_script.sh", str(dictVal['P0'])]

        try:
            execution_status = subprocess.run(run_cmd, capture_output=True, text=True)
        except ValueError:
            print("There is a Value error")

        # print('execution_status: ', execution_status.stderr)
        qmc_exetime = execution_status.stdout.split("\n")[-2]
        print('execution time: ', qmc_exetime)
        performance = float(self.num_workers)/float(qmc_exetime)
        print('performance: ', performance)
        return float(performance) #return performance 

