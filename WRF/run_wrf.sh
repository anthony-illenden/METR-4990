#!/bin/tcsh
#
#SBATCH -p normal
#SBATCH -J real
#SBATCH -N 3 
#SBATCH -n 60 
#SBATCH -t 9:00:00
#SBATCH --mail-user=anthony.illenden@ou.edu
#SBATCH --mail-type=ALL
#SBATCH -o /scratch/tonyille/wrfstuff/WRFV4/run/wrf_%j_out.txt
#SBATCH -e /scratch/tonyille/wrfstuff/WRFV4/run/wrf_%j_error.txt
#SBATCH --mem=0
#
#################################################
hostname

setenv MP_STACK_SIZE '64000000 (OMP STACKSIZE)'

source /scratch/tonyille/wrfstuff/bashrc_wrf

mpirun ./wrf.exe
