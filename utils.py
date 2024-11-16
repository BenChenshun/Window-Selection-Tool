# File: utils.py

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Navigation button functions
def Home():
    home = st.button("Return")
    if home:
        switch_page("Home")

def Go_to_Location():
    loc = st.button("Next")
    if loc:
        switch_page("house location")

def Back_to_Location():
    loc = st.button("Return")
    if loc:
        switch_page("house location")

def Go_to_House():
    house = st.button("Next")
    if house:
        switch_page("House Information")

def Back_to_House():
    house = st.button("Return")
    if house:
        switch_page("House Information")

def Go_to_Window():
    window = st.button("Next")
    if window:
        switch_page("Window Information")

def Back_to_Window():
    window = st.button("Return")
    if window:
        switch_page("Window Information")

def Go_to_Result():
    window = st.button("Finish and Run!")
    if window:
        switch_page("Results")
