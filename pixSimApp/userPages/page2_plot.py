import streamlit as st
from core.Page import Page
### custom
import altair as alt
import pandas as pd

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

class Page3(Page):
    def __init__(self):
        super().__init__("Plots", "📊 Plotting Page ", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]
        setDict=st.session_state.Setup

        if st.session_state.debug:
            st.error("Debug is on")

        doWork=False
        
        if len(setDict['simResults'])<1:
            st.write("No results yet")
        else:
            st.write("Got results :"+str(len(setDict['simResults'])))
            doWork=True
            if st.session_state.debug: st.write(setDict['simResults'])


        if doWork:
            ## select results
            st.write("## Select data")
            results=st.selectbox("select results by name", setDict['simResults'], index=0, format_func=lambda x: x['name'])

            ## settings for selected dataset
            st.write("### Results")
            st.write("Settings of selected dataset")
            st.json(results['settings'], expanded=False)

            ## plotting
            ### collect pixel info.
            pix_xs = [p for p in range(0,len(results['pix_data'][0]),1)]
            pix_deps = [x for x in results['pix_data'][0]]
            pix_idxs = [0 for p in range(0,len(results['pix_data'][0]),1)]
            for i in range(1,results['settings']['numPix'],1):
                pix_xs.extend([p for p in range(0,len(results['pix_data'][i]),1)])
                pix_deps.extend([x for x in results['pix_data'][i]])
                pix_idxs.extend([i for p in range(0,len(results['pix_data'][i]),1)])

            ### put info. in dataframe
            pixel_data = pd.DataFrame({
            'x': pix_xs,
            'y': pix_deps,
            'px': pix_idxs
            })
            if st.session_state.debug:
                st.dataframe(pixel_data)

            ### plot dataframe
            st.write("### Visualisation")
            yTitle="Counts"
            if results['settings']['chipMode']=="tpx":
                yTitle="Charge deposited"
            myPlot=alt.Chart(pixel_data).mark_line().encode(
                x=alt.X('x', axis=alt.Axis(title="Arbitrary units")),
                y=alt.Y('y', axis=alt.Axis(title=yTitle)),
                color=alt.Color('px:O', scale=alt.Scale(scheme='dark2'), legend=alt.Legend(title="Pixel"))
            ).interactive()
            ### mark pixel limits
            line_data = pd.DataFrame({'a': [x*55.0 for x in range(0,results['settings']['numPix']+1,1) ]})
            pix_lines=alt.Chart(line_data).mark_rule(strokeDash=[1,1],size=3).encode(
                x=alt.X('a:Q', axis=alt.Axis(labels=False))
            )

            combPlot=myPlot+pix_lines
            st.altair_chart(combPlot, use_container_width=True)

            if st.checkbox("Delete result?"):
                if st.button("Delete"):
                    del setDict['simResults'][setDict['simResults'].index(results)]
                    st.write("Results deleted. Untick box to reset page.")