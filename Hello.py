import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.write("# Statystyki zatrudnienia absolwentów")

uploaded_file = st.file_uploader("Załaduj plik z dealami z Pipedrive w formacie csv:")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.session_state['dataframe'] = dataframe
    st.write(dataframe)

st.markdown(
        """
        **👈 Wybierz z listy po lewej, jakie zestawienie chcesz wyświetlić
    """
    )