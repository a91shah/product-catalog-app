import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

# Load Excel file
df = pd.read_excel("Book1.xlsx")
df[['Family', 'Sub Family']] = df[['Family', 'Sub Family']].fillna(method='ffill')

st.title("Product Catalog Explorer")

show_all = st.checkbox("Show All Data")

if show_all:
    st.subheader("Complete Product Catalog")
    st.dataframe(df)
else:
    # Family filter
    families = df['Family'].dropna().unique()
    selected_families = st.multiselect("Select Family(s)", families)
    filtered_df = df[df['Family'].isin(selected_families)] if selected_families else df

    # Sub Family filter
    sub_families = filtered_df['Sub Family'].dropna().unique()
    selected_sub_families = st.multiselect("Select Sub Family(s)", sub_families)
    filtered_df = filtered_df[filtered_df['Sub Family'].isin(selected_sub_families)] if selected_sub_families else filtered_df

    # Item Name filter
    item_names = filtered_df['Item Name'].dropna().unique()
    selected_items = st.multiselect("Select Item Name(s)", item_names)
    filtered_df = filtered_df[filtered_df['Item Name'].isin(selected_items)] if selected_items else filtered_df

    # Size filter
    sizes = filtered_df['Size'].dropna().unique()
    selected_sizes = st.multiselect("Select Size(s)", sizes)
    filtered_df = filtered_df[filtered_df['Size'].isin(selected_sizes)] if selected_sizes else filtered_df

    # Item Description filter
    descriptions = filtered_df['Item Description'].dropna().unique()
    selected_descriptions = st.multiselect("Select Item Description(s)", descriptions)
    filtered_df = filtered_df[filtered_df['Item Description'].isin(selected_descriptions)] if selected_descriptions else filtered_df

    # Fuzzy Search
    search_query = st.text_input("Fuzzy Search (comma-separated, matches Item Name, Description, or Size)", "")
    if search_query.strip():
        terms = [term.strip().lower() for term in search_query.split(',')]
        mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        for term in terms:
            for col in ['Item Name', 'Item Description', 'Size']:
                mask |= filtered_df[col].astype(str).str.lower().apply(lambda x: fuzz.partial_ratio(x, term) > 70)
        filtered_df = filtered_df[mask]

    # Display results
    display_df = filtered_df[['Item Name', 'Size', 'Item Description', 'Purchase Price', 'Sales Price']]
    st.subheader("Filtered Item Details")
    st.dataframe(display_df)
