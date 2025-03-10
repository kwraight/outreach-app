import streamlit as st
from core.Page import Page
### custom
import pandas as pd
import json
from measurement.measures import Weight, Volume
### general
import os
import sys
import re
import datetime
### other
# cwd = os.getcwd()
# sys.path.insert(0, cwd+"/code")
from .simCode.pixelSim import RunPixSim

#####################
### useful functions
#####################
### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))

def RunSimulation(pageDict):
    settings={'numPix':pageDict['numPix'],'chargeSharing':pageDict['chargeSharing'],'beamWidth':pageDict['beamWidth'],'chipMode':pageDict['chipMode'],'threshold':pageDict['threshold']}
    simResults=[]
    for px in range(0,pageDict['numPix'],1):
        simResults.append(RunPixSim(npx=pageDict['numPix'], px_idx=px, cs=pageDict['chargeSharing'], bw=pageDict['beamWidth'], mode=pageDict['chipMode'], thl=pageDict['threshold']))
    
    if "simResults" not in pageDict.keys():
        pageDict['simResults']=[{'name':pageDict['name'],'pix_data':simResults,'settings':settings}]
    else:
        pageDict['simResults'].append({'name':pageDict['name'],'pix_data':simResults,'settings':settings})
    
    return "Simulation complete: "+DateFormat(datetime.datetime.now())


infoList=["### Instructions",
        "  * set number of pixels",
        "  * set relative beam widt",
        "  * set relative charge sharing",
        "  * set relative THL",
        "  * set chip mode"]
#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Setup", "🛠 Select Simulation Parameters", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]


        # debug check
        if st.session_state.debug:
            st.error("Debug is on")
            [st.write(x) for x in infoList]

        st.write("## Standards")
        st.write("All sizes relative to pixel length: 1 unit")

        # Number of pixels
        st.write("## Select number of Pixels")
        numPix=st.slider("Number of pixels", min_value=1, max_value=5, value=3, step=1)

        ## select beam width
        st.write("## Beam sigma (relative to pixel width)")
        beamWidth=st.slider("Width of beam", min_value=0.01, max_value=1.0, value=0.09, step=0.01)

        ## select charge sharing
        st.write("## Charge sharing (relative to pixel width)")
        chargeSharing=st.slider("Charge sharing", min_value=0.01, max_value=1.0, value=0.18, step=0.01)

        ## select threshold
        st.write("## Threshold (relative to input charge)")
        threshold=st.slider("Threshold", min_value=0.01, max_value=1.0, value=0.5, step=0.01)

        ## select chip mode
        st.write("## chip mode")
        # st.write("* mpx: medipix like mode (hit counting)")
        # st.write("* tpx: timepix like mode (charge integrating)")
        #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        chipMode=st.radio("chip mode", ["mpx: medipix like mode (hit counting)","tpx: timepix like mode (charge integrating)"], index=0)
        chipMode=chipMode[0:4]
        ## set output name
        st.write("## Output name")
        try:
            if name[-3:]=="mpx" and chipMode=="tpx":
                name=name[:-3]+"tpx"
            if name[-3:]=="tpx" and chipMode=="mpx":
                name=name[:-3]+"mpx"
            name=st.text_input("Output name", value=name, max_chars=20)
        except:
            name=st.text_input("Output name", value='simOut_Npix'+str(numPix)+'_'+chipMode, max_chars=20)

        ## ready
        st.write("### Set Ready")
        if "ready" not in pageDict.keys():
            pageDict['ready']=False

        if st.session_state.debug:
            st.write({'numPix':numPix,'beamWidth':beamWidth,'chargeSharing':chargeSharing,'threshold':threshold,'chipMode':chipMode,'name':name})
        if st.button("set ready"):
            pageDict['ready']=True
            pageDict['numPix']=numPix
            pageDict['beamWidth']=beamWidth
            pageDict['chargeSharing']=chargeSharing
            pageDict['threshold']=threshold
            pageDict['chipMode']=chipMode
            pageDict['name']=name

        if pageDict['ready']==False:
            st.write("Simulation is not set ready")
            st.stop()
        else:
            st.write("Simulation is ready. Run below")

        ### run simulation
        st.write("---")
        st.sidebar.title("## Run Simple Pixel Simulation")

        if st.button("Run Simulation!"):
            outVal=RunSimulation(pageDict)
            st.markdown(outVal)
        
        st.markdown("### Results")
        if "simResults" not in pageDict.keys():
            st.sidebar.markdown("No results yet")
        else:
            st.markdown("Got results :"+str(len(pageDict['simResults'])))

