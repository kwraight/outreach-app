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