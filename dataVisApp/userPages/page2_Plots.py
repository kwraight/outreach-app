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

infoList=["### Instructions",
        " __NB__ Currently only supporting [_Altair_](https://altair-viz.github.io)",
        "  1. Select _chart type_ and _population_ (number of entries)",
        "  2. Input _channels_ (types of information) - _X_ & _Y_ required",
        "  3. Generate data (based on _channel_ inputs)",
        "  4. Plot data"]
#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Plots", ":microscope: Interesting Plots", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        selOpts=["pyramid","anscombe's quartet"]
        sel_plot=st.selectbox("Select plot",selOpts,format_func=lambda x: x.title())

        st.write(f"{sel_plot.title()}")

