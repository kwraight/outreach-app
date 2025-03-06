### simple pixel charge deposition simulation
import numpy as np
import math
import random


def IntegrateGaussianFrac( A, Bx, Cx, xlo=-1.0, xhi=-1.0 ):

    z=-1.0
    if(xlo<xhi):
        z=(math.erf((xhi - Bx)/(math.sqrt(2.)*Cx)) - math.erf((xlo - Bx)/(math.sqrt(2.)*Cx)));
        #z = z * (-math.erf((y1 - By)/(math.sqrt(2.)*Cy)) + math.erf((y0 - By)/(math.sqrt(2.)*Cy)));
        z = z * A * 1/2.0

    #print "Gaus: ",A,", ",Bx,", ",Cx,", ",By,", ",Cy
    #print "\nlimits: ",xlo,"->",xhi
    #print "\n alt: ",z

    return z


def ModeResult(val, THL, mode="mpx"):
    if "tpx" in mode or "TPX" in mode:
        if val>THL: return val
        else: return 0
    else:
        if val>THL: return 1
        else: return 0
    print("### ERROR ### ModeResult: nothing happened")
    return


def RunPixSim(*, npx, px_idx, cs, bw, mode, thl):

    # px_idx is zero based pixel index
    pixDim=[55.0*px_idx,55.0*(px_idx+1)]
    THL=10.0

    stepSize=1.0
    startPoint=0.0
    endPoint=55.0*npx

    energy=1000.0

    points=np.arange(startPoint,endPoint,stepSize)
    depTHLs=[]
    scanShares=np.arange(0.0,cs*5*abs(pixDim[0]-pixDim[1]),cs)
    scanWidths=np.arange(0.0,bw*5*abs(pixDim[0]-pixDim[1]),bw)
    scanTHLs=np.arange(energy/5,energy,energy/5)

    #depSimple= GetSimplePoints(points,pixDim,energy)

    #depShare= GetSharePoints(points,pixDim,energy,mode,cs*abs(pixDim[0]-pixDim[1]))

    #depBeam= GetBeamPoints(points,pixDim,energy,mode,bw*abs(pixDim[0]-pixDim[1]))

    #depComb= GetCombPoints(points,pixDim,energy,mode,cs*abs(pixDim[0]-pixDim[1]),bw*abs(pixDim[0]-pixDim[1]))

    depTHL= GetTHLPoints(points,pixDim,energy,mode,cs*abs(pixDim[0]-pixDim[1]),bw*abs(pixDim[0]-pixDim[1]),thl*energy)

    return depTHL


def GetSimplePoints(points, pixDim, energy):
    # charge deposition without beam or sharing effects
    depPoints=[]
    for p in points:
        dep=0.0
        if p>=pixDim[0] and p<pixDim[1]:
           dep=energy
        depPoints.append(dep)
    return depPoints


def GetSharePoints(points, pixDim, energy, mode, sharing):
    # charge deposition with sharing effects only
    depPoints=[]
    for p in points:
        dep=0.0
        dep = IntegrateGaussianFrac(energy, p, sharing, pixDim[0], pixDim[1])
        depForMode=ModeResult(dep,0.1,mode) # negligible THL
        depPoints.append(depForMode)
    return depPoints


def GetBeamPoints(points, pixDim, energy, mode, beamWidth):
    # charge deposition with beam effects only
    depPoints=[]
    for p in points:
        depForMode=0.0
        for i in range(0,1000,1):
            p_spread= random.gauss(p, beamWidth)
            dep = IntegrateGaussianFrac(energy, p_spread, 0.001, pixDim[0], pixDim[1]) # negligible charge sharing
            depForMode+=ModeResult(dep,0.1,mode) # negligible THL
        depPoints.append(depForMode)#/1000.0)
    return depPoints


def GetCombPoints(points, pixDim, energy, mode, sharing, beamWidth):
    # charge deposition with beam and sharing effects
    depPoints=[]
    for p in points:
        depForMode=0.0
        for i in range(0,1000,1):
            p_spread= random.gauss(p, beamWidth)
            dep = IntegrateGaussianFrac(energy, p_spread, sharing, pixDim[0], pixDim[1])
            depForMode+=ModeResult(dep,0.1,mode) # negligible THL
        depPoints.append(depForMode)#/1000.0)
    return depPoints


