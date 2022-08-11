import numpy as np
from autotune import TuningProblem
from autotune.space import *
import os, sys, time, json, math
import ConfigSpace as CS
import ConfigSpace.hyperparameters as CSH
from skopt.space import Real, Integer, Categorical

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.dirname(HERE)+ '/plopper')
from plopper import Plopper

# create an object of ConfigSpace
cs = CS.ConfigurationSpace(seed=1234)
# walkers per rank
# p0= CSH.UniformIntegerHyperparameter(name='p0', lower=500, upper=5000, default_value=500)
# number of threads
p0= CSH.UniformIntegerHyperparameter(name='p0', lower=1, upper=64, default_value=8)
# threads_limit source file
p1 = CSH.OrdinalHyperparameter(name='p1', sequence=['0', '64', '128', '192', '256'], default_value='0')
# threads_limit header file AAOMPTarget
p2 = CSH.OrdinalHyperparameter(name='p2', sequence=['0', '64', '128', '192', '256'], default_value='0')
# threads_limit header file ABOMPTarget
p3 = CSH.OrdinalHyperparameter(name='p3', sequence=['0', '64', '128 ', '192', '256'], default_value='0')
# chuck_size_per_team source file
p4 = CSH.OrdinalHyperparameter(name='p4', sequence=['128', '192', '256', '384', '512', '768', '1024'], default_value="512")
# chuck_size_per_team header file AAOMPTarget
p5 = CSH.OrdinalHyperparameter(name='p5', sequence=['128', '192', '256', '384', '512', '768', '1024'], default_value="512")
# chuck_size_per_team file ABOMPTarget
p6 = CSH.OrdinalHyperparameter(name='p6', sequence=['128', '192', '256', '384', '512', '768', '1024'], default_value="512")
cs.add_hyperparameters([p0, p1, p2, p3, p4, p5, p6])

# problem space
task_space = None
input_space = cs
output_space = Space([
     Real(0.0, 6000000, name="performance")
])

dir_path = os.path.dirname(os.path.realpath(__file__))
masterfile_cpp = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/QMCWaveFunctions/BsplineFactory/SplineC2ROMPTarget_master.cpp'
compilefile_cpp = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/QMCWaveFunctions/BsplineFactory/SplineC2ROMPTarget.cpp'
masterfile_hAA = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableAAOMPTarget_master.h'
compilefile_hAA = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableAAOMPTarget.h'
masterfile_hAB = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableABOMPTarget_master.h'
compilefile_hAB = '/home/gidumah/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/src/Particle/SoaDistanceTableABOMPTarget.h'
num_walkers = 400

obj = Plopper(num_walkers, masterfile_cpp, compilefile_cpp, masterfile_hAA, compilefile_hAA, masterfile_hAB, compilefile_hAB)

x1=['p0','p1','p2','p3','p4','p5','p6']
def myobj(point: dict):
    def plopper_func(x):
        x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
        value = [point[x1[0]],point[x1[1]],point[x1[2]],point[x1[3]],point[x1[4]],point[x1[5]],point[x1[6]]]
        print('CONFIG:',point)
        params = ['P0', 'thread_limit_cpp', 'thread_limit_hAA', 'thread_limit_hAB', 'chunksize_cpp', 'chunksize_hAA', 'chunksize_hAB']
        result = obj.findPerformance(value, params)
        return result

    x = np.array([point[f'p{i}'] for i in range(len(point))])
    results = plopper_func(x)
    print('OUTPUT:%f',results)
    return -results

Problem = TuningProblem(
    task_space=None,
    input_space=input_space,
    output_space=output_space,
    objective=myobj,
    constraints=None,
    model=None
    )
