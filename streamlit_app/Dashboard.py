import streamlit as st
from streamlit import session_state as session
from st_init import init

# Подключение к БД
def run():
    test = st.text_input('Переменная на странице дашборд')
    btn = st.button('Сохранить')
    if btn:
        session['test_123'] = test

if __name__ == '__main__':
    init()
    run()