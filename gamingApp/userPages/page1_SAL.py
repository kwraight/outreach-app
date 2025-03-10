### standard
import streamlit as st
from core.Page import Page
### custom
import pandas as pd
import altair as alt
from vega_datasets import data
from datetime import datetime
from random import seed, randint
import ast
import csv
import copy
import time
### PDB stuff
import core.stInfrastructure as infra
import commonCode.StreamlitTricks as stTrx


#####################
### useful functions
#####################
### define game
def PlaySALGame(pageDict, seed_val=0):

    # pass settings
    players=pageDict['players']
    snakeDict=pageDict['snakeDict']
    ladderDict=pageDict['ladderDict']
    rollAgain=pageDict['roll_again']
    squares=pageDict['tile_num']

    ### set up players
    playerList=[]
    for p in range(1,players+1):
        playerList.append({'name':f"Player{p}",'position':0})

    winCondition=False
    moveLog=[]
    count=0
    for pl in playerList:
        # print(pl)
        moveLog.append(dict({'moveIndex':count}, **pl))
    # play!

    seed( seed_val )
    print(f" - with seed {seed_val}")

    # until winner 
    while not winCondition:
        # loop over players
        for pl in playerList:
            count+=1
            roll=True
            while roll:
                diceRoll= randint(1,6)
                pl['position']+=diceRoll
                # check snakes
                if pl['position'] in snakeDict['points'].keys():
                    pl['position']+= snakeDict['points'][pl['position']]*snakeDict['scale']
                # check ladders
                if pl['position'] in ladderDict['points'].keys():
                    pl['position']+= ladderDict['points'][pl['position']]*ladderDict['scale']
                # check for winner
                if pl['position']>=squares:
                    winCondition=True
                    break
                # roll again?
                if rollAgain==False or diceRoll!=6:
                    roll=False
            # print(pl)
            moveLog.append(dict({'moveIndex':count}, **pl))
            # end if win
            if winCondition:
                break

    return moveLog


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
        super().__init__("🐍 & 🪜", "🎲 Snakes and Ladders", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ##################
        ### settings
        ##################
        st.write("## Settings")
        st.write("Setting up the game")

        st.write("### Board settings")
        if "snakeDict" not in pageDict.keys():
            pageDict['snakeDict']={'name':"Snakes", 'number':5, 'length':[5,10], 'points':None, 'scale':-1}
            pageDict['ladderDict']={'name':"Ladders", 'number':5, 'length':[5,10], 'points':None, 'scale':1}

        pageDict['tile_num']=st.number_input('How many squares on the board?', min_value=50, max_value=200, value=100)

        if st.write("Set-up snakes and ladders"):
            sal_num=st.number_input('How many snakes and ladders?',min_value=0, max_value=10, value=5)
            pageDict['snakeDict']['number']=sal_num
            pageDict['ladderDict']['number']=sal_num
        
        ### set snakes and ladders positions
        if st.button("Set board"):
            margin=5
            pageDict['snakeDict']['points']={randint(0+margin, pageDict['tile_num']-margin):randint(pageDict['snakeDict']['length'][0],pageDict['snakeDict']['length'][1]) for s in range(0,pageDict['snakeDict']['number'],1)}
            pageDict['ladderDict']['points']={randint(0+margin, pageDict['tile_num']-margin):randint(pageDict['ladderDict']['length'][0],pageDict['ladderDict']['length'][1]) for s in range(0,pageDict['ladderDict']['number'],1)}
            # check overlap
            while bool( set(pageDict['snakeDict']['points'].keys()) & set(pageDict['ladderDict']['points'].keys()) ):
                for x in list( set(pageDict['snakeDict']['points'].keys()) & set(pageDict['ladderDict']['points'].keys()) ):
                    pageDict['ladderDict']['points'][x+1]=pageDict['ladderDict']['points'][x]
                    del(pageDict['ladderDict']['points'][x])
            st.write(" - board updated ✅")
        
        
        st.write("### Player settings")
        pageDict['players']=st.number_input('How many players?', min_value=2, max_value=10, value=2)


        st.write("### Game settings")
        pageDict['roll_again']=st.checkbox('Roll again with six?', value=False)


        st.write("---")

        ##################
        ### games
        ##################

        st.write("## Play games")

        game_num=st.number_input('How many games?', min_value=1, max_value=100, value=1)

        ### games loop
        if st.button("Play games!"):
            # reset metric
            metric=[]
            pageDict['game_num']=game_num

            prog_bar = st.progress(0)
            prog_txt = st.empty()

            dt = datetime.today()  # Get timezone naive now
            seconds = dt.timestamp()
            for g in range(1,game_num+1,1):
                prog_bar.progress( 1.0*g/game_num)
                prog_txt.markdown(f" - playing game {g}")
                moveLog=PlaySALGame(pageDict, seconds+g)
                # display(pd.DataFrame(moveLog))
                print(moveLog[-1])
                # print(moveLog[-1])
                metric.append(moveLog[-1])
                time.sleep(0.1)


            prog_txt.markdown("Playing complete!")
            pageDict['metric']=metric

        ### set metric
        if "metric" not in pageDict.keys() or "game_num" not in pageDict.keys() or pageDict['game_num']!=game_num:
            st.write("Run games to get data")
            st.stop()

        if len(pageDict['metric'])<1:
            st.write("Play games when ready")
            st.stop()
        
        df_metric=pd.DataFrame(pageDict['metric'])
        if st.checkbox("Show results?", value=True):
            st.write(df_metric)

        st.write("---")

        ##################
        ### visualisation
        ##################
        st.write("## Results")
        nameMap={'name':"Winning Player", 'moveIndex':"Number of Turns", 'position':"Final Position"}
        for col in df_metric.columns:
            # st.write(f"### {col}")
            if "name" in col:
                chart=alt.Chart(df_metric).mark_bar().encode(
                            x=alt.X(col+':O', title=nameMap[col], axis=alt.Axis(labelAngle=-45)), 
                            y=alt.Y('count():Q', title="Frequency"),
                            color=alt.Color('name:N'),
                            tooltip=[col+':Q','count():Q']
                        ).properties(
                        title={
                            'text':[f"Distribution from {pageDict['game_num']} games"],
                            },           
                        width=600)
                st.write(chart)
                st.write(" - __Most Wins__:", df_metric[col].mode().values[0])
            
            else:
                chart=alt.Chart(df_metric).mark_bar().encode(
                            x=alt.X(col+':Q', bin=True, title=nameMap[col]), 
                            y=alt.Y('count():Q', title="Frequency"),
                            tooltip=[col+':Q','count():Q']
                        ).properties(
                        title={
                            'text':[f"Distribution from {pageDict['game_num']} games"],
                            },           
                        width=600)
                st.write(chart)
                st.write(" - __Average__:", df_metric[col].mean())