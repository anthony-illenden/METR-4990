#!/bin/tcsh
#
#SBATCH -p normal
#SBATCH -J WRF_compile
#SBATCH -n 1 
#SBATCH -t 75
#SBATCH --mail-user=stacey.hitchcock@ou.edu
#SBATCH --mail-type=ALL
#SBATCH -o /home/sh1269/compileWRF/WPS/compile_%j_out.txt
#SBATCH -e /home/sh1269/compileWRF/WPS/compile_%j_error.txt
#SBATCH --mem=1024
#SBATCH --chdir=/home/sh1269/compileWRF/WPS
#
#################################################
hostname

source /home/sh1269/compileWRF/bashrc_wrf

./compile 
