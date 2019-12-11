#!/bin/bash

#SBATCH -N 1        # number of nodes

#SBATCH -n 4   # number of cores

#SBATCH -p shared   # partition to submit to

#SBATCH --mem=16000  # memory per node in MB (see also --mem-per-cpu)

#SBATCH -t 60 # expected runtime in minutes

#SBATCH -J keras_@NUM  # name of this job

#### adapted from Eugene Kwan Gaussian submission script (ekwan.github.io)

mkdir results/model_@NUM
out=results/model_@NUM/results.txt

echo "*************************************" > $out 
echo "Running on host:" >> $out
hostname >> $out
echo "Job @JOBNAME started at..." >> $out
date >> $out

python run_model_ccw.py --config best_china_model_@NUM.json >> $out

echo "Job @JOBNAME finished at..." >> $out
date >> $out

