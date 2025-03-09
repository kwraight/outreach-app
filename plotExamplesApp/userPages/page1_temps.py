### standard
import streamlit as st
from core.Page import Page
### custom
import pandas as pd
import altair as alt
from vega_datasets import data
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

class Page1(Page):
    def __init__(self):
        super().__init__("Weather", "📊 Data Visualisation Examples", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        selOpts=["Annual Weather Heatmap","Hexabin Chart", "Scatter Plot with Rolling Mean"]
        sel_plot=st.selectbox("Select plot",selOpts,format_func=lambda x: x.title())

        if "annual" in sel_plot.lower():

            source = data.seattle_weather()

            chart=alt.Chart(source, title="Daily Max Temperatures (C) in Seattle, WA", width=600).mark_rect().encode(
                x=alt.X("date(date):O", title="Day", axis=alt.Axis(format="%e", labelAngle=0)),
                y=alt.Y("month(date):O", title="Month"),
                color=alt.Color("max(temp_max)", legend=alt.Legend(title=None)),
                tooltip=[
                    alt.Tooltip("monthdate(date)", title="Date"),
                    alt.Tooltip("max(temp_max)", title="Max Temp"),
                ],
            ).configure_view(step=13, strokeWidth=0).configure_axis(domain=False)

        elif "hexabin" in sel_plot.lower():
            source = data.seattle_weather()

            # Size of the hexbins
            size = 15
            # Count of distinct x features
            xFeaturesCount = 12
            # Count of distinct y features
            yFeaturesCount = 7
            # Name of the x field
            xField = 'date'
            # Name of the y field
            yField = 'date'

            # the shape of a hexagon
            hexagon = "M0,-2.3094010768L2,-1.1547005384 2,1.1547005384 0,2.3094010768 -2,1.1547005384 -2,-1.1547005384Z"

            chart=alt.Chart(source).mark_point(size=size**2, shape=hexagon).encode(
                x=alt.X('xFeaturePos:Q', axis=alt.Axis(title='Month',
                                                    grid=False, tickOpacity=0, domainOpacity=0)),
                y=alt.Y('day(' + yField + '):O', axis=alt.Axis(title='Weekday',
                                                            labelPadding=20, tickOpacity=0, domainOpacity=0)),
                stroke=alt.value('black'),
                strokeWidth=alt.value(0.2),
                fill=alt.Fill('mean(temp_max):Q', scale=alt.Scale(scheme='darkblue')),
                tooltip=['month(' + xField + '):O', 'day(' + yField + '):O', 'mean(temp_max):Q']
            ).transform_calculate(
                # This field is required for the hexagonal X-Offset
                xFeaturePos='(day(datum.' + yField + ') % 2) / 2 + month(datum.' + xField + ')'
            ).properties(
                # Exact scaling factors to make the hexbins fit
                width=size * xFeaturesCount * 3,
                height=size * yFeaturesCount * 1.7320508076*1.25,  # 1.7320508076 is approx. sin(60°)*2
            ).configure_view(
                strokeWidth=0
            )

        elif "rolling" in sel_plot.lower():
            source = data.seattle_weather()

            line = alt.Chart(source).mark_line(
                color='red',
                size=3
            ).transform_window(
                rolling_mean='mean(temp_max)',
                frame=[-15, 15]
            ).encode(
                x='date:T',
                y='rolling_mean:Q'
            )

            points = alt.Chart(source, width=600).mark_point().encode(
                x='date:T',
                y=alt.Y('temp_max:Q',
                        axis=alt.Axis(title='Max Temp')),
                color="weather",
            )

            chart= points 

        else:
            st.write("Please select example.")


        ### Show stuff
        st.write(f"{sel_plot.title()}")
        if st.checkbox("Show data"):
            st.write(source)
        st.write(chart)
