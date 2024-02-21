import streamlit as st
import requests
from instaloader import Instaloader, Profile
from facebook_scraper import get_profile
from typing import Dict

from pdf import create_pdf
import json

st.title("Scam Detector")

col1, col2 = st.columns([3, 1])

def open_json(filepath: str) -> Dict:
    with open(filepath) as json_data:
        d = json.load(json_data)
    print(d)
    return d

info = open_json("data.json")

username = col1.text_input("username", "wassupkanti")

col2.write("")
num_of_cols = 3

if col2.button("Run"):

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

