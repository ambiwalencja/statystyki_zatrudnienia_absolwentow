import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap


def process_data(df):
    # usuwamy niewłaściwe lost reasons
    df = df[~df['Deal - Lost reason'].str.contains('Duplikat|Rezygnacja|Błędne', na=False, case=False)] 
    # poprawiamy nazewnictwo kursów
    df['Deal - Nazwa kursu'] = df['Deal - Nazwa kursu'].str.replace('_old_', '', regex=False)
    # zmieniamy "Brak informacji" na nan
    df['Person - Znaleziona praca - czy znalazł pracę'] = df['Person - Znaleziona praca - czy znalazł pracę'].replace('Brak informacji', np.nan)
    df['Person - Znaleziona praca - czy się przebranżowił'] = df['Person - Znaleziona praca - czy się przebranżowił'].replace('Brak informacji', np.nan)
    df['Person - Znaleziona praca - czy związana z kursem'] = df['Person - Znaleziona praca - czy związana z kursem'].replace('Brak informacji', np.nan)
    # dodajemy nową zmienną - czy skorzystał ze wsparcia czy nie
    stage_list_after_support = ['Odbyte konsultacje', 'Przekazani do partnerów',  'Kandydaci', 'Po warsztatach CV', 'Po rozmowie 2', 'Po symulacjach']
    df['Czy skorzystał ze wsparcia'] = np.where(df['Deal - Stage'].isin(stage_list_after_support), "skorzystał", "nie skorzystał")

    #dodajemy nową zmienną - rok zakończenia kursu
    df['Deal - Termin zakończenia kursu'] = pd.to_datetime(df['Deal - Termin zakończenia kursu'])
    df['Deal - Termin zakończenia kursu - rok'] = df['Deal - Termin zakończenia kursu'].dt.year
    df['Deal - Termin zakończenia kursu - rok'] = df['Deal - Termin zakończenia kursu - rok'].astype('Int64')
    return df

def create_year_list(df):
    list_of_years = df['Deal - Termin zakończenia kursu - rok'].dropna().unique().tolist()
    list_of_years.insert(0, "Wszystkie lata")
    return list_of_years

def create_funding_source_list(df):
    list_of_funding_sources = df['Deal - Źródło finansowania'].dropna().unique().tolist()
    list_of_funding_sources.insert(0, "Wszystkie")
    return list_of_funding_sources

def create_course_list(df):
    list_of_courses = df['Deal - Nazwa kursu'].dropna().unique().tolist()
    list_of_courses.insert(0, "Wszystkie")
    return list_of_courses



# wykres przedstawiający procent poszczególnych odpowiedzi w stosunku do całej grupy, dla której posiadamy informacje
# czyli do 100% nie liczą się braki informacji
def create_one_variable_plot(df, x_variable):
    data_to_plot = df.dropna(axis=0, subset=x_variable)

    # sprawdzanie czy dane istnieją
    total = len(data_to_plot[x_variable])
    if total == 0:
        st.write("Brak danych do wyświetlenia")
        return
    st.write(f'Liczba osób: {total}')
    
    # obliczanie procentów
    value_counts = data_to_plot[x_variable].value_counts().reset_index()
    value_counts.columns = ['category', 'count']
    value_counts['percentage'] = value_counts['count'].apply(lambda x: 100 * x / total)

    # wykres
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.countplot(x=x_variable, data=data_to_plot, color='#087E8B', order=value_counts['category'], ax=ax)

    # ustawianie maksymalnej wartości dla osi y
    y_axis_max_val = data_to_plot[x_variable].value_counts().max() * 1.2
    ax.set_ylim(0, y_axis_max_val)

    # wrapowanie etykiet
    labels = [textwrap.fill(label.get_text(), width=20) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=40, ha="right")
    ax.tick_params(labelsize=14)

    # podpisywanie słupków wartościami
    for p, percentage in zip(ax.patches, value_counts['percentage']):
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '{:1.1f}%'.format(percentage), 
                ha="center", va="bottom", color="black", fontweight="bold", fontsize=14)

    ax.set_xlabel('')
    fig.suptitle(x_variable, fontsize=16)
    plt.tight_layout()
    plt.show()
    
    st.pyplot(fig)

    return True


