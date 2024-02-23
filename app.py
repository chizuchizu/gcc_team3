import streamlit as st
import requests
import time
from instaloader import Instaloader, Profile
from facebook_scraper import get_profile
from typing import Dict
import pandas as pd
import plotly.express as px
import phonenumbers
from phonenumbers import geocoder
from pdf import create_pdf
import json

def display_map(country):
    df = pd.DataFrame({
            'country': [country],
                'iso_alpha': ['THA'],
                    'value': [1],  # You can adjust the values based on what you want to represent (e.g., population, GDP)
                    })

    # Creating the Choropleth map
    fig = px.choropleth(df, locations="iso_alpha",
                                            color="value",  # value that you want to color-code
                                            hover_name="country",  # column to add to hover information
                                            color_continuous_scale=px.colors.sequential.Plasma)

    # Displaying the map in the Streamlit app
    st.plotly_chart(fig)

def country_from_number(raw):
    phonenumber = "+" + raw[:2] +  " " + raw[2:]

    # Parse in the phone numbers from the txt file later
    phone_number = phonenumbers.parse(phonenumber)
    country = geocoder.description_for_number(phone_number, "en")

    print(f"The country of the phone number is: {country}")
    return country

st.title("Scam Detector")

col1, col2 = st.columns([3, 1])

def open_json(filepath: str) -> Dict:
    with open(filepath) as json_data:
        d = json.load(json_data)
    print(d)
    return d

info = open_json("data.json")

username = col1.text_input("username", "nahid_danica")

col2.write("")
num_of_cols = 3


if col2.button("Run"):
    with st.spinner("Now collecting..."):
        time.sleep(3)
    filepath = "telegram.json"
    text = f"""
    ## Telegram Details
    {info}
    """

    medias = ["Telegram", "Instagram", "Facebook"]

    for media in medias:

        st.markdown(f"## {media} Details")
        cols = st.columns(num_of_cols)
        for i, (key, value) in enumerate(info[media].items()):
            cols[i % num_of_cols].markdown("### " + key)
            cols[i % num_of_cols].markdown(value)

    path = "data.pdf"
    create_pdf(info, path)


    with open(path, "rb") as f:

        btn = st.download_button(
                label="Generate Reports",
                data=f,
                file_name=path,
        )

    location = country_from_number(info["Instagram"]["Phone Number"])
    st.write(f"The country of the phone number is: {location}")
    display_map(location)
