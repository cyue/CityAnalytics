#!/bin/bash

# Name: Cong Yue
# Surname: Yue
# Student Id: 682020

#SBATCH --job-name=1node-8core
#SBATCH -p cloud
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1

module load Python/3.4.3-goolf-2015a 
srun process.py $1

