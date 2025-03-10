import streamlit as st
from core.Page import Page
### custom
import datetime
import os
import sys
cwd = os.getcwd()
sys.path.insert(1, cwd)
### for streamlitShare
cwd = os.getcwd()

#####################
### useful functions
#####################

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))

infoList=["### Pixel Simulation Pages",
        "  1. __Setup__: Set simulation parameters & generate data",
        "  2. __Plots__: Visualise simulation results"
        ]
#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Info", "ℹ Information", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        st.write(" --- ")
        ###

        st.write("### Simple pixel detecter 1D simulation")

        [st.write(x) for x in infoList]

        # state.cwd=cwd
        if st.session_state.debug:
            st.error("Debug is on")
            st.write("Current directory:",cwd)
            st.write(os.listdir())

        ##
        st.write("### Happy Simulating")
