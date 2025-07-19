
import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

# Load the Excel file
df = pd.read_excel("Book1.xlsx")

# Fill down Family and Sub Family
df[['Family', 'Sub Family']] = df[['Family', 'Sub Family']].fillna(method='ffill')

st.title("Product Catalog Explorer")

show_all = st.checkbox("Show All Data")

if show_all:
    st.subheader("Complete Product Catalog")
    st.dataframe(df)
else:
    families = df['Family'].dropna().unique()
    selected_families = st.multiselect("Select Family(s)", families)

    filtered_df = df[df['Family'].isin(selected_families)] if selected_families else df

    sub_families = filtered_df['Sub Family'].dropna().unique()
    selected_sub_families = st.multiselect("Select Sub Family(s)", sub_families)

    if selected_sub_families:
        filtered_df = filtered_df[filtered_df['Sub Family'].isin(selected_sub_families)]

    item_names = filtered_df['Item Name'].dropna().unique()
    selected_items = st.multiselect("Select Item Name(s)", item_names)

    if selected_items:
        filtered_df = filtered_df[filtered_df['Item Name'].isin(selected_items)]

    descriptions = filtered_df['Item Description'].dropna().unique()
    selected_descriptions = st.multiselect("Select Item Description(s)", descriptions)

    if selected_descriptions:
        filtered_df = filtered_df[filtered_df['Item Description'].isin(selected_descriptions)]

    # Fuzzy search with corrected index alignment
    search_query = st.text_input("Fuzzy Search (comma-separated, matches any column)", "")

    if search_query.strip():
        terms = [term.strip().lower() for term in search_query.split(',')]
        mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        for term in terms:
            for col in ['Item Name', 'Item Description', 'Size']:
                mask |= filtered_df[col].astype(str).str.lower().apply(lambda x: fuzz.partial_ratio(x, term) > 70)
        filtered_df = filtered_df[mask]

    # Display table
    display_df = filtered_df[['Item Name', 'Size', 'Item Description', 'Purchase Price', 'Sales Price']]
    st.subheader("Filtered Item Details")
    st.dataframe(display_df)
