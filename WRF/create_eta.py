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
fdir='/scratch/w40/sh1269/WRFV4.2/20101207/run_ERA5/run/'

#read in data from a file...
fname='wrfout_d01_2010-12-06_00:00:00'
fpath=fdir+fname
data=xr.open_dataset(fpath)
eta=data.ZNU.squeeze()

#this bit does a quick plot of z dz to get average domain wide vertical grid spacing
alt=(data.PHB+data.PH)/g  #ph is geopotential
alt=alt.squeeze()
meanalt=alt.mean(dim='south_north').mean(dim='west_east')
dz=np.insert(np.diff(meanalt),0,0)

plt.figure()
plt.plot(dz,meanalt)
plt.ylabel(r'$\bar{z}$')
plt.xlabel(r'$d\bar{z}$')
plt.savefig('zbydz.png')

#now try and back out appropriate eta values for desired grid spacing
#use a log function to get ideal spacing
dz_bot=50. #for stretched
dz_top=200. # for unstretched
ztop=20200.
str_bot=0.
str_top=3000.

#from cm1
#nominal_dz=.5*(dz_bot+dz_top) #grid spacing at stretch midpoint?u

nk=(str_bot/dz_bot)+(ztop-str_top)/dz_top + (str_top-str_bot)/(.5*(dz_bot+dz_top))

nk1=int(str_bot/dz_bot) #num levels below stretch
nk3=int((ztop-str_top)/dz_top) #num levles above stretch
nk2=int(nk-(nk1+nk3)) #num stretch levs

#find C1 and C2 using first point and midpoint? this code is from CM1
nominal_dz=(str_top-str_bot)/nk2
C2=(nominal_dz-dz_bot)/(nominal_dz*nominal_dz*float(nk2-1))
C1=(dz_bot/nominal_dz)-C2*nominal_dz


#find C1 and C2 using known levels (1 and str_top) #SMH Version doesn't work here...
#lev1=str_bot+dz_bot
#C2=(-1/((dz_bot**2)*(1+strlevs)))*((str_top/strlevs-lev1))
#C1=lev1/dz_bot -dz_bot*C2
#C1check=str_top/(strlevs*dz_bot)-(strlevs*dz_bot)*C2

zprime=np.zeros(shape=int(nk))
#create zprime array
for kk in range(0,nk1+1):
    #print(kk)
    zprime[kk-1]=kk*dz_bot

for kk in range(nk1+1,nk1+nk2+2):
    #print(kk)
    zprime[kk-1]=zprime[nk1+1]+(C1+C2*float(kk-1-nk1)*nominal_dz)*float(kk-1-nk1)*nominal_dz

for kk in range((nk1+nk2+1),(nk1+nk2+nk3+1)):
    #print(kk)
    zprime[kk-1]=zprime[kk-2]+dz_top


#get needed  virtual temp and pressure data for hypsometric below
Tsfc=data.T2
Qvsfc=data.Q2
Tvsfc=_Tv(Tsfc,Qvsfc)
Tvs_mean=Tvsfc.squeeze().mean(dim='south_north').mean(dim='west_east').values
TH=data.T+300.

#get needed pressure data
P0=data.PB #pa
P=data.P+P0 #pa
P=P.squeeze()

Psfc=data.PSFC #pa

Ps_mean=Psfc.squeeze().mean(dim='south_north').mean(dim='west_east').values
Pcolumn_mean=P.squeeze().mean(dim='south_north').mean(dim='west_east').values
Pt_mean=Pcolumn_mean[-1]

#convert to temperature before averaging and interpolation
Tk=_th2Tk(TH,P/100.)

#convert to Tv first too...
qv=data.QVAPOR.squeeze() #kg/kg

Tvk=_Tv(Tk,qv)

Tvkcolumn_mean=Tvk.mean(dim='south_north').mean(dim='west_east').values
Tvkcolumn_mean=np.insert(Tvkcolumn_mean,0,Tvs_mean)

#interpolation
f=interpolate.interp1d(meanalt,Tvkcolumn_mean,fill_value='extrapolate') #interpolation function
Tvknew=f(zprime)

#check interp
plt.figure()
plt.plot(Tvkcolumn_mean,meanalt)
plt.plot(Tvknew,zprime)
plt.savefig('Tvinterptest.png')
plt.close()


#use hypsometric to back out pressures associated with desired dz
dzprime=np.diff(zprime)

newP=np.zeros(shape=zprime.shape)
newP[0]=Ps_mean
for ii in range(0,len(zprime)-1):
    newP[ii+1]=newP[ii]*np.exp((-dzprime[ii]*g)/(Rd*Tvknew[ii]))

#check interp
plt.figure()
plt.plot(np.insert(Pcolumn_mean/100,0,Ps_mean/100),meanalt)
plt.plot(newP/100,zprime)
plt.savefig('Pinterptest.png')
plt.close()

#plug that into formula for eta... this won't be exactly right, but close (P-Ptop)/(Psfc-Ptop)
eta=(newP-newP[-1])/(newP[0]-newP[-1])




