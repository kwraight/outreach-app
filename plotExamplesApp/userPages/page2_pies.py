### standard
import streamlit as st
from core.Page import Page
### custom
import pandas as pd
import altair as alt
from vega_datasets import data
import numpy as np
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
        super().__init__("Pies", "🥧 Pie Chart Examples", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        selOpts=["Pacman","Pyramid"]
        sel_plot=st.selectbox("Select plot",selOpts,format_func=lambda x: x.title())

        if "pyramid" in sel_plot.lower():

            category = ['Sky', 'Shady side of a pyramid', 'Sunny side of a pyramid']
            color = ["#416D9D", "#674028", "#DEAC58"]
            source = pd.DataFrame({'category': category, 'value': [75, 10, 15]})

            chart=alt.Chart(source).mark_arc(outerRadius=80).encode(
                alt.Theta('value:Q', scale=alt.Scale(range=[2.356, 8.639])),
                alt.Color('category:N',
                    scale=alt.Scale(domain=category, range=color),
                    legend=alt.Legend(title=None, orient='none', legendX=160, legendY=50)),
                order='value:Q'
            ).properties(width=600, height=400).configure_view(strokeOpacity=0)
     

        elif "pac" in sel_plot.lower():
            source = pd.DataFrame()

            chart=alt.Chart().mark_arc(color="gold").encode(
                theta=alt.datum((5 / 8) * np.pi, scale=None),
                theta2=alt.datum((19 / 8) * np.pi),
                radius=alt.datum(100, scale=None),
            ).properties(width=600, height=400)

        else:
            st.write("Please select example.")


        ### Show stuff
        st.write(f"### {sel_plot.title()}")
        if st.checkbox("Show data"):
            st.write(source)
        st.write(chart)
