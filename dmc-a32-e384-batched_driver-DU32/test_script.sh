#!/bin/bash

# Set the number of OpenMP threads from Plopper
export OMP_NUM_THREADS=$1 

SupercellSize=8

file_prefix=NiO-fcc-S$SupercellSize-dmc

module use /soft/modulefiles
module load cmake/3.22.1
module load public_mkl
module use /soft/packaging/spack-builds/modules/linux-opensuse_leap15-x86_64
module load hdf5
module load llvm/master-latest
module load boost/1.74.0-gcc-10.2.0-lwc57tn

#cmake -DQMC_MPI=off -DQMC_DATA=data_folder -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -D ENABLE_OFFLOAD=ON -D USE_OBJECT_TARGET=ON -D ENABLE_CUDA=ON -D CMAKE_CUDA_ARCHITECTURES=80 ..

cd ~/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/build

make -j 8 qmcpack

cd -
exe=~/ytopt/ytopt/ytopt/benchmark/qmcpack/qmcpack-3.14.0/build/bin/qmcpack

# replace marker, but not in-place
# sed 's/P0/'$2'/g' $file_prefix.xml > $file_prefix'_tmp'.xml

# execute qmcpack
$exe $file_prefix.xml > $file_prefix.out

output=$(awk '/QMC Execution time/ {print $5}' $file_prefix.out | tail -1)

echo $output


