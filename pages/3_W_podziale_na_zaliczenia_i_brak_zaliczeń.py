import streamlit as st
import pandas as pd
from functions import process_data, recode_job_variables, create_multiple_variable_plot_percentages, create_year_list, recode_certificate_variable

st.set_page_config(layout="wide")

if 'dataframe' in st.session_state:
    df_persons = st.session_state['dataframe']
    df_persons = process_data(df_persons)
    recode_job_variables(df_persons)
    recode_certificate_variable(df_persons)

    st.write(' **Wybierz rok, dla którego chcesz przedstawić statystyki**')

    # wybór lat
    list_of_years = create_year_list(df_persons)
    year = st.selectbox("Rok zakończenia kursu",list_of_years)
    st.write('Wybrany rok: ', year)

    if year != 'Wszystkie lata':
        df_persons = df_persons.loc[df_persons['Deal - Termin zakończenia kursu - rok']==year]

    create_multiple_variable_plot_percentages(df_persons, 'Czy znalazł pracę - binarna', 'Czy się przebranżowił - binarna', 'Czy praca związana z kursem - binarna', 'Czy zaliczył kurs - binarna')
else:
    st.error("Nie znaleziono danych. Proszę załaduj plik z danymi na stronie Hello.")