def GetTHLPoints(points, pixDim, energy, mode, sharing, beamWidth, thl):
    # charge deposition with beam and sharing effects
    depPoints=[]
    for p in points:
        depForMode=0.0
        for i in range(0,1000,1):
            p_spread= random.gauss(p, beamWidth)
            dep = IntegrateGaussianFrac(energy, p_spread, sharing, pixDim[0], pixDim[1])
            depForMode+=ModeResult(dep,thl,mode) # negligible THL
        depPoints.append(depForMode)#/1000.0)
    return depPoints







# #print depTHLs
# plt.figure("pixel scan simulation")
#
# #ideal pixel
# plt.subplot(221)
# plt.plot(points, [d[0] for d in depShares], lw=2, label="ideal")
# plt.grid(True)
# plt.legend()
# plt.title(r"Ideal 55$\mu m$ pixel")
#
#
# '''
# plt.plot([pixDim[0], pixDim[0]], [0, max([max(d) for d in depBeams])], 'k--', lw=2)
# plt.plot([pixDim[1], pixDim[1]], [0, max([max(d) for d in depBeams])], 'k--', lw=2)
# plt.rc('axes', prop_cycle=(cycler('color', ['k', 'r', 'g', 'b', 'm'])))
# for t in range(0,len(depShares[0]),1):
#     plt.plot(points, [d[t] for d in depShares], lw=2, label=str(scanShares[t]))
# plt.grid(True)
# plt.legend()
# plt.show()
# '''
#
# #beam only
# plt.subplot(222)
# plt.plot([pixDim[0], pixDim[0]], [0, max([max(d) for d in depBeams])], 'k--', lw=2)
# plt.plot([pixDim[1], pixDim[1]], [0, max([max(d) for d in depBeams])], 'k--', lw=2)
# plt.rc('axes', prop_cycle=(cycler('color', ['k', 'r', 'g', 'b', 'm'])))
# for t in range(0,len(depBeams[0]),1):
#     plt.plot(points, [d[t] for d in depBeams], lw=2, label=r"$\sigma$="+str(scanWidths[t]))
# plt.grid(True)
# plt.legend()
# plt.title("Beam width only")
#
#
# #beam and charge sharing
# plt.subplot(223)
# plt.plot([pixDim[0], pixDim[0]], [0, max([max(d) for d in depBeamShares])], 'k--', lw=2)
# plt.plot([pixDim[1], pixDim[1]], [0, max([max(d) for d in depBeamShares])], 'k--', lw=2)
# plt.rc('axes', prop_cycle=(cycler('color', ['k', 'r', 'g', 'b', 'm'])))
# for t in range(0,len(depBeamShares[0]),1):
#     plt.plot(points, [d[t] for d in depBeamShares], lw=2, label=r"$\sigma$="+str(scanWidths[t]))
# plt.grid(True)
# plt.legend()
# plt.title(r"Beam width with charge sharing ($\sigma_{cs}$ = 2$\mu m$)")
#
#
# #THL comparison
# plt.subplot(224)
# plt.plot([pixDim[0], pixDim[0]], [0, max([max(d) for d in depTHLs])], 'k--', lw=2)
# plt.plot([pixDim[1], pixDim[1]], [0, max([max(d) for d in depTHLs])], 'k--', lw=2)
# plt.rc('axes', prop_cycle=(cycler('color', ['k', 'r', 'g', 'b', 'm'])))
# for t in range(0,len(depTHLs[0]),1):
#     plt.plot(points, [d[t] for d in depTHLs], lw=2, label=str(scanTHLs[t]))
# plt.grid(True)
# plt.legend()
# plt.title(r"THL effects ($\sigma_{beam}$ = 2.5$\mu m$, $\sigma_{cs}$ = 5$\mu m$)")
# plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95, hspace=0.40, wspace=0.409)
# plt.show()
#
