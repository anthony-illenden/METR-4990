import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def _th2Tk(TH,P):
    #TH in K, P in hpa
    Tk=TH*(P/1000.)**(Rd/Cp)
    return Tk

def _theta_rho(T,P,rv,rl,ri):
    #T in K, P in hPa,rs in kg/kg
    theta_rho=_theta(T,P)*(1.+.61*rv-rl-ri)
    return theta_rho

def _Tv(Tk,rv):
    ####################################################################
    #Returns virtual temperature (K) using T in K and mixing ratio rv(kg/kg)
    #Based on Rodgers and Yau 2.21
    ####################################################################
    Tv=Tk*((1.+(rv/eps))/(1.+rv))
    return Tv


#constants
Rd=287.047 #J/kgk
Rv=461.5 #J/kgk
g=9.81
Cp=1005. #J/kgk
eps=Rd/Rv

#directory info
fdir='/g/data/w40/sh1269/WRF/20130718/MYNN_Th2M/traj/'

#read in data from a file...
#fname='wrfout_d01_2010-12-06_00:00:00'
#fname='wrfout_d02_2010-12-06_01:30:00'
fname='wrfout_d01_2013-07-18_00:00:00'
fpath=fdir+fname
data=xr.open_dataset(fpath)
eta=data.ZNU.squeeze()

#this bit does a quick plot of z dz to get average domain wide vertical grid spacing
alt=(data.PHB+data.PH)/g  #ph is geopotential
alt=alt.squeeze()
Press=data.P+data.PB
Press=Press.squeeze()
meanalt=alt.mean(dim='south_north').mean(dim='west_east')
dz=np.insert(np.diff(meanalt),0,0)

plt.figure()
plt.plot(dz,meanalt)
plt.ylabel(r'$\bar{z}$')
plt.xlabel(r'$d\bar{z}$')
plt.savefig('zbydz_new.png')



