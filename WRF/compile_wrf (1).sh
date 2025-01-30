#!/bin/tcsh
#
#SBATCH -p normal
#SBATCH -J WRF_compile
#SBATCH -n 1 
#SBATCH -t 75
#SBATCH --mail-user=chomeyer@ou.edu
#SBATCH --mail-type=ALL
#SBATCH -o /home/chomeyer/compile_%j_out.txt
#SBATCH -e /home/chomeyer/compile_%j_error.txt
#SBATCH --mem=1024
#SBATCH --chdir=/home/chomeyer/WRFV4
#
#################################################
hostname

module load JasPer/1.900.1-intel-2016a
module load netCDF-Fortran/4.4.4-intel-2016a
setenv NETCDF '/opt/oscer/software/netCDF-Fortran/4.4.4-intel-2016a'
setenv WRFIO_NCD_LARGE_FILE_SUPPORT '1'
setenv WRF_EM_CORE '1'

./compile em_real
