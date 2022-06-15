import streamlit as st
import muusikoidenTori as tori


def search(query, query_type, price_range):
    return tori.search(query, query_type, price_range)


st.title("Search Muusikoiden.net")
query_type = st.radio("Type", ["sell", "buy"])
price_range = st.slider("Price range", 0, 10000, (0, 10000), step=100, format="%f€")
query = st.text_input("Search for...")
if query:
    items = search(query, query_type, price_range)
    for item in items:
        full_text = st.expander(item["name"])
        full_text.write(item["description"])
        col1, col2 = st.columns([1, 1])
        col1.write(item["price"])
        col2.write('<div style="text-align: right"><a href='+item["link"]+'>LINK</a></div>', unsafe_allow_html=True)
