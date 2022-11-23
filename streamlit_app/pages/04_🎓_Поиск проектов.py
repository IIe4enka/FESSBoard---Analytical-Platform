import streamlit as st
from streamlit import session_state as session
import streamlit_setup as setup
import pandas as pd
import numpy as np
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import plotly.express as px
from connectdb import mysql_conn
from datetime import date
 
 # Database Query
@st.experimental_memo(ttl=600)
def query_data(query):
    with mysql_conn() as conn:
        df = pd.read_sql(query, conn)
    return df

# Load projects dataset
@st.experimental_memo
def load_projects():
    query   =   """
                SELECT
                    projects.project_id 'ID',
                    companies.company_name 'Заказчик',
                    company_types.company_type 'Тип компании',
                    projects.project_name 'Название',
                    projects.project_description 'Описание',
                    projects.project_result 'Результат',
                    projects.project_start_date 'Дата начала',
                    projects.project_end_date 'Дата окончания',
                    project_grades.grade 'Грейд',
                    project_fields.field 'Направление',
                    projects.is_frozen 'Заморожен'
                FROM projects 
                LEFT JOIN project_grades
                    ON projects.project_grade   = project_grades.grade_id
                LEFT JOIN project_fields
                    ON projects.project_field   = project_fields.field_id
                LEFT JOIN (companies
                            LEFT JOIN company_types
                                ON companies.company_type = company_types.company_type_id)
                    ON projects.project_company = companies.company_id;
                """
    projects_df = query_data(query)
    projects_df['Дата окончания']   = pd.to_datetime(projects_df['Дата окончания'], format='%Y-%m-%d')
    projects_df['Дата начала']      = pd.to_datetime(projects_df['Дата начала'], format='%Y-%m-%d')
    projects_df['ID']               = pd.to_numeric(projects_df['ID'])
    return projects_df

# Apply filters and return filtered dataset
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.sidebar.checkbox("Показать фильтры")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Фильтровать по", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            if is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f" {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f" {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
                        # Treat columns with < 10 unique values as categorical
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 30:
                options = np.insert(df[column].unique(), 0, 'Все')
                user_cat_input = right.multiselect(
                    f"{column}",
                    options,
                    default='Все',
                )
                if 'Все' in (user_cat_input):
                    _cat_input = df[column].unique()
                else:
                    _cat_input = user_cat_input
                df = df[df[column].isin(_cat_input)]
            else:
                user_text_input = right.text_input(
                    f"{column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

@st.experimental_memo
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Запуск приложения
def run():
    # Загружаем датасет
    projects_df = load_projects()
    st.title('Поиск проектов')
    st.write('''
            На данной странице можно составить выборку проектов при заданных настройках.  
            Включить и выключить отображение фильтров можно в левой боковой панели приложения.
            Вы также можете скачать составленную выборку в формате .CSV (совместимо с Microsoft Excel)! \n
            :warning:Если добавить столбец в фильтр, но не указывать искомые значения, то будут искаться проекты с незаполненым полем!
            ''')
    # Отрисовываем фильтры и возвращаем отфильтрованный датесет
    projects_df_filtered = filter_dataframe(projects_df)
    tab1, tab2 = st.tabs(["Данные", "Аналитика"])
    with tab1:
        st.dataframe(projects_df_filtered, use_container_width=True)
        csv = convert_df(projects_df_filtered)
        st.download_button('Скачать таблицу', data=csv, file_name="fessboard_slice.csv", mime='text/csv', )
    with tab2:
        st.write('какая-то аналитика')

if __name__ == "__main__":
    setup.page_config(layout='centered', title='Поиск проектов')
    setup.remove_footer()
    run()