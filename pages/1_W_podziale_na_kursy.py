import streamlit as st
import pandas as pd
from functions import create_one_variable_plot, process_data, create_course_list, create_year_list, create_funding_source_list

# czcionka Helvetica, Tahoma, Arial, Verdana - ?

st.set_page_config(layout="wide")

if 'dataframe' in st.session_state:
    df_persons = st.session_state['dataframe']

    df_persons = process_data(df_persons)

    st.write(' **Wybierz rok oraz kurs, dla których chcesz przedstawić statystyki**')

    # wybór lat
    list_of_years = create_year_list(df_persons)
    year = st.selectbox("Rok zakończenia kursu",list_of_years)
    st.write('Wybrany rok: ', year)

    if year != 'Wszystkie lata':
        df_persons = df_persons.loc[df_persons['Deal - Termin zakończenia kursu - rok']==year]
    
    # wybór źródła finansowania
    list_of_funding_sources = create_funding_source_list(df_persons)
    funding_source = st.selectbox("Źródło finansowania",list_of_funding_sources)
    st.write('Wybrane źródło finansowania: ', funding_source)

    if funding_source != 'Wszystkie':
        df_persons = df_persons.loc[df_persons['Deal - Źródło finansowania'] == funding_source]

    # wybór kursu
    list_of_courses = create_course_list(df_persons)
    course = st.selectbox("Ukończony kurs",list_of_courses)
    st.write('Wybrany kurs: ', course)

    if course == 'Wszystkie':
        data_to_plot = df_persons.drop_duplicates(subset='Person - ID')
    else:
        data_to_plot = df_persons.loc[df_persons['Deal - Nazwa kursu']==course]
    
    persons_columns_closed = ['Person - Znaleziona praca - czy znalazł pracę',
                    'Person - Znaleziona praca - czy się przebranżowił',
                    'Person - Znaleziona praca - czy związana z kursem']
    
    col1, col2 = st.columns(2)
    for index, column in enumerate(persons_columns_closed):
        if index in [0,2]:
            with col1:
                create_one_variable_plot(data_to_plot, column)
        else:
            with col2:
                create_one_variable_plot(data_to_plot, column)
else:
    st.error("No data found. Please upload a file in the Hello page.")