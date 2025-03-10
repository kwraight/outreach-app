### standard
import streamlit as st
from core.Page import Page
### custom
import pandas as pd
import altair as alt
from faker import Faker
from random import uniform, choice, randint
import ast
import csv
import copy
### PDB stuff
import core.stInfrastructure as infra
import commonCode.StreamlitTricks as stTrx


#####################
### useful functions
#####################

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))

infoList=["## Data Visualisation Pages",
        " 1. __DataViser__: Generate data and plots"]
#####################
### main part
#####################

class Page0(Page):
    def __init__(self):
        super().__init__("Info", "ℹ Information", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        [st.write(x) for x in infoList]

        # state.cwd=cwd
        if st.session_state.debug:
            st.error("Debug is on")
            st.write("Current directory:",cwd)
            st.write(os.listdir())

        ##
        st.write("### Happy Visualising 😀")