def recode_job_variables(df):
    # rekodujemy zmienne czy znalazł pracę, czy się przebranżowił i czy praca związana z kursem na binarne
    df['Person - Znaleziona praca - czy znalazł pracę'] = df['Person - Znaleziona praca - czy znalazł pracę'].replace('Nie szuka', np.nan) # nie szuka w tym wypadku traktujemy jako brak informacji
    got_job = ['Tak', "Tak - awans w pracy"] # nie - nadal w tej samej pracy, nie - to zero. natomiast brak informacji powinien pozostać brakiem
    df['Czy znalazł pracę - binarna'] = np.where(df['Person - Znaleziona praca - czy znalazł pracę'].isin(got_job), 1, np.where(df['Person - Znaleziona praca - czy znalazł pracę'].isna(), np.nan, 0))
    df['Czy znalazł pracę - binarna'] = df['Czy znalazł pracę - binarna'].astype('Int64')
    changed_sector = ['Tak', 'Częściowo']
    df['Czy się przebranżowił - binarna'] = np.where(df['Person - Znaleziona praca - czy się przebranżowił'].isin(changed_sector), 1, np.where(df['Person - Znaleziona praca - czy się przebranżowił'].isna(), np.nan, 0))
    df['Czy się przebranżowił - binarna'] = df['Czy się przebranżowił - binarna'].astype('Int64')
    job_course_connected = ['Tak']
    df['Czy praca związana z kursem - binarna'] = np.where(df['Person - Znaleziona praca - czy związana z kursem'].isin(job_course_connected), 1, np.where(df['Person - Znaleziona praca - czy związana z kursem'].isna(), np.nan, 0))
    df['Czy praca związana z kursem - binarna'] = df['Czy praca związana z kursem - binarna'].astype('Int64')
    return

def recode_certificate_variable(df):
    df['Czy zaliczył kurs - binarna'] = np.where(df['Deal - Certyfikat - numer'].notnull(), "zaliczył", "nie zaliczył")
    return

def create_multiple_variable_plot_counts(df):
    # obliczanie dataframe'a
    count_data = df.groupby('Czy skorzystał ze wsparcia').agg({'Czy znalazł pracę - binarna': lambda x: (x==1).sum(), 'Czy się przebranżowił - binarna': lambda x: (x==1).sum(), 'Czy praca związana z kursem - binarna': lambda x: (x==1).sum()}).reset_index()
    melted_data = pd.melt(count_data, id_vars=['Czy skorzystał ze wsparcia'], value_vars=['Czy znalazł pracę - binarna', 'Czy się przebranżowił - binarna', 'Czy praca związana z kursem - binarna'], var_name='Variable', value_name='Count')

    # wykres
    fig, ax = plt.subplots(figsize=(10, 6)) # plt.figure(figsize=(10, 6))
    sns.barplot(data=melted_data, x='Variable', y='Count', hue='Czy skorzystał ze wsparcia')
    plt.title('Liczba osób, które odpowiedziały "Tak" na poszczególne pytania')
    plt.legend(title='Czy skorzystał ze wsparcia')
    plt.xlabel('')
    plt.show()
    
    for container in ax.containers:
        ax.bar_label(container, fontweight="bold")
    
    st.pyplot(fig)
    return


def create_multiple_variable_plot_percentages(df, x_variable_1, x_variable_2, x_variable_3, category_variable):
    # dla sprawdzenia tabele krzyżowe
    col1, col2, col3 = st.columns(3)
    with col1:
        crosstab1 = pd.crosstab(df[x_variable_1], df[category_variable])
        st.dataframe(crosstab1)
    with col2:
        crosstab2 = pd.crosstab(df[x_variable_2], df[category_variable])
        st.dataframe(crosstab2)
    with col3:
        crosstab3 = pd.crosstab(df[x_variable_3], df[category_variable])
        st.dataframe(crosstab3)
    
    
    def calculate_percentage(group):
        return group.sum() / group.count() * 100
    
    # obliczanie dataframe
    percent_data = df.groupby(category_variable).agg({x_variable_1: calculate_percentage, \
                                        x_variable_2: calculate_percentage, \
                                        x_variable_3: calculate_percentage}).reset_index()
    melted_data = pd.melt(percent_data, 
                          id_vars=[category_variable], 
                          value_vars=[x_variable_1, x_variable_2, x_variable_3], 
                          var_name='Variable', 
                          value_name='Percentage')
    # wykres
    fig, ax = plt.subplots(figsize=(10, 6)) # plt.figure(figsize=(10, 6))
    sns.barplot(data=melted_data, x='Variable', y='Percentage', hue=category_variable)
    plt.legend(title=category_variable)
    plt.xlabel('')
    plt.show()

    for container in ax.containers:
        ax.bar_label(container, fontweight="bold", fmt='%.1f%%')
    
    st.pyplot(fig)
    return