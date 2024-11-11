import streamlit as st
import pandas as pd
from functions import create_one_variable_plot, process_data, create_course_list, create_year_list

# 'Person - Znaleziona praca - czy znalazł pracę',
# 'Person - Znaleziona praca - czy się przebranżowił',
# 'Person - Znaleziona praca - czy związana z kursem',
# 'Deal - Termin zakończenia kursu'

st.set_page_config(layout="wide")

if 'dataframe' in st.session_state:
    df_persons = st.session_state['dataframe']

    df_persons = process_data(df_persons)

    st.write(' **Procent braków danych w poszczególnych zmiennych**')
    
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.write('Czy znalazł pracę')
    #     round(100*(data.isnull().sum()/len(data.index)),2)

    # st.table(round(100*(df_persons.isnull().sum()/len(df_persons.index)),2))

    df_persons = df_persons[['Person - Znaleziona praca - czy znalazł pracę',
                            'Person - Znaleziona praca - czy się przebranżowił',
                            'Person - Znaleziona praca - czy związana z kursem',
                            'Deal - Termin zakończenia kursu',
                            'Deal - Certyfikat - numer',
                            'Deal - Nazwa kursu',
                            'Deal - Źródło finansowania']]

    total = df_persons.isnull().sum().sort_values(ascending=False)
    percent = ((df_persons.isnull().sum()/df_persons.isnull().count())*100).round(2).sort_values(ascending=False)
    percent = percent.astype(str) + '%'
    missing_data = pd.concat([total, percent], axis=1, keys=['Liczba', 'Procent'])
    st.table(missing_data.head(20))
    
else:
    st.error("Nie znaleziono danych. Proszę załaduj plik z danymi na stronie Hello